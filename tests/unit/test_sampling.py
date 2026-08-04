from openalex_spike.sampling import select_nested, write_selection


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
    write_selection(first, selection, targets, "fixed-seed", '"etag"', "abc123")
    write_selection(second, selection, targets, "fixed-seed", '"etag"', "abc123")
    assert first.read_bytes() == second.read_bytes()
