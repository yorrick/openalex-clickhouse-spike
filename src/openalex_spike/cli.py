from __future__ import annotations

from argparse import ArgumentParser, Namespace
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from time import monotonic
import hashlib
import json
import os
import re
import sys

from openalex_spike.benchmark import (
    BenchmarkQuery,
    ServiceBenchmarkClient,
    load_query_catalog,
    run_sequential,
)
from openalex_spike.clickhouse import ClickHouseService, ResourcePreflightError
from openalex_spike.concurrency import run_closed_loop, summarize_concurrency
from openalex_spike.config import ExperimentConfig
from openalex_spike.correctness import (
    evaluate_stage1,
    require_all,
    write_correctness,
)
from openalex_spike.download import (
    download_files,
    materialize_supporting_entities,
    materialize_tier_links,
    object_path,
    verify_downloads,
)
from openalex_spike.manifest import (
    SELECTED_SMALL_ENTITIES,
    EntityManifest,
    pin_manifest_set,
    reconcile_pinned_manifests,
)
from openalex_spike.report import render_report
from openalex_spike.sampling import (
    ALGORITHM,
    STAGE1_BIAS_CAVEAT,
    SelectedFile,
    select_nested,
    write_selection,
)
from openalex_spike.storage import (
    DecimatedFilesystemSampler,
    StorageMonitor,
    collect_storage_sample,
    write_storage_samples,
)
from openalex_spike.stage2 import (
    STAGE2_TIERS,
    Stage2PrerequisiteError,
    artifact_hashes,
    build_run_identity,
    file_sha256,
    maximum_input_bytes,
    nested_stage2_tiers,
    require_free_space,
    require_resume_identity,
    required_build_free_bytes,
    required_download_free_bytes,
    stage2_local_verdict,
    stage2_performance_verdict,
    verify_artifact_hashes,
    worst_stage2_verdict,
)


COMMAND_VERSION = "0.1.0"


class PrerequisiteError(RuntimeError):
    pass


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _state_path(root: Path, name: str) -> Path:
    return root / ".data" / "state" / f"{name}.json"


def _write_json_atomic(destination: Path, document: object) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f"{destination.name}.tmp")
    temporary.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, destination)


def _write_jsonl_atomic(destination: Path, rows: list[dict[str, object]]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f"{destination.name}.tmp")
    with temporary.open("w") as output:
        for row in rows:
            output.write(json.dumps(row, sort_keys=True) + "\n")
    os.replace(temporary, destination)


def _write_state(root: Path, name: str, **values: object) -> Path:
    path = _state_path(root, name)
    _write_json_atomic(
        path,
        {
            "command": name,
            "command_version": COMMAND_VERSION,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            **values,
        },
    )
    return path


def _require_state(root: Path, name: str) -> dict[str, object]:
    path = _state_path(root, name)
    if not path.exists():
        raise PrerequisiteError(f"missing prerequisite state: {path}")
    return json.loads(path.read_text())


def _config(root: Path) -> ExperimentConfig:
    path = root / "config" / "experiment.toml"
    if not path.exists():
        raise PrerequisiteError(f"missing experiment configuration: {path}")
    return ExperimentConfig.load(path)


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_raw_glob(value: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"unsafe raw-data glob: {value}")
    if path.parts[0] != "tiers" or "'" in value or '"' in value:
        raise ValueError(f"raw-data glob must remain under /raw/tiers: {value}")
    return value


def _database_identifier(value: str) -> str:
    if not re.fullmatch(r"[a-z][a-z0-9_]*", value):
        raise ValueError(f"invalid database identifier: {value}")
    return value


def render_sql_template(
    path: Path, *, database: str, globs: dict[str, str]
) -> tuple[str, str]:
    database = _database_identifier(database)
    sql = path.read_text().replace("openalex_spike", database)
    for name, value in globs.items():
        validated = validate_raw_glob(value)
        sql = sql.replace(f"{{{{{name}}}}}", validated)
    if "{{" in sql:
        raise ValueError(f"unresolved SQL template in {path}")
    sha256 = hashlib.sha256(sql.encode()).hexdigest()
    print(f"rendered {path.name} sha256={sha256}", flush=True)
    return sql, sha256


def _manifest_paths(root: Path) -> dict[str, Path]:
    manifest_dir = root / ".data" / "manifests"
    paths = {
        path.name.removesuffix("-manifest.json"): path
        for path in manifest_dir.glob("*-manifest.json")
        if path.name != "combined-manifest.json"
    }
    return paths


def command_pin_manifests(args: Namespace) -> int:
    root: Path = args.root
    cfg = _config(root)
    destination = root / ".data" / "manifests"
    print("pinning combined, Works, Authors, and selected dimension manifests", flush=True)
    manifests = pin_manifest_set(
        destination,
        cfg.combined_manifest_url,
        include_authors=True,
    )
    _write_state(
        root,
        "pin-manifests",
        combined_manifest=str(destination / "combined-manifest.json"),
        entities={
            entity: {
                "content_length": manifest.content_length,
                "record_count": manifest.record_count,
                "files": len(manifest.files),
            }
            for entity, manifest in manifests.items()
        },
    )
    print(f"pinned {len(manifests)} entity manifests", flush=True)
    return 0


def command_select(args: Namespace) -> int:
    root: Path = args.root
    _require_state(root, "pin-manifests")
    cfg = _config(root)
    works_path = root / ".data" / "manifests" / "works-manifest.json"
    metadata_path = works_path.with_name(f"{works_path.name}.metadata.json")
    if not works_path.exists() or not metadata_path.exists():
        raise PrerequisiteError("pinned Works manifest or metadata is missing")
    manifest = EntityManifest.from_path(works_path)
    metadata = json.loads(metadata_path.read_text())
    selection = select_nested(manifest.files, cfg.tiers, cfg.seed)
    destination = root / ".data" / "selection.json"
    write_selection(
        destination,
        selection,
        cfg.tiers,
        cfg.seed,
        str(metadata["etag"]),
        str(metadata["sha256"]),
        manifest.files,
    )
    _write_state(
        root,
        "select",
        selection=str(destination),
        selection_sha256=_sha256_path(destination),
        tiers={
            tier: {
                "files": len(files),
                "content_length": sum(file.content_length for file in files),
                "record_count": sum(file.record_count for file in files),
            }
            for tier, files in selection.items()
        },
    )
    for tier, files in selection.items():
        print(
            f"{tier}: {len(files)} files, "
            f"{sum(file.content_length for file in files):,} bytes",
            flush=True,
        )
    return 0


def _selected_tier(root: Path, tier: str) -> list[SelectedFile]:
    selection_path = root / ".data" / "selection.json"
    if not selection_path.exists():
        raise PrerequisiteError(f"missing selection document: {selection_path}")
    raw = json.loads(selection_path.read_text())
    if raw.get("algorithm") != ALGORITHM:
        raise PrerequisiteError(
            f"selection algorithm is {raw.get('algorithm')!r}; "
            f"rerun select with {ALGORITHM}"
        )
    if tier not in raw["tiers"]:
        raise PrerequisiteError(f"selection has no tier named {tier}")
    return [SelectedFile(**item) for item in raw["tiers"][tier]["files"]]


