from __future__ import annotations

from argparse import ArgumentParser, Namespace
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import re
import sys

from openalex_spike.benchmark import (
    ServiceBenchmarkClient,
    load_query_catalog,
    run_sequential,
)
from openalex_spike.clickhouse import ClickHouseService
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
    StorageMonitor,
    collect_storage_sample,
    write_storage_samples,
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
    works_files = _selected_tier(root, tier)
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
    print(
        f"downloading/verifying {len(all_files)} selected files "
        f"({sum(file.content_length for file in all_files):,} bytes)",
        flush=True,
    )
    raw_root = root / ".data" / "raw"
    object_paths = download_files(all_files, raw_root / "objects")
    groups: dict[str, list] = {f"{tier}/works": works_files}
    for entity in sorted(required_entities):
        groups[f"{tier}/{entity}"] = list(manifests[entity].files)
    verification_path = root / ".data" / f"download-verification-{tier}.json"
    verification = verify_downloads(groups, object_paths, verification_path)
    materialize_tier_links(
        raw_root,
        {tier: works_files},
        object_paths,
        entity="works",
    )
    materialize_supporting_entities(
        raw_root,
        [tier],
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
) -> tuple[dict[str, object], list[dict[str, object]]]:
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
    finally:
        storage_samples = monitor.stop()
    write_storage_samples(result_dir / "storage-samples.json", storage_samples)
    gates, query_evidence, distributions = evaluate_stage1(
        service.query_json,
        database=database,
        works_glob=globs["WORKS_GLOB"],
        expected_manifest_rows=expected_rows,
        raw_evidence=raw_evidence,
    )
    correctness = write_correctness(
        result_dir / "correctness.json", gates, query_evidence, distributions
    )
    correctness["sql_sha256"] = hashes
    correctness["raw_evidence"] = raw_evidence
    _write_json_atomic(result_dir / "correctness.json", correctness)
    require_all(gates)
    return correctness, [asdict(sample) for sample in storage_samples]


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
    all_storage_samples: list[dict[str, object]] = []
    try:
        for database in databases:
            print(f"building isolated database {database}", flush=True)
            correctness, storage_samples = _build_stage1_database(
                service,
                root=root,
                database=database,
                globs=globs,
                expected_rows=expected_rows,
                result_dir=result_root / database,
            )
            builds.append(correctness)
            all_storage_samples.extend(storage_samples)
        hashes = [str(build["normalized_sha256"]) for build in builds]
        if hashes[0] != hashes[1]:
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
        referential = builds[1]["distributions"]["referential_coverage"]
        missing_institution_sample = builds[1]["distributions"][
            "missing_institution_sample"
        ]
        limitations = [
            "Stage 1 validates correctness and query execution on a target of approximately 1 GiB; its actual size can exceed that target by one selected file.",
            STAGE1_BIAS_CAVEAT,
            "Stage 1 scaling evidence is not a full-size prediction.",
            "The Docker VM uses 48 GiB because 64 GiB did not boot on this host.",
        ]
        if int(referential["missing_institutions"]) > 0:
            limitations.append(
                f"The canonical Institutions snapshot does not resolve {referential['missing_institutions']} of {referential['institution_bridge_rows']} Work-institution bridge rows ({referential['distinct_missing_institution_ids']} distinct IDs; coverage ratio {float(referential['institution_reference_coverage_ratio']):.6f}). The raw links are preserved and analyses must use LEFT JOIN when unmatched affiliations matter."
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
                "rebuild_deterministic": True,
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
            },
            "local_engine_verdict": "pass",
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


def command_stage2(args: Namespace) -> int:
    state = _require_state(args.root, "stage1")
    if not state.get("passed"):
        raise PrerequisiteError("Stage 2 requires a passing Stage 1 state")
    raise PrerequisiteError("Stage 2 execution is not part of the current Stage 1 run")


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
    except (PrerequisiteError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
