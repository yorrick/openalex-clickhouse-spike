from argparse import Namespace
from pathlib import Path
import hashlib
import json

import pytest

from openalex_spike.cli import (
    LEGACY_STAGE2_EXECUTION,
    PrerequisiteError,
    STAGE2_TELEMETRY_SCHEMA_VERSION,
    Stage2Execution,
    _require_no_foreign_merge_activity,
    _resolve_stage2_execution,
    _selected_tier,
    _stage2_merge_activity_payload,
    _stage2_storage_payload,
    _validate_stage2_dimensions,
    build_parser,
    command_stage1,
    main,
    validate_raw_glob,
)
from openalex_spike.clickhouse import ResourcePreflightError
from openalex_spike.config import ExperimentConfig
from openalex_spike.sampling import ALGORITHM
from openalex_spike.stage2 import Stage2PrerequisiteError


def test_cli_exposes_exact_pipeline_commands_and_download_flags():
    parser = build_parser()
    subparsers = next(
        action for action in parser._actions if action.dest == "command"
    )
    assert set(subparsers.choices) == {
        "pin-manifests",
        "select",
        "download",
        "clickhouse-up",
        "stage1",
        "stage2",
        "report",
        "clickhouse-down",
    }
    download = subparsers.choices["download"]
    options = {option for action in download._actions for option in action.option_strings}
    assert {
        "--tier",
        "--include-complete-authors",
        "--include-small-dimensions",
    } <= options
    stage2 = subparsers.choices["stage2"]
    stage2_options = {
        option for action in stage2._actions for option in action.option_strings
    }
    assert {
        "--memory-gb",
        "--tier",
        "--run-id",
        "--cpus",
        "--workers",
        "--query-threads",
        "--maximum-seconds",
    } <= stage2_options


def test_v2_storage_payload_normalizes_mixed_provenance_samples():
    old_sample = {
        "timestamp": 1.0,
        "table_bytes": {},
        "projection_bytes": {},
        "filesystem_bytes": 10,
    }
    new_sample = {**old_sample, "filesystem_vanished_files": 2}
    checkpoint = {"dimension_storage_samples": [old_sample]}
    summaries = {
        "stage2_small": {"storage_samples": [new_sample], "projection": None},
        "stage2_large": {
            "storage_samples": [new_sample],
            "projection": {"storage_samples": [old_sample]},
        },
    }

    payload = _stage2_storage_payload(
        checkpoint,
        summaries,
        legacy_identity=False,
    )

    populations = [
        payload["storage"]["dimension_samples"],
        *payload["storage"]["tiers"].values(),
        payload["projection"]["storage_samples"],
    ]
    assert all(
        "filesystem_vanished_files" in sample
        for population in populations
        for sample in population
    )
    assert all(
        "filesystem_vanished_directories" in sample
        for population in populations
        for sample in population
    )
    assert payload["storage"]["dimension_samples"][0][
        "filesystem_vanished_files"
    ] == 0
    assert payload["storage"]["dimension_samples"][0][
        "filesystem_vanished_directories"
    ] == 0
    assert payload["storage"]["tiers"]["stage2_small"][0][
        "filesystem_vanished_files"
    ] == 2


def test_legacy_storage_payload_preserves_original_sample_shape():
    sample = {
        "timestamp": 1.0,
        "table_bytes": {},
        "projection_bytes": {},
        "filesystem_bytes": 10,
    }
    checkpoint = {"dimension_storage_samples": [sample]}
    summaries = {
        "stage2_large": {
            "storage_samples": [sample],
            "projection": {"storage_samples": [sample]},
        }
    }

    payload = _stage2_storage_payload(
        checkpoint,
        summaries,
        legacy_identity=True,
    )

    assert payload["storage"]["dimension_samples"] == [sample]
    assert payload["storage"]["tiers"]["stage2_large"] == [sample]
    assert payload["projection"]["storage_samples"] == [sample]