def command_download(args: Namespace) -> int:
    root: Path = args.root
    _require_state(root, "select")
    tier = args.tier
    selection_sha256 = _sha256_path(root / ".data" / "selection.json")
    tier_names = nested_stage2_tiers(tier)
    works_selections = {
        tier_name: _selected_tier(root, tier_name) for tier_name in tier_names
    }
    works_files = works_selections[tier]
    manifest_paths = _manifest_paths(root)
    required_entities = set(SELECTED_SMALL_ENTITIES) if args.include_small_dimensions else set()
    if args.include_complete_authors:
        required_entities.add("authors")
    missing = required_entities - manifest_paths.keys()
    if missing:
        raise PrerequisiteError(f"missing pinned entity manifests: {sorted(missing)}")
    manifests = reconcile_pinned_manifests(
        root / ".data" / "manifests" / "combined-manifest.json",
        [manifest_paths[name] for name in sorted(required_entities | {"works"})],
    )
    supporting_files = [
        file
        for entity in sorted(required_entities)
        for file in manifests[entity].files
    ]
    all_files = [*works_files, *supporting_files]
    raw_root = root / ".data" / "raw"
    if (
        tier == "stage2_large"
        and args.include_complete_authors
        and args.include_small_dimensions
    ):
        selection = json.loads((root / ".data" / "selection.json").read_text())
        pin_state = _require_state(root, "pin-manifests")
        maximum_raw_bytes = maximum_input_bytes(selection, pin_state)
        unique_files = {file.url: file for file in all_files}
        remaining = sum(
            file.content_length
            for file in unique_files.values()
            if not object_path(raw_root / "objects", file.url).exists()
        )
        required = required_download_free_bytes(
            remaining_object_bytes=remaining,
            maximum_raw_input_bytes=maximum_raw_bytes,
        )
        available = require_free_space(
            root,
            required_bytes=required,
            purpose="the Stage 2 download and ClickHouse build",
        )
        print(
            f"Stage 2 disk preflight passed: {available:,} bytes free; "
            f"conservative requirement {required:,} bytes",
            flush=True,
        )
    print(
        f"downloading/verifying {len(all_files)} selected files "
        f"({sum(file.content_length for file in all_files):,} bytes)",
        flush=True,
    )
    object_paths = download_files(all_files, raw_root / "objects")
    groups: dict[str, list] = {
        f"{tier_name}/works": files
        for tier_name, files in works_selections.items()
    }
    for tier_name in tier_names:
        for entity in sorted(required_entities):
            groups[f"{tier_name}/{entity}"] = list(manifests[entity].files)
    verification_path = root / ".data" / f"download-verification-{tier}.json"
    verification = verify_downloads(groups, object_paths, verification_path)
    materialize_tier_links(
        raw_root,
        works_selections,
        object_paths,
        entity="works",
    )
    materialize_supporting_entities(
        raw_root,
        tier_names,
        manifests,
        object_paths,
        include_complete_authors=args.include_complete_authors,
    )
    _write_state(
        root,
        f"download-{tier}",
        tier=tier,
        selection_algorithm=ALGORITHM,
        selection_sha256=selection_sha256,
        include_complete_authors=args.include_complete_authors,
        include_small_dimensions=args.include_small_dimensions,
        verification=str(verification_path),
        groups={
            name: {
                "content_length": values["content_length"],
                "record_count": values["record_count"],
                "files": len(values["files"]),
            }
            for name, values in verification["tiers"].items()
        },
    )
    print(f"download verified and materialized for {tier}", flush=True)
    return 0


def command_clickhouse_up(args: Namespace) -> int:
    service = ClickHouseService(args.root)
    service.up(memory_gb=args.memory_gb, cpus=args.cpus)
    evidence_path = args.root / ".data" / "evidence" / "environment.json"
    service.write_environment_evidence(evidence_path)
    print(f"ClickHouse {service.query_value('SELECT version()')} is ready", flush=True)
    return 0


def command_clickhouse_down(args: Namespace) -> int:
    ClickHouseService(args.root).down()
    return 0


def _raw_evidence(
    service: ClickHouseService,
    sql_dir: Path,
    database: str,
    globs: dict[str, str],
) -> tuple[dict[str, int], dict[str, str]]:
    sql, sha256 = render_sql_template(
        sql_dir / "05_raw_evidence.sql", database=database, globs=globs
    )
    rows = [json.loads(line) for line in service.execute_script(sql).splitlines()]
    if len(rows) != 2:
        raise RuntimeError(f"unexpected raw-evidence output: {rows}")
    evidence = {**rows[0], **rows[1]}
    if int(evidence["rejected_id_entries"]) != 0:
        raise RuntimeError(f"raw reference ID rejection gate failed: {evidence}")
    if int(evidence["null_topic_scores"]) != 0:
        raise RuntimeError(f"null topic score gate failed: {evidence}")
    return {name: int(value) for name, value in evidence.items()}, {
        "05_raw_evidence.sql": sha256
    }


def _build_stage1_database(
    service: ClickHouseService,
    *,
    root: Path,
    database: str,
    globs: dict[str, str],
    expected_rows: int,
    result_dir: Path,
    minimum_ordinary_author_reference_coverage: float,
) -> tuple[
    dict[str, object], list[dict[str, object]], dict[str, object]
]:
    sql_dir = root / "sql"
    service.execute_script(f"DROP DATABASE IF EXISTS {_database_identifier(database)}")
    hashes: dict[str, str] = {}
    schema, hashes["00_schema.sql"] = render_sql_template(
        sql_dir / "00_schema.sql", database=database, globs=globs
    )
    service.execute_script(schema)
    raw_evidence, raw_hash = _raw_evidence(service, sql_dir, database, globs)
    hashes.update(raw_hash)
    monitor = StorageMonitor(
        lambda: collect_storage_sample(
            service.query_json,
            database=database,
            clickhouse_data_dir=root / ".data" / "clickhouse",
        )
    )
    monitor.start()
    try:
        for filename in ("10_load_dimensions.sql", "20_load_works.sql"):
            sql, hashes[filename] = render_sql_template(
                sql_dir / filename, database=database, globs=globs
            )
            service.execute_script(sql)
    except BaseException as load_error:
        try:
            monitor.stop()
        except BaseException as monitor_error:
            raise ExceptionGroup(
                "ClickHouse load and storage monitoring both failed",
                [load_error, monitor_error],
            )
        raise
    else:
        storage_samples = monitor.stop()
    write_storage_samples(result_dir / "storage-samples.json", storage_samples)
    gates, query_evidence, distributions = evaluate_stage1(
        service.query_json,
        database=database,
        works_glob=globs["WORKS_GLOB"],
        expected_manifest_rows=expected_rows,
        raw_evidence=raw_evidence,
        minimum_ordinary_author_reference_coverage=(
            minimum_ordinary_author_reference_coverage
        ),
    )
    correctness = write_correctness(
        result_dir / "correctness.json", gates, query_evidence, distributions
    )
    correctness["sql_sha256"] = hashes
    correctness["raw_evidence"] = raw_evidence
    _write_json_atomic(result_dir / "correctness.json", correctness)
    require_all(gates)
    return (
        correctness,
        [asdict(sample) for sample in storage_samples],
        distributions,
    )


