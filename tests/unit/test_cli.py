from argparse import Namespace
from pathlib import Path
import hashlib
import json

import pytest

from openalex_spike.cli import (
    PrerequisiteError,
    _selected_tier,
    build_parser,
    command_stage1,
    main,
    validate_raw_glob,
)
from openalex_spike.sampling import ALGORITHM


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


def test_missing_select_prerequisite_returns_nonzero(tmp_path: Path):
    assert main(["--root", str(tmp_path), "select"]) != 0


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
