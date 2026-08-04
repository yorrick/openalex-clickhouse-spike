from pathlib import Path

from openalex_spike.benchmark import load_query_catalog, run_sequential
from openalex_spike.config import QueryEnvelope


class FakeClient:
    def execute(self, query, *, parameters, settings, query_id):
        return {
            "elapsed_seconds": 0.25,
            "read_rows": 10,
            "read_bytes": 100,
            "result_rows": 2,
            "peak_memory_bytes": 1024,
            "spill_bytes": 0,
            "query_id": query_id,
            "settings": settings,
            "parameters": parameters,
        }


def test_catalog_contains_exact_fixed_query_contract():
    catalog = load_query_catalog(Path("sql/queries"))
    assert [query.name for query in catalog] == [f"q0{i}" for i in range(1, 8)]
    assert {query.query_class for query in catalog} == {
        "routine",
        "join",
        "one_hop",
        "two_hop",
    }
    assert [query.name for query in catalog if query.diagnostic] == ["q06"]
    assert [query.name for query in catalog if query.requires_seed] == ["q05", "q06"]


def test_sequential_runner_records_post_restart_and_five_warm_runs():
    query = load_query_catalog(Path("sql/queries"))[0]
    restarts = []
    records = run_sequential(
        [query],
        FakeClient,
        lambda: restarts.append(True),
        QueryEnvelope(32, 7, 2),
        seed_work_ids=(1, 2, 3),
    )
    assert len(restarts) == 1
    assert [record.run_kind for record in records] == [
        "post_restart_run",
        "warm_run",
        "warm_run",
        "warm_run",
        "warm_run",
        "warm_run",
    ]
    assert len({record.query_id for record in records}) == 6
    assert all("cold" not in record.run_kind for record in records)
    assert all(record.gating for record in records)