def _stage1_seed_work_ids(
    service: ClickHouseService, works_glob: str
) -> tuple[int, int, int]:
    works_glob = validate_raw_glob(works_glob)
    median = int(
        float(
            service.query_value(
                "SELECT quantileExact(0.5)(referenced_works_count) "
                f"FROM file('{works_glob}', Parquet)"
            )
        )
    )
    p95 = int(
        float(
            service.query_value(
                "SELECT quantileExact(0.95)(referenced_works_count) "
                f"FROM file('{works_glob}', Parquet)"
            )
        )
    )

    def nearest(target: int) -> int:
        return int(
            service.query_value(
                "SELECT openalex_numeric_id(id) AS work_id "
                f"FROM file('{works_glob}', Parquet) "
                "WHERE work_id IS NOT NULL "
                f"ORDER BY abs(toInt64(referenced_works_count) - {target}), work_id "
                "LIMIT 1"
            )
        )

    maximum = int(
        service.query_value(
            "SELECT openalex_numeric_id(id) AS work_id "
            f"FROM file('{works_glob}', Parquet) "
            "WHERE work_id IS NOT NULL "
            "ORDER BY referenced_works_count DESC, work_id LIMIT 1"
        )
    )
    return nearest(median), nearest(p95), maximum


def _export_settings(service: ClickHouseService, destination: Path) -> list[dict[str, object]]:
    rows = service.query_json(
        "SELECT name, value, changed, description FROM system.settings "
        "WHERE changed = 1 OR name IN "
        "('max_threads', 'max_memory_usage', 'max_bytes_before_external_group_by', "
        "'max_bytes_before_external_sort', 'join_algorithm') ORDER BY name"
    )
    _write_json_atomic(destination, rows)
    return rows


def command_stage1(args: Namespace) -> int:
    root: Path = args.root
    download_state = _require_state(root, "download-stage1")
    if not args.include_small_dimensions:
        raise PrerequisiteError("stage1 requires --include-small-dimensions")
    if not download_state.get("include_small_dimensions"):
        raise PrerequisiteError("Stage 1 dimensions were not downloaded")
    selection_path = root / ".data" / "selection.json"
    selection = json.loads(selection_path.read_text())
    if selection.get("algorithm") != ALGORITHM:
        raise PrerequisiteError(
            f"selection algorithm is {selection.get('algorithm')!r}; "
            f"rerun select with {ALGORITHM}"
        )
    selection_sha256 = _sha256_path(selection_path)
    if download_state.get("selection_sha256") != selection_sha256:
        raise PrerequisiteError("Stage 1 download does not match the current selection")
    expected_rows = int(selection["tiers"]["stage1"]["record_count"])
    manifest_identities = {}
    for entity in ("works", "institutions"):
        manifest_path = root / ".data" / "manifests" / f"{entity}-manifest.json"
        metadata_path = manifest_path.with_name(f"{manifest_path.name}.metadata.json")
        if not manifest_path.exists() or not metadata_path.exists():
            raise PrerequisiteError(
                f"missing pinned {entity} manifest identity: {manifest_path}"
            )
        manifest_identities[entity] = {
            "date": json.loads(manifest_path.read_text())["date"],
            **json.loads(metadata_path.read_text()),
        }
    run_id = args.run_id or datetime.now(timezone.utc).strftime("stage1-%Y%m%dT%H%M%SZ")
    result_root = root / "results" / run_id
    globs = {
        "WORKS_GLOB": "tiers/stage1/works/*.parquet",
        "INSTITUTIONS_GLOB": "tiers/stage1/institutions/*.parquet",
        "SOURCES_GLOB": "tiers/stage1/sources/*.parquet",
        "TOPICS_GLOB": "tiers/stage1/topics/*.parquet",
    }
    cfg = _config(root)
    service = ClickHouseService(root)
    service.up(memory_gb=32, cpus=cfg.cpus)
    environment = service.write_environment_evidence(
        result_root / "environment.json"
    )
    databases = ("openalex_stage1_a", "openalex_stage1_b")
    builds = []
    build_distributions = []
    all_storage_samples: list[dict[str, object]] = []
    try:
        for database in databases:
            print(f"building isolated database {database}", flush=True)
            correctness, storage_samples, distributions = _build_stage1_database(
                service,
                root=root,
                database=database,
                globs=globs,
                expected_rows=expected_rows,
                result_dir=result_root / database,
                minimum_ordinary_author_reference_coverage=(
                    cfg.thresholds.minimum_ordinary_author_reference_coverage
                ),
            )
            builds.append(correctness)
            build_distributions.append(distributions)
            all_storage_samples.extend(storage_samples)
        hashes = [str(build["normalized_sha256"]) for build in builds]
        rebuild_deterministic = hashes[0] == hashes[1]
        if not rebuild_deterministic:
            raise RuntimeError(f"Stage 1 rebuild hash mismatch: {hashes}")

        seed_work_ids = _stage1_seed_work_ids(service, globs["WORKS_GLOB"])
        catalog = load_query_catalog(root / "sql" / "queries")

        def restart() -> None:
            service.down()
            service.up(memory_gb=32, cpus=cfg.cpus)

        sequential = run_sequential(
            catalog,
            lambda: ServiceBenchmarkClient(service, databases[1]),
            restart,
            cfg.envelopes[32],
            seed_work_ids=seed_work_ids,
        )
        sequential_json = [asdict(record) for record in sequential]
        _write_json_atomic(result_root / "sequential.json", sequential_json)
        settings = _export_settings(service, result_root / "settings.json")
        observed_peak = max(
            (sample["filesystem_bytes"] for sample in all_storage_samples),
            default=0,
        )
        referential = build_distributions[1]["referential_coverage"]
        missing_institution_sample = build_distributions[1][
            "missing_institution_sample"
        ]
        blocking_gates_passed = all(
            bool(gate["passed"]) or not bool(gate["blocking"])
            for gate in builds[1]["gates"]
        )
        limitations = [
            "Stage 1 validates correctness and query execution on a target of approximately 1 GiB; its actual size can exceed that target by one selected file.",
            STAGE1_BIAS_CAVEAT,
            "Stage 1 scaling evidence is not a full-size prediction.",
            "The Docker Desktop VM has 48 GiB; the ClickHouse container is capped at 32 GiB. A 64-GiB Docker VM did not boot on this host.",
            f"Only {referential['retained_cited_edges']} of {referential['citation_edges']} citation edges point to another Work inside this partial sample (retention ratio {float(referential['citation_retention_ratio']):.6f}); this is sampling-induced and is not evidence of citation data loss.",
        ]
        if int(referential["missing_institutions"]) > 0:
            limitations.append(
                f"The canonical Institutions snapshot does not resolve {referential['missing_institutions']} of {referential['institution_bridge_rows']} Work-institution bridge rows ({referential['distinct_missing_institution_ids']} distinct IDs; coverage ratio {float(referential['institution_reference_coverage_ratio']):.6f}). The raw links are preserved and analyses must use LEFT JOIN when unmatched affiliations matter."
            )
        if int(referential["missing_authors"]) > 0:
            limitations.append(
                f"The canonical Authors snapshot does not resolve {referential['missing_authors']} of {referential['author_bridge_rows']} Work-author bridge rows. This includes {referential['null_author_rows']} documented NULL-author rows and {referential['deleted_author_rows']} documented deleted-author rows; ordinary coverage is {float(referential['ordinary_author_reference_coverage_ratio']):.9f} against a blocking floor of {cfg.thresholds.minimum_ordinary_author_reference_coverage:.6f}. The raw links are preserved and analyses must use LEFT JOIN when unmatched authorships matter."
            )
        report_evidence = {
            "run_id": run_id,
            "inputs": {
                "selection_sha256": selection_sha256,
                "selection_algorithm": selection["algorithm"],
                "stage1_coverage_policy": selection["stage1_coverage_policy"],
                "entity_manifests": manifest_identities,
                "expected_work_rows": expected_rows,
                "seed_work_ids": seed_work_ids,
            },
            "environment": environment,
            "settings": settings,
            "correctness": {
                "build_hashes": hashes,
                "rebuild_deterministic": rebuild_deterministic,
                "gates": builds[1]["gates"],
                "raw_evidence": builds[1]["raw_evidence"],
                "referential_coverage": referential,
                "missing_institution_sample": missing_institution_sample,
            },
            "sequential": sequential_json,
            "concurrent": {"status": "not run in Stage 1"},
            "storage": {
                "samples": all_storage_samples,
                "observed_peak_bytes": observed_peak,
                "sampling_note": "Each build records an initial baseline and a forced final sample. Empty initial table_bytes means no active parts existed yet; empty projection_bytes means the SQL scripts executed by this Stage 1 build create no projections.",
            },
            "local_engine_verdict": (
                "pass"
                if blocking_gates_passed and rebuild_deterministic
                else "fail"
            ),
            "capacity_verdict": "Uncertain",
            "limitations": limitations,
        }
        report_json, report_md = render_report(result_root, report_evidence)
        _write_state(
            root,
            "stage1",
            passed=True,
            run_id=run_id,
            databases=list(databases),
            correctness_hash=hashes[0],
            report_json=str(report_json),
            report_md=str(report_md),
        )
        print(f"Stage 1 passed; report: {report_md}", flush=True)
        return 0
    finally:
        service.down()


