import json

import pytest

from openalex_spike.correctness import (
    CorrectnessFailure,
    GateResult,
    QueryEvidence,
    canonical_result_hash,
    evaluate_stage1,
    require_all,
    write_correctness,
)


def test_require_all_names_failed_gate_and_expected_actual_values():
    results = [
        GateResult("rows", True, 2, 2, {}),
        GateResult("references", False, 3, 2, {"query_sha256": "abc"}),
    ]
    with pytest.raises(CorrectnessFailure) as captured:
        require_all(results)
    payload = json.loads(str(captured.value))
    assert payload["failures"][0]["name"] == "references"
    assert payload["failures"][0]["expected"] == 3
    assert payload["failures"][0]["actual"] == 2


def test_canonical_result_hash_ignores_dictionary_order_only():
    first = [{"b": 2, "a": 1}, {"a": 3}]
    second = [{"a": 1, "b": 2}, {"a": 3}]
    assert canonical_result_hash(first) == canonical_result_hash(second)
    assert canonical_result_hash(first) != canonical_result_hash(list(reversed(second)))


def test_correctness_artifact_keeps_digests_not_full_result_bodies(tmp_path):
    rows = [{"value": number} for number in range(100)]
    output = write_correctness(
        tmp_path / "correctness.json",
        [GateResult("rows", True, 100, 100, {})],
        [QueryEvidence("values", "SELECT value", "sql-sha", rows)],
        {"values": rows},
    )

    assert "distributions" not in output
    assert output["distribution_digests"]["values"] == {
        "value_kind": "rows",
        "item_count": 100,
        "sha256": canonical_result_hash(rows),
    }
    assert "rows" not in output["queries"][0]
    assert output["queries"][0]["result_row_count"] == 100
    assert output["queries"][0]["result_sha256"] == canonical_result_hash(rows)
    assert (tmp_path / "correctness.json").stat().st_size < 2_000


def _evaluate_with_references(**reference_overrides):
    referential = {
        "missing_works_for_authors": 0,
        "missing_authors": 0,
        "distinct_missing_author_ids": 0,
        "works_with_missing_authors": 0,
        "author_reference_coverage_ratio": 1.0,
        "institution_bridge_rows": 10,
        "missing_institutions": 2,
        "distinct_missing_institution_ids": 1,
        "works_with_missing_institutions": 2,
        "authors_with_missing_institutions": 2,
        "institution_reference_coverage_ratio": 0.8,
        "topic_bridge_rows": 10,
        "missing_topics": 0,
        "distinct_missing_topic_ids": 0,
        "topic_reference_coverage_ratio": 1.0,
        "citation_edges": 20,
        "retained_cited_edges": 4,
        "citation_retention_ratio": 0.2,
        **reference_overrides,
    }
    responses = iter(
        [
            [{"rows": 2, "unique_ids": 2}],
            [{"authors": 2, "institutions": 2, "topics": 2}],
            [{"works": 2, "authors": 2, "institutions": 2, "topics": 2, "citations": 2}],
            [referential],
            [{"institution_id": 99, "display_name": "Deleted Institute", "raw_bridge_rows": 2}],
            *[[{"rows": 2, "unique_ids": 2}] for _ in range(5)],
            [],
            [],
        ]
    )
    return evaluate_stage1(
        lambda _: next(responses),
        database="fixture",
        works_glob="tiers/stage1/works/*.parquet",
        expected_manifest_rows=2,
        raw_evidence={
            "rejected_id_entries": 0,
            "null_topic_scores": 0,
            "distinct_valid_pairs": 2,
            "duplicate_pair_delta": 0,
        },
    )


def test_missing_institutions_are_reported_but_do_not_fail_stage1():
    gates, _, distributions = _evaluate_with_references()
    require_all(gates)
    institution_gate = next(gate for gate in gates if gate.name == "missing_institutions")
    assert institution_gate.passed is False
    assert institution_gate.blocking is False
    assert distributions["referential_coverage"]["missing_institutions"] == 2
    assert distributions["missing_institution_sample"][0]["institution_id"] == 99


@pytest.mark.parametrize(
    "field",
    ["missing_works_for_authors", "missing_authors", "missing_topics"],
)
def test_internal_reference_gaps_remain_blocking(field):
    gates, _, _ = _evaluate_with_references(**{field: 1})
    with pytest.raises(CorrectnessFailure, match=field):
        require_all(gates)
