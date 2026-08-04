from openalex_spike.benchmark import load_query_catalog
from openalex_spike.concurrency import (
    ConcurrentRecord,
    build_worker_schedules,
    run_closed_loop,
    summarize_concurrency,
)
from openalex_spike.config import QueryEnvelope


class FakeClient:
    def execute(self, query, *, parameters, settings, query_id):
        return {
            "elapsed_seconds": 0.1,
            "read_rows": 1,
            "read_bytes": 10,
            "result_rows": 1,
            "peak_memory_bytes": 100,
            "spill_bytes": 0,
        }


def test_worker_schedules_are_rotated_and_exclude_two_hop():
    schedules = build_worker_schedules(load_query_catalog("sql/queries"))
    assert len(schedules) == 3
    assert all("q06" not in [query.name for query in schedule] for schedule in schedules)
    assert schedules[1][0] == schedules[0][1]
    assert schedules[2][0] == schedules[0][2]


def test_closed_loop_reaches_every_gated_class_without_two_hop():
    records, error = run_closed_loop(
        load_query_catalog("sql/queries"),
        lambda worker_id: FakeClient(),
        QueryEnvelope(32, 7, 2),
        seed_work_ids=(1, 2, 3),
        minimum_samples=2,
        maximum_seconds=60,
    )
    assert error is None
    assert "two_hop" not in {record.query_class for record in records}
    assert {record.query_class for record in records} == {"routine", "join", "one_hop"}
    assert all(record.max_threads == 8 for record in records)


def test_under_sampled_class_caps_verdict_at_conditional():
    record = ConcurrentRecord(
        worker_id=0,
        query_name="q01",
        query_class="routine",
        query_id="id",
        elapsed_seconds=1.0,
        max_threads=8,
        error=None,
    )
    summary = summarize_concurrency([record], minimum_samples=50, first_error=None)
    assert summary["verdict_cap"] == "conditional"
    assert summary["classes"]["routine"]["insufficient_sample"] is True