def test_merge_activity_payload_preserves_legacy_and_rejects_mixed_schemas():
    legacy_summaries = {
        "stage2_small": {},
        "stage2_medium": {},
    }
    assert _stage2_merge_activity_payload({}, legacy_summaries) is None

    with pytest.raises(Stage2PrerequisiteError, match="mix telemetry schemas"):
        _stage2_merge_activity_payload(
            {},
            {
                "stage2_small": {"merge_activity": {"status": "complete"}},
                "stage2_medium": {},
            },
        )

    with pytest.raises(Stage2PrerequisiteError, match="evidence is missing"):
        _stage2_merge_activity_payload(
            {"telemetry_schema_version": STAGE2_TELEMETRY_SCHEMA_VERSION},
            legacy_summaries,
        )

    assert _stage2_merge_activity_payload(
        {"telemetry_schema_version": STAGE2_TELEMETRY_SCHEMA_VERSION},
        {
            "stage2_small": {"merge_activity": {"status": "complete"}},
            "stage2_medium": {"merge_activity": {"status": "complete"}},
        },
    ) == {
        "stage2_small": {"status": "complete"},
        "stage2_medium": {"status": "complete"},
    }


def test_foreign_merge_activity_is_a_hard_experiment_failure():
    _require_no_foreign_merge_activity(
        {
            "completed_foreign_merge_count": 0,
            "in_flight_foreign_merge_count": 0,
            "foreign_databases": [],
        }
    )

    with pytest.raises(Stage2PrerequisiteError, match="foreign database merge"):
        _require_no_foreign_merge_activity(
            {
                "completed_foreign_merge_count": 1,
                "in_flight_foreign_merge_count": 0,
                "foreign_databases": ["openalex_stage2_prior"],
            }
        )


def test_resume_dimension_validation_uses_supported_database_catalog_query():
    class Service:
        def __init__(self):
            self.existence_sql = ""

        def query_value(self, sql):
            self.existence_sql = sql
            return "1"

        def query_json(self, sql):
            return [
                {
                    "authors": 4,
                    "institutions": 3,
                    "sources": 2,
                    "topics": 1,
                }
            ]

    service = Service()

    _validate_stage2_dimensions(
        service,
        database="openalex_stage2_resume_12345678",
        expected_counts={
            "authors": 4,
            "institutions": 3,
            "sources": 2,
            "topics": 1,
        },
    )

    assert service.existence_sql == (
        "SELECT count() FROM system.databases "
        "WHERE name = 'openalex_stage2_resume_12345678'"
    )
    assert "existsDatabase" not in service.existence_sql


def test_resume_dimension_validation_fails_closed_for_missing_database():
    class Service:
        def query_value(self, sql):
            return "0"

        def query_json(self, sql):
            raise AssertionError("dimension tables must not be read")

    with pytest.raises(Stage2PrerequisiteError, match="database is missing"):
        _validate_stage2_dimensions(
            Service(),
            database="openalex_stage2_missing_12345678",
            expected_counts={},
        )


def test_resume_dimension_validation_rejects_unsafe_database_identifier():
    class Service:
        def query_value(self, sql):
            raise AssertionError("unsafe identifier must fail before SQL")

    with pytest.raises(ValueError, match="invalid database identifier"):
        _validate_stage2_dimensions(
            Service(),
            database="openalex_stage2_x' OR 1=1",
            expected_counts={},
        )


def test_missing_select_prerequisite_returns_nonzero(tmp_path: Path):
    assert main(["--root", str(tmp_path), "select"]) != 0


def _execution_config() -> ExperimentConfig:
    return ExperimentConfig.load(Path("config/experiment.toml"))


def test_legacy_stage2_checkpoint_rejects_new_execution_options():
    checkpoint = {"identity": {"run_id": "legacy"}}
    args = Namespace(
        cpus=16,
        workers=None,
        query_threads=None,
        maximum_seconds=None,
        report_only=True,
    )

    with pytest.raises(Stage2PrerequisiteError, match="legacy Stage 2 checkpoints"):
        _resolve_stage2_execution(args, _execution_config(), checkpoint)


