from pathlib import Path

from openalex_spike.cli import build_parser, main, validate_raw_glob


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
