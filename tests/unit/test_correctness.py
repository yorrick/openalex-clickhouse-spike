import json

import pytest

from openalex_spike.correctness import (
    CorrectnessFailure,
    GateResult,
    canonical_result_hash,
    require_all,
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