STAGE2_WORK_TABLES = (
    "citation_edge",
    "work_topic",
    "work_institution",
    "work_author",
    "works",
)


def _stage2_globs(tier: str) -> dict[str, str]:
    return {
        "WORKS_GLOB": f"tiers/{tier}/works/*.parquet",
        "AUTHORS_GLOB": f"tiers/{tier}/authors/*.parquet",
        "INSTITUTIONS_GLOB": f"tiers/{tier}/institutions/*.parquet",
        "SOURCES_GLOB": f"tiers/{tier}/sources/*.parquet",
        "TOPICS_GLOB": f"tiers/{tier}/topics/*.parquet",
    }


def _stage2_database(run_id: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", run_id.lower()).strip("_")
    if not normalized:
        raise ValueError("Stage 2 run ID must contain a letter or number")
    digest = hashlib.sha256(run_id.encode()).hexdigest()[:8]
    return _database_identifier(f"openalex_stage2_{normalized[:24]}_{digest}")


def _stage2_rendered_sql_hashes(
    root: Path, *, database: str, tiers: tuple[str, ...]
) -> dict[str, str]:
    sql_dir = root / "sql"
    hashes = {}
    base_globs = _stage2_globs("stage2_large")
    for filename in (
        "00_schema.sql",
        "11_load_complete_authors.sql",
        "12_load_small_dimensions.sql",
        "30_reverse_projection.sql",
    ):
        _, hashes[filename] = render_sql_template(
            sql_dir / filename, database=database, globs=base_globs
        )
    for tier in tiers:
        globs = _stage2_globs(tier)
        for filename in ("05_raw_evidence.sql", "20_load_works.sql"):
            _, hashes[f"{tier}/{filename}"] = render_sql_template(
                sql_dir / filename, database=database, globs=globs
            )
    return hashes


def _stage2_monitor(
    service: ClickHouseService, *, root: Path, database: str
) -> StorageMonitor:
    sampler = DecimatedFilesystemSampler(
        service.query_json,
        database=database,
        clickhouse_data_dir=root / ".data" / "clickhouse",
        filesystem_interval_seconds=30.0,
    )
    return StorageMonitor(
        sampler,
        interval_seconds=1.0,
        final_sample=sampler.final,
    )


def _prepare_stage2_dimensions(
    service: ClickHouseService,
    *,
    root: Path,
    database: str,
    expected_counts: dict[str, int],
    result_dir: Path,
) -> tuple[dict[str, int], list[dict[str, object]]]:
    globs = _stage2_globs("stage2_large")
    sql_dir = root / "sql"
    service.execute_script(f"DROP DATABASE IF EXISTS {database}")
    schema, _ = render_sql_template(
        sql_dir / "00_schema.sql", database=database, globs=globs
    )
    service.execute_script(schema)
    monitor = _stage2_monitor(service, root=root, database=database)
    monitor.start()
    try:
        for filename in (
            "11_load_complete_authors.sql",
            "12_load_small_dimensions.sql",
        ):
            sql, _ = render_sql_template(
                sql_dir / filename, database=database, globs=globs
            )
            service.execute_script(sql)
    except BaseException as load_error:
        try:
            monitor.stop()
        except BaseException as monitor_error:
            raise ExceptionGroup(
                "Stage 2 dimension load and storage monitoring both failed",
                [load_error, monitor_error],
            )
        raise
    else:
        samples = monitor.stop()
    rows = service.query_json(
        "SELECT "
        f"(SELECT count() FROM {database}.authors) AS authors, "
        f"(SELECT uniqExact(author_id) FROM {database}.authors) AS unique_authors, "
        f"(SELECT count() FROM {database}.institutions) AS institutions, "
        f"(SELECT count() FROM {database}.sources) AS sources, "
        f"(SELECT count() FROM {database}.topics) AS topics"
    )[0]
    counts = {name: int(value) for name, value in rows.items()}
    if counts["authors"] != counts["unique_authors"]:
        raise RuntimeError(f"complete Authors IDs are not unique: {counts}")
    for entity in ("authors", "institutions", "sources", "topics"):
        if counts[entity] != expected_counts[entity]:
            raise RuntimeError(
                f"Stage 2 {entity} row mismatch: "
                f"{counts[entity]} != {expected_counts[entity]}"
            )
    sample_rows = [asdict(sample) for sample in samples]
    write_storage_samples(result_dir / "storage-samples.json", samples)
    _write_json_atomic(result_dir / "counts.json", counts)
    return counts, sample_rows


def _validate_stage2_dimensions(
    service: ClickHouseService,
    *,
    database: str,
    expected_counts: dict[str, int],
) -> None:
    exists = service.query_value(f"SELECT existsDatabase('{database}')")
    if exists != "1":
        raise Stage2PrerequisiteError(
            "resumable Stage 2 database is missing; use an explicit new --run-id"
        )
    rows = service.query_json(
        "SELECT "
        f"(SELECT count() FROM {database}.authors) AS authors, "
        f"(SELECT count() FROM {database}.institutions) AS institutions, "
        f"(SELECT count() FROM {database}.sources) AS sources, "
        f"(SELECT count() FROM {database}.topics) AS topics"
    )[0]
    actual = {name: int(value) for name, value in rows.items()}
    if actual != expected_counts:
        raise Stage2PrerequisiteError(
            f"resumable Stage 2 dimensions changed: {actual} != {expected_counts}; "
            "use an explicit new --run-id"
        )


def _reset_stage2_work_tables(
    service: ClickHouseService, *, database: str
) -> None:
    statements = [
        f"ALTER TABLE {database}.citation_edge DROP PROJECTION IF EXISTS by_cited"
    ]
    statements.extend(
        f"TRUNCATE TABLE {database}.{table}" for table in STAGE2_WORK_TABLES
    )
    service.execute_script(";\n".join(statements) + ";")


def _stage2_profile(
    service: ClickHouseService,
    *,
    database: str,
    works_glob: str,
) -> dict[str, object]:
    works_glob = validate_raw_glob(works_glob)
    coverage = service.query_json(
        "SELECT "
        f"(SELECT count() FROM {database}.works) AS works, "
        f"(SELECT count() FROM {database}.work_author) AS authorships, "
        f"(SELECT uniqExact(author_id) FROM {database}.work_author) AS matched_authors, "
        f"(SELECT count() FROM {database}.authors) AS complete_authors, "
        "if(works = 0, 0., authorships / works) AS authorships_per_work, "
        "if(complete_authors = 0, 0., matched_authors / complete_authors) "
        "AS matched_author_fraction"
    )[0]
    degree = service.query_json(
        "SELECT quantileExact(0.5)(referenced_works_count) AS median, "
        "quantileExact(0.95)(referenced_works_count) AS p95, "
        "max(referenced_works_count) AS maximum "
        f"FROM file('{works_glob}', Parquet)"
    )[0]
    marginals = {}
    expressions = {
        "publication_year": "toString(publication_year)",
        "work_type": "work_type",
        "primary_topic_id": "toString(primary_topic_id)",
        "is_xpac": "toString(is_xpac)",
    }
    for name, expression in expressions.items():
        marginals[name] = service.query_json(
            f"SELECT {expression} AS value, count() AS works "
            f"FROM {database}.works GROUP BY value ORDER BY value"
        )
    return {
        "coverage": coverage,
        "reference_degree": degree,
        "marginals": marginals,
    }


def _load_stage2_tier(
    service: ClickHouseService,
    *,
    root: Path,
    database: str,
    tier: str,
    expected_rows: int,
    result_dir: Path,
    minimum_ordinary_author_reference_coverage: float,
) -> tuple[dict[str, object], dict[str, object], list[dict[str, object]]]:
    globs = _stage2_globs(tier)
    _reset_stage2_work_tables(service, database=database)
    raw_evidence, raw_hash = _raw_evidence(
        service, root / "sql", database, globs
    )
    monitor = _stage2_monitor(service, root=root, database=database)
    monitor.start()
    try:
        works_sql, works_hash = render_sql_template(
            root / "sql" / "20_load_works.sql",
            database=database,
            globs=globs,
        )
        service.execute_script(works_sql)
    except BaseException as load_error:
        try:
            monitor.stop()
        except BaseException as monitor_error:
            raise ExceptionGroup(
                f"{tier} load and storage monitoring both failed",
                [load_error, monitor_error],
            )
        raise
    else:
        samples = monitor.stop()
    write_storage_samples(result_dir / "storage-samples.json", samples)
    gates, query_evidence, distributions = evaluate_stage1(
        service.query_json,
        database=database,
        works_glob=globs["WORKS_GLOB"],
        expected_manifest_rows=expected_rows,
        raw_evidence=raw_evidence,
        minimum_ordinary_author_reference_coverage=(
            minimum_ordinary_author_reference_coverage
        ),
    )
    correctness = write_correctness(
        result_dir / "correctness.json", gates, query_evidence, distributions
    )
    correctness["sql_sha256"] = {
        **raw_hash,
        "20_load_works.sql": works_hash,
    }
    correctness["raw_evidence"] = raw_evidence
    correctness["referential_coverage"] = distributions["referential_coverage"]
    correctness["missing_author_sample"] = distributions["missing_author_sample"]
    correctness["missing_institution_sample"] = distributions[
        "missing_institution_sample"
    ]
    _write_json_atomic(result_dir / "correctness.json", correctness)
    require_all(gates)
    profile = _stage2_profile(
        service,
        database=database,
        works_glob=globs["WORKS_GLOB"],
    )
    _write_json_atomic(result_dir / "profile.json", profile)
    return correctness, profile, [asdict(sample) for sample in samples]


def _projection_catalog(phase: str) -> tuple[BenchmarkQuery, ...]:
    definitions = (
        (
            "incoming",
            "one_hop",
            "SELECT citing_work_id FROM openalex_spike.citation_edge "
            "WHERE cited_work_id = {seed_work_id:UInt64}",
            True,
        ),
        (
            "outgoing",
            "one_hop",
            "SELECT cited_work_id FROM openalex_spike.citation_edge "
            "WHERE citing_work_id = {seed_work_id:UInt64}",
            True,
        ),
        (
            "citations_by_year",
            "routine",
            "SELECT citing_year, cited_work_id, count() AS citations "
            "FROM openalex_spike.citation_edge GROUP BY citing_year, cited_work_id "
            "ORDER BY citations DESC, cited_work_id LIMIT 1000",
            False,
        ),
    )
    return tuple(
        BenchmarkQuery(
            name=f"projection_{phase}_{name}",
            filename=f"projection_{name}.sql",
            query_class=query_class,
            diagnostic=False,
            sql=sql,
            requires_seed=requires_seed,
        )
        for name, query_class, sql, requires_seed in definitions
    )


def _run_projection_experiment(
    service: ClickHouseService,
    *,
    root: Path,
    database: str,
    memory_gib: int,
    seed_work_ids: tuple[int, int, int],
    result_dir: Path,
) -> dict[str, object]:
    cfg = _config(root)

    def restart() -> None:
        service.down()
        service.up(memory_gb=memory_gib, cpus=cfg.cpus)

    client = lambda: ServiceBenchmarkClient(service, database)
    projection_definitions = int(
        service.query_value(
            "SELECT count() FROM system.projections "
            f"WHERE database = '{database}' AND table = 'citation_edge' "
            "AND name = 'by_cited'"
        )
    )
    if projection_definitions != 0:
        raise RuntimeError(
            "projection baseline requires by_cited to be absent before measurement"
        )
    before = run_sequential(
        _projection_catalog("before"),
        client,
        restart,
        cfg.envelopes[memory_gib],
        seed_work_ids=seed_work_ids,
    )
    monitor = _stage2_monitor(service, root=root, database=database)
    monitor.start()
    started = monotonic()
    try:
        projection_sql, projection_hash = render_sql_template(
            root / "sql" / "30_reverse_projection.sql",
            database=database,
            globs=_stage2_globs("stage2_large"),
        )
        service.execute_script(projection_sql)
    except BaseException as projection_error:
        try:
            monitor.stop()
        except BaseException as monitor_error:
            raise ExceptionGroup(
                "projection build and storage monitoring both failed",
                [projection_error, monitor_error],
            )
        raise
    else:
        projection_samples = monitor.stop()
    build_seconds = monotonic() - started
    after = run_sequential(
        _projection_catalog("after"),
        client,
        restart,
        cfg.envelopes[memory_gib],
        seed_work_ids=seed_work_ids,
    )
    write_storage_samples(
        result_dir / "projection-storage-samples.json", projection_samples
    )
    result = {
        "sql_sha256": projection_hash,
        "build_seconds": build_seconds,
        "before": [asdict(record) for record in before],
        "after": [asdict(record) for record in after],
        "storage_samples": [asdict(sample) for sample in projection_samples],
    }
    _write_json_atomic(result_dir / "projection.json", result)
    return result


def _stage2_checkpoint_path(root: Path, run_id: str) -> Path:
    digest = hashlib.sha256(run_id.encode()).hexdigest()[:12]
    return _state_path(root, f"stage2-{digest}")


def _write_stage2_checkpoint(path: Path, document: dict[str, object]) -> None:
    _write_json_atomic(
        path,
        {
            **document,
            "command": "stage2",
            "command_version": COMMAND_VERSION,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
    )


def _finalize_stage2_report(
    *,
    root: Path,
    result_root: Path,
    checkpoint_path: Path,
    checkpoint: dict[str, object],
    run_id: str,
    memory_gib: int,
    tiers: tuple[str, ...],
    cfg: ExperimentConfig,
    selection: dict[str, object],
    selection_sha256: str,
    pin_state: dict[str, object],
    maximum_raw_bytes: int,
    environment: dict[str, object],
    identity: dict[str, object],
    evaluation_mode: str,
    write_derived_logs: bool,
) -> int:
    tier_summaries = {
        tier: json.loads(
            (result_root / checkpoint["tiers"][tier]["summary"]).read_text()
        )
        for tier in tiers
    }
    for tier, summary in tier_summaries.items():
        if int(summary["memory_gib"]) != memory_gib:
            raise Stage2PrerequisiteError(
                f"{tier} summary memory does not match checkpoint identity"
            )

    if write_derived_logs:
        query_log_rows = []
        disk_rows = []
        for tier, summary in tier_summaries.items():
            tier_dir = result_root / "tiers" / f"{tier}-memory{memory_gib}gib"
            query_log_rows.extend(
                json.loads(line)
                for line in (tier_dir / "query-log.jsonl").read_text().splitlines()
                if line
            )
            disk_rows.extend(
                {
                    "tier": tier,
                    "memory_gib": memory_gib,
                    "phase": "load",
                    **sample,
                }
                for sample in summary["storage_samples"]
            )
            if summary["projection"]:
                disk_rows.extend(
                    {
                        "tier": tier,
                        "memory_gib": memory_gib,
                        "phase": "projection",
                        **sample,
                    }
                    for sample in summary["projection"]["storage_samples"]
                )
        _write_jsonl_atomic(result_root / "query-log.jsonl", query_log_rows)
        _write_jsonl_atomic(result_root / "disk-samples.jsonl", disk_rows)

    performance_by_tier = {
        tier: stage2_performance_verdict(summary["concurrent"], cfg.thresholds)
        for tier, summary in tier_summaries.items()
    }
    aggregate_performance = worst_stage2_verdict(
        list(performance_by_tier.values())
    )
    local_verdict = stage2_local_verdict(
        memory_gib=memory_gib,
        performance_verdict=aggregate_performance,
    )
    first_errors = [
        summary["concurrent"]["first_error"]
        for summary in tier_summaries.values()
        if summary["concurrent"]["first_error"]
    ]
    restarted = any(
        summary["concurrent"]["server_restarted"]
        for summary in tier_summaries.values()
    )
    report_evidence = {
        "run_id": run_id,
        "inputs": {
            "selection_sha256": selection_sha256,
            "selection_algorithm": selection["algorithm"],
            "maximum_raw_input_bytes": maximum_raw_bytes,
            "tiers": {
                tier: {
                    "content_length": sum(
                        int(item["content_length"])
                        for item in selection["tiers"][tier]["files"]
                    ),
                    "record_count": int(selection["tiers"][tier]["record_count"]),
                }
                for tier in tiers
            },
            "complete_authors_bytes": int(
                pin_state["entities"]["authors"]["content_length"]
            ),
            "seed_work_ids": list(checkpoint["seed_work_ids"]),
            "run_identity": identity,
        },
        "environment": environment,
        "correctness": {
            tier: summary["correctness"] for tier, summary in tier_summaries.items()
        },
        "sequential": {
            tier: summary["sequential"] for tier, summary in tier_summaries.items()
        },
        "concurrent": {
            tier: summary["concurrent"] for tier, summary in tier_summaries.items()
        },
        "performance": {
            "latency_threshold_seconds": {
                "routine": {
                    "pass": cfg.thresholds.pass_routine_p95_seconds,
                    "conditional": cfg.thresholds.conditional_routine_p95_seconds,
                },
                "join": {
                    "pass": cfg.thresholds.pass_join_p95_seconds,
                    "conditional": cfg.thresholds.conditional_join_p95_seconds,
                },
            },
            "per_tier_verdict": performance_by_tier,
            "aggregate_verdict": aggregate_performance,
            "boundary_semantics": (
                "p95 equal to a ceiling remains in that band; only values above "
                "the ceiling move to the next severity"
            ),
            "undersampling_semantics": (
                "classes below the minimum sample count are excluded from latency "
                "grading and cap the tier at Conditional; nearest-rank p95 is retained"
            ),
            "one_hop_latency_criterion": (
                "not configured; one-hop remains gated for errors and sample count"
            ),
        },
        "verdict_evaluation": {
            "mode": evaluation_mode,
            "source": "SHA-256-pinned completed tier summaries",
        },
        "storage": {
            "dimension_samples": checkpoint["dimension_storage_samples"],
            "tiers": {
                tier: summary["storage_samples"]
                for tier, summary in tier_summaries.items()
            },
            "capacity_model_status": "not yet validated at full corpus scale",
        },
        "profiles": {
            tier: summary["profile"] for tier, summary in tier_summaries.items()
        },
        "projection": tier_summaries.get("stage2_large", {}).get("projection"),
        "errors": {
            "concurrent_first_errors": first_errors,
            "server_restarted": restarted,
        },
        "local_engine_verdict": local_verdict,
        "capacity_verdict": "Uncertain",
        "limitations": [
            f"This local Stage 2 run uses a 32 GiB ClickHouse container because the captured Docker VM exposes only {int(environment['resource_limits']['docker_memory_bytes']) / (1 << 30):.3f} GiB; the 50 GiB acceptance arm is unreachable here and the local verdict is capped at Conditional.",
            "The 50 GiB option requires a different Docker environment with at least 54 GiB configured; no automatic memory downgrade exists.",
            "The OpenAlex manifests publish byte lengths and record counts but no content checksum; verification checks size and Parquet footer row counts and does not claim cryptographic object integrity.",
            "The Works samples are stratified by updated_date and are not a population-representative sample.",
            "Local Apple Silicon and local SSD latency is not extrapolated to an Alliance x86 VM with network-backed storage.",
            "The 50 GiB and Alliance performance envelopes remain unvalidated.",
        ]
        + [
            f"{tier}: the canonical Authors snapshot leaves {summary['correctness']['referential_coverage']['missing_authors']} of {summary['correctness']['referential_coverage']['author_bridge_rows']} Work-author bridge rows unresolved, including {summary['correctness']['referential_coverage']['null_author_rows']} documented NULL-author rows and {summary['correctness']['referential_coverage']['deleted_author_rows']} documented deleted-author rows. The ordinary unresolved count is {summary['correctness']['referential_coverage']['ordinary_missing_author_rows']} of {summary['correctness']['referential_coverage']['ordinary_authorship_rows']} (coverage {float(summary['correctness']['referential_coverage']['ordinary_author_reference_coverage_ratio']):.10f}; blocking floor {cfg.thresholds.minimum_ordinary_author_reference_coverage:.6f}). Raw links are preserved; use LEFT JOIN when unmatched authorships matter."
            for tier, summary in tier_summaries.items()
            if int(summary["correctness"]["referential_coverage"]["missing_authors"])
            > 0
        ],
    }
    report_json, report_md = render_report(result_root, report_evidence)
    checkpoint["status"] = "complete"
    checkpoint["report_json"] = str(report_json)
    checkpoint["report_md"] = str(report_md)
    _write_stage2_checkpoint(checkpoint_path, checkpoint)
    _write_state(
        root,
        "stage2",
        passed=local_verdict != "fail",
        run_id=run_id,
        memory_gib=memory_gib,
        report_json=str(report_json),
        report_md=str(report_md),
        checkpoint=str(checkpoint_path),
    )
    print(f"Stage 2 complete; report: {report_md}", flush=True)
    return 0


def command_stage2(args: Namespace) -> int:
    root: Path = args.root
    stage1_state = _require_state(root, "stage1")
    if not stage1_state.get("passed"):
        raise PrerequisiteError("Stage 2 requires a passing Stage 1 state")
    cfg = _config(root)
    run_id = args.run_id or "stage2"
    checkpoint_path = _stage2_checkpoint_path(root, run_id)
    report_only_checkpoint = None
    if args.report_only:
        if not checkpoint_path.exists():
            raise Stage2PrerequisiteError(
                f"missing Stage 2 checkpoint for report-only: {checkpoint_path}"
            )
        report_only_checkpoint = json.loads(checkpoint_path.read_text())
        memory_gib = int(report_only_checkpoint["identity"]["memory_gib"])
        tiers = tuple(str(tier) for tier in report_only_checkpoint["identity"]["tiers"])
        if args.memory_gb is not None and int(args.memory_gb) != memory_gib:
            raise Stage2PrerequisiteError(
                "report-only memory must match the checkpoint identity"
            )
        if args.tier is not None and (args.tier,) != tiers:
            raise Stage2PrerequisiteError(
                "report-only tiers must match the checkpoint identity"
            )
    else:
        memory_gib = int(args.memory_gb or 32)
        tiers = (args.tier,) if args.tier else STAGE2_TIERS
    if memory_gib not in cfg.envelopes:
        raise PrerequisiteError(
            f"Stage 2 memory envelope must be one of {sorted(cfg.envelopes)} GiB"
        )
    database = _stage2_database(run_id)
    selection_path = root / ".data" / "selection.json"
    selection = json.loads(selection_path.read_text())
    selection_sha256 = file_sha256(selection_path)
    download_path = _state_path(root, "download-stage2_large")
    download_state = _require_state(root, "download-stage2_large")
    if not download_state.get("include_complete_authors"):
        raise PrerequisiteError("Stage 2 requires complete Authors")
    if not download_state.get("include_small_dimensions"):
        raise PrerequisiteError("Stage 2 requires the approved small dimensions")
    if download_state.get("selection_sha256") != selection_sha256:
        raise PrerequisiteError("Stage 2 download does not match the selection")
    expected_groups = {
        f"{tier}/{entity}"
        for tier in STAGE2_TIERS
        for entity in ("works", "authors", *SELECTED_SMALL_ENTITIES)
    }
    if not expected_groups <= set(download_state.get("groups", {})):
        raise PrerequisiteError(
            "Stage 2 maximum download was not materialized into every nested tier"
        )
    pin_state = _require_state(root, "pin-manifests")
    maximum_raw_bytes = maximum_input_bytes(selection, pin_state)
    if not args.report_only:
        required = required_build_free_bytes(
            maximum_raw_input_bytes=maximum_raw_bytes
        )
        available = require_free_space(
            root,
            required_bytes=required,
            purpose="the Stage 2 ClickHouse build",
        )
        print(
            f"Stage 2 disk preflight passed: {available:,} bytes free; "
            f"conservative requirement {required:,} bytes",
            flush=True,
        )
    rendered_hashes = _stage2_rendered_sql_hashes(
        root, database=database, tiers=tiers
    )
    identity = build_run_identity(
        run_id=run_id,
        memory_gib=memory_gib,
        tiers=tiers,
        selection_sha256=selection_sha256,
        download_state_sha256=file_sha256(download_path),
        config_sha256=file_sha256(root / "config" / "experiment.toml"),
        rendered_sql_sha256=rendered_hashes,
    )
    result_root = root / "results" / run_id
    if report_only_checkpoint is not None:
        checkpoint = report_only_checkpoint
    elif checkpoint_path.exists():
        checkpoint = json.loads(checkpoint_path.read_text())
    else:
        checkpoint = {
            "identity": identity,
            "database": database,
            "dimensions_complete": False,
            "completed_tiers": [],
            "tiers": {},
            "status": "in_progress",
        }
    require_resume_identity(checkpoint["identity"], identity)
    if checkpoint["database"] != database:
        raise Stage2PrerequisiteError("Stage 2 checkpoint database changed")
    for tier in checkpoint["completed_tiers"]:
        verify_artifact_hashes(
            checkpoint["tiers"][tier]["artifact_sha256"], root=result_root
        )
    if args.report_only:
        if checkpoint.get("status") != "complete":
            raise Stage2PrerequisiteError(
                "report-only requires a complete Stage 2 checkpoint"
            )
        if set(checkpoint["completed_tiers"]) != set(tiers):
            raise Stage2PrerequisiteError(
                "report-only requires every checkpoint identity tier to be complete"
            )
        environment_path = result_root / "environment.json"
        if not environment_path.exists():
            raise Stage2PrerequisiteError(
                f"report-only is missing environment evidence: {environment_path}"
            )
        return _finalize_stage2_report(
            root=root,
            result_root=result_root,
            checkpoint_path=checkpoint_path,
            checkpoint=checkpoint,
            run_id=run_id,
            memory_gib=memory_gib,
            tiers=tiers,
            cfg=cfg,
            selection=selection,
            selection_sha256=selection_sha256,
            pin_state=pin_state,
            maximum_raw_bytes=maximum_raw_bytes,
            environment=json.loads(environment_path.read_text()),
            identity=identity,
            evaluation_mode="postprocessed_from_sha256_pinned_tier_artifacts",
            write_derived_logs=False,
        )

    expected_dimension_counts = {
        entity: int(pin_state["entities"][entity]["record_count"])
        for entity in ("authors", "institutions", "sources", "topics")
    }
    service = ClickHouseService(root)
    service.up(memory_gb=memory_gib, cpus=cfg.cpus)
    environment = service.write_environment_evidence(
        result_root / "environment.json"
    )
    try:
        if checkpoint["dimensions_complete"]:
            _validate_stage2_dimensions(
                service,
                database=database,
                expected_counts=checkpoint["dimension_counts"],
            )
        else:
            counts, samples = _prepare_stage2_dimensions(
                service,
                root=root,
                database=database,
                expected_counts=expected_dimension_counts,
                result_dir=result_root / "dimensions",
            )
            checkpoint["dimensions_complete"] = True
            checkpoint["dimension_counts"] = {
                name: counts[name] for name in expected_dimension_counts
            }
            checkpoint["dimension_storage_samples"] = samples
            _write_stage2_checkpoint(checkpoint_path, checkpoint)

        if "seed_work_ids" not in checkpoint:
            checkpoint["seed_work_ids"] = list(
                _stage1_seed_work_ids(
                    service, _stage2_globs("stage2_small")["WORKS_GLOB"]
                )
            )
            _write_stage2_checkpoint(checkpoint_path, checkpoint)
        seed_work_ids = tuple(int(value) for value in checkpoint["seed_work_ids"])
        catalog = load_query_catalog(root / "sql" / "queries")

        for tier in tiers:
            if tier in checkpoint["completed_tiers"]:
                print(f"resuming after completed tier {tier}", flush=True)
                continue
            tier_dir = result_root / "tiers" / f"{tier}-memory{memory_gib}gib"
            expected_rows = int(selection["tiers"][tier]["record_count"])
            print(
                f"building {tier}: {expected_rows:,} Works at {memory_gib} GiB",
                flush=True,
            )
            correctness, profile, storage_samples = _load_stage2_tier(
                service,
                root=root,
                database=database,
                tier=tier,
                expected_rows=expected_rows,
                result_dir=tier_dir,
                minimum_ordinary_author_reference_coverage=(
                    cfg.thresholds.minimum_ordinary_author_reference_coverage
                ),
            )

            def restart() -> None:
                service.down()
                service.up(memory_gb=memory_gib, cpus=cfg.cpus)

            sequential = run_sequential(
                catalog,
                lambda: ServiceBenchmarkClient(service, database),
                restart,
                cfg.envelopes[memory_gib],
                seed_work_ids=seed_work_ids,
            )
            sequential_rows = [asdict(record) for record in sequential]
            _write_json_atomic(tier_dir / "sequential.json", sequential_rows)
            restart()
            container_before = service.container_id()
            concurrent_records, first_error = run_closed_loop(
                catalog,
                lambda _: ServiceBenchmarkClient(service, database),
                cfg.envelopes[memory_gib],
                seed_work_ids=seed_work_ids,
                minimum_samples=cfg.thresholds.minimum_samples,
                maximum_seconds=cfg.thresholds.maximum_seconds,
            )
            container_after = service.container_id()
            server_restarted = container_before != container_after
            concurrent_summary = summarize_concurrency(
                concurrent_records,
                minimum_samples=cfg.thresholds.minimum_samples,
                first_error=first_error,
            )
            concurrent_summary["server_restarted"] = server_restarted
            concurrent_rows = [asdict(record) for record in concurrent_records]
            _write_json_atomic(tier_dir / "concurrent-summary.json", concurrent_summary)
            query_rows = [
                {"tier": tier, "memory_gib": memory_gib, "mode": "sequential", **row}
                for row in sequential_rows
            ] + [
                {"tier": tier, "memory_gib": memory_gib, "mode": "concurrent", **row}
                for row in concurrent_rows
            ]
            projection = None
            if tier == "stage2_large":
                projection = _run_projection_experiment(
                    service,
                    root=root,
                    database=database,
                    memory_gib=memory_gib,
                    seed_work_ids=seed_work_ids,
                    result_dir=tier_dir,
                )
                query_rows.extend(
                    {
                        "tier": tier,
                        "memory_gib": memory_gib,
                        "mode": "projection_before",
                        **row,
                    }
                    for row in projection["before"]
                )
                query_rows.extend(
                    {
                        "tier": tier,
                        "memory_gib": memory_gib,
                        "mode": "projection_after",
                        **row,
                    }
                    for row in projection["after"]
                )
            _write_jsonl_atomic(tier_dir / "query-log.jsonl", query_rows)
            performance_verdict = stage2_performance_verdict(
                concurrent_summary, cfg.thresholds
            )
            tier_summary = {
                "tier": tier,
                "memory_gib": memory_gib,
                "expected_work_rows": expected_rows,
                "correctness": correctness,
                "profile": profile,
                "sequential": sequential_rows,
                "concurrent": concurrent_summary,
                "performance_verdict": performance_verdict,
                "storage_samples": storage_samples,
                "projection": projection,
                "local_verdict": stage2_local_verdict(
                    memory_gib=memory_gib,
                    performance_verdict=performance_verdict,
                ),
            }
            summary_path = tier_dir / "summary.json"
            _write_json_atomic(summary_path, tier_summary)
            artifacts = [
                path
                for path in tier_dir.iterdir()
                if path.is_file()
            ]
            checkpoint["tiers"][tier] = {
                "summary": str(summary_path.relative_to(result_root)),
                "artifact_sha256": artifact_hashes(artifacts, root=result_root),
            }
            checkpoint["completed_tiers"].append(tier)
            _write_stage2_checkpoint(checkpoint_path, checkpoint)

        return _finalize_stage2_report(
            root=root,
            result_root=result_root,
            checkpoint_path=checkpoint_path,
            checkpoint=checkpoint,
            run_id=run_id,
            memory_gib=memory_gib,
            tiers=tiers,
            cfg=cfg,
            selection=selection,
            selection_sha256=selection_sha256,
            pin_state=pin_state,
            maximum_raw_bytes=maximum_raw_bytes,
            environment=environment,
            identity=identity,
            evaluation_mode="in_run",
            write_derived_logs=True,
        )

    finally:
        service.down()


def command_report(args: Namespace) -> int:
    if args.run:
        report = args.root / "results" / args.run / "report.md"
        if not report.exists():
            raise PrerequisiteError(f"missing report: {report}")
        print(report)
        return 0
    state = _require_state(args.root, "stage1")
    print(state["report_md"])
    return 0


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="openalex-spike")
    parser.add_argument("--root", type=Path, default=_project_root())
    subparsers = parser.add_subparsers(dest="command", required=True)

    pin = subparsers.add_parser("pin-manifests")
    pin.set_defaults(handler=command_pin_manifests)
    select = subparsers.add_parser("select")
    select.set_defaults(handler=command_select)
    download = subparsers.add_parser("download")
    download.add_argument("--tier", required=True, choices=("stage1", "stage2_small", "stage2_medium", "stage2_large"))
    download.add_argument("--include-complete-authors", action="store_true")
    download.add_argument("--include-small-dimensions", action="store_true")
    download.set_defaults(handler=command_download)
    up = subparsers.add_parser("clickhouse-up")
    up.add_argument("--memory-gb", type=int, default=32)
    up.add_argument("--cpus", type=int, default=16)
    up.set_defaults(handler=command_clickhouse_up)
    stage1 = subparsers.add_parser("stage1")
    stage1.add_argument("--include-small-dimensions", action="store_true")
    stage1.add_argument("--run-id")
    stage1.set_defaults(handler=command_stage1)
    stage2 = subparsers.add_parser("stage2")
    stage2.add_argument(
        "--memory-gb",
        type=int,
        choices=(32, 50),
        default=None,
        help="ClickHouse container limit in GiB (compatibility flag spelling)",
    )
    stage2.add_argument("--tier", choices=STAGE2_TIERS)
    stage2.add_argument("--run-id")
    stage2.add_argument("--report-only", action="store_true")
    stage2.set_defaults(handler=command_stage2)
    report = subparsers.add_parser("report")
    report.add_argument("--run")
    report.set_defaults(handler=command_report)
    down = subparsers.add_parser("clickhouse-down")
    down.set_defaults(handler=command_clickhouse_down)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except (
        PrerequisiteError,
        ResourcePreflightError,
        Stage2PrerequisiteError,
        ValueError,
    ) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