@pytest.mark.parametrize("report_only", [False, True])
def test_v2_resume_reads_execution_from_checkpoint_and_checks_overrides(
    report_only: bool,
):
    execution = Stage2Execution(16, 1, 8, 18_000)
    checkpoint = {
        "identity": {
            "identity_version": 2,
            "execution": {
                "cpus": execution.cpus,
                "workers": execution.workers,
                "query_threads": execution.query_threads,
                "maximum_seconds": execution.maximum_seconds,
            },
        }
    }
    args = Namespace(
        cpus=None,
        workers=None,
        query_threads=None,
        maximum_seconds=None,
        report_only=report_only,
    )

    assert _resolve_stage2_execution(args, _execution_config(), checkpoint) == (
        execution,
        False,
    )
    args.workers = 3
    with pytest.raises(Stage2PrerequisiteError, match="do not match"):
        _resolve_stage2_execution(args, _execution_config(), checkpoint)


def test_fresh_stage2_defaults_create_a_v2_execution():
    args = Namespace(
        cpus=None,
        workers=None,
        query_threads=None,
        maximum_seconds=None,
        report_only=False,
    )

    execution, legacy = _resolve_stage2_execution(
        args, _execution_config(), None
    )
    assert execution == LEGACY_STAGE2_EXECUTION
    assert legacy is False


def test_selected_tier_rejects_stale_algorithm(tmp_path: Path):
    data = tmp_path / ".data"
    data.mkdir()
    (data / "selection.json").write_text(
        json.dumps({"algorithm": "cumulative-bytes-four-strata-v1", "tiers": {}})
    )

    with pytest.raises(PrerequisiteError, match="rerun select"):
        _selected_tier(tmp_path, "stage1")


def test_stage1_rejects_download_from_different_selection(tmp_path: Path):
    data = tmp_path / ".data"
    state = data / "state"
    state.mkdir(parents=True)
    selection_path = data / "selection.json"
    selection_path.write_text(
        json.dumps(
            {
                "algorithm": ALGORITHM,
                "stage1_coverage_policy": {},
                "tiers": {"stage1": {"record_count": 1}},
            }
        )
    )
    current_sha256 = hashlib.sha256(selection_path.read_bytes()).hexdigest()
    assert current_sha256 != "stale"
    (state / "download-stage1.json").write_text(
        json.dumps({"include_small_dimensions": True, "selection_sha256": "stale"})
    )

    with pytest.raises(PrerequisiteError, match="does not match"):
        command_stage1(
            Namespace(
                root=tmp_path,
                include_small_dimensions=True,
                run_id="test",
            )
        )


def test_stage1_requires_manifest_identities_before_build(tmp_path: Path):
    data = tmp_path / ".data"
    state = data / "state"
    state.mkdir(parents=True)
    selection_path = data / "selection.json"
    selection_path.write_text(
        json.dumps(
            {
                "algorithm": ALGORITHM,
                "stage1_coverage_policy": {},
                "tiers": {"stage1": {"record_count": 1}},
            }
        )
    )
    selection_sha256 = hashlib.sha256(selection_path.read_bytes()).hexdigest()
    (state / "download-stage1.json").write_text(
        json.dumps(
            {
                "include_small_dimensions": True,
                "selection_sha256": selection_sha256,
            }
        )
    )

    with pytest.raises(PrerequisiteError, match="missing pinned works manifest"):
        command_stage1(
            Namespace(
                root=tmp_path,
                include_small_dimensions=True,
                run_id="test",
            )
        )


def test_raw_glob_validation_rejects_escape_quotes_and_alternate_roots():
    assert validate_raw_glob("tiers/stage1/works/*.parquet") == (
        "tiers/stage1/works/*.parquet"
    )
    for invalid in (
        "../works/*.parquet",
        "/tmp/works/*.parquet",
        "other/stage1/*.parquet",
        "tiers/stage1/wo'rks/*.parquet",
    ):
        try:
            validate_raw_glob(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(f"accepted unsafe glob: {invalid}")


def test_memory_preflight_is_a_clean_cli_error(tmp_path, monkeypatch, capsys):
    class RefusingService:
        def __init__(self, root):
            pass

        def up(self, *, memory_gb, cpus):
            raise ResourcePreflightError("memory refused without fallback")

    monkeypatch.setattr("openalex_spike.cli.ClickHouseService", RefusingService)

    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "clickhouse-up",
                "--memory-gb",
                "50",
            ]
        )
        == 2
    )
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "error: memory refused without fallback\n"
