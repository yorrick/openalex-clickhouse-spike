import json

import pytest

from openalex_spike.sampling import ALGORITHM, select_nested, write_selection


def test_selection_is_deterministic_and_nested(works_manifest):
    targets = {
        "stage1": 1_000,
        "stage2_small": 3_000,
        "stage2_medium": 6_000,
        "stage2_large": 9_000,
    }
    first = select_nested(works_manifest.files, targets, "fixed-seed")
    second = select_nested(works_manifest.files, targets, "fixed-seed")
    assert first == second
    assert set(first["stage1"]) <= set(first["stage2_small"])
    assert set(first["stage2_small"]) <= set(first["stage2_medium"])
    assert set(first["stage2_medium"]) <= set(first["stage2_large"])
    assert {entry.stratum for entry in first["stage1"]} == {0, 1, 2, 3}


def test_stage1_coverage_holds_across_many_seeds(works_manifest):
    targets = {"stage1": 1_000, "stage2_small": 3_000}
    for seed_number in range(60):
        selection = select_nested(works_manifest.files, targets, f"seed-{seed_number}")
        assert {entry.stratum for entry in selection["stage1"]} == {0, 1, 2, 3}
        assert sum(entry.content_length for entry in selection["stage1"]) == 1_000


def test_stage1_fails_when_a_stratum_has_no_file_under_coverage_cap(works_manifest):
    with pytest.raises(ValueError, match="has no file at or below"):
        select_nested(works_manifest.files, {"stage1": 100}, "fixed-seed")


def test_selection_document_is_byte_deterministic(tmp_path, works_manifest):
    targets = {
        "stage1": 1_000,
        "stage2_small": 3_000,
        "stage2_medium": 6_000,
        "stage2_large": 9_000,
    }
    selection = select_nested(works_manifest.files, targets, "fixed-seed")
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    write_selection(
        first,
        selection,
        targets,
        "fixed-seed",
        '"etag"',
        "abc123",
        works_manifest.files,
    )
    write_selection(
        second,
        selection,
        targets,
        "fixed-seed",
        '"etag"',
        "abc123",
        works_manifest.files,
    )
    assert first.read_bytes() == second.read_bytes()
    document = json.loads(first.read_text())
    assert document["algorithm"] == ALGORITHM
    policy = document["stage1_coverage_policy"]
    assert policy["max_seed_file_bytes"] == 250
    assert {values["eligible_files"] for values in policy["strata"].values()} == {1}
    assert "not a representative performance sample" in policy["bias_caveat"]
