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
            "started_at_unix_us": 1_000_000,
            "finished_at_unix_us": 1_100_000,
            "read_rows": 1,
            "read_bytes": 10,
            "result_rows": 1,
            "peak_memory_bytes": 100,
            "spill_bytes": 0,
            "real_time_us": 100_000,
            "user_time_us": 50_000,
            "system_time_us": 5_000,
            "os_cpu_virtual_time_us": 55_000,
            "os_cpu_wait_time_us": 10_000,
            "disk_read_elapsed_us": 2_000,
            "synchronous_read_wait_us": 3_000,
            "page_cache_miss_bytes": 4_000,
            "page_cache_miss_elapsed_us": 1_000,
            "os_read_bytes": 6_000,
            "file_descriptor_read_bytes": 5_000,
        }


def test_worker_schedules_are_rotated_and_exclude_two_hop():
    schedules = build_worker_schedules(load_query_catalog("sql/queries"))
    assert len(schedules) == 3
    assert all("q06" not in [query.name for query in schedule] for schedule in schedules)
    assert schedules[1][0] == schedules[0][1]
    assert schedules[2][0] == schedules[0][2]


def test_single_worker_gets_full_unrotated_gated_catalog():
    catalog = load_query_catalog("sql/queries")
    schedules = build_worker_schedules(catalog, workers=1)

    assert len(schedules) == 1
    assert [query.name for query in schedules[0]] == [
        "q01",
        "q02",
        "q03",
        "q04",
        "q05",
        "q07",
    ]


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


def test_closed_loop_uses_requested_single_worker_threads_and_telemetry():
    records, error = run_closed_loop(
        load_query_catalog("sql/queries"),
        lambda worker_id: FakeClient(),
        QueryEnvelope(50, 12, 4),
        seed_work_ids=(1, 2, 3),
        minimum_samples=1,
        maximum_seconds=60,
        worker_count=1,
        query_threads=18,
    )

    assert error is None
    assert {record.worker_id for record in records} == {0}
    assert all(record.max_threads == 18 for record in records)
    assert all(record.read_rows == 1 for record in records)
    assert all(record.read_bytes == 10 for record in records)
    assert all(record.peak_memory_bytes == 100 for record in records)
    assert all(record.spill_bytes == 0 for record in records)
    assert [record.worker_iteration for record in records] == list(
        range(len(records))
    )
    q05 = next(record for record in records if record.query_name == "q05")
    assert q05.seed_work_id == 2
    assert q05.started_at_unix_us == 1_000_000
    assert q05.finished_at_unix_us == 1_100_000
    assert q05.os_cpu_wait_time_us == 10_000
    assert q05.page_cache_miss_bytes == 4_000
    assert q05.os_read_bytes == 6_000


def test_under_sampled_class_caps_verdict_at_conditional():
    record = ConcurrentRecord(
        worker_id=0,
        query_name="q01",
        query_class="routine",
        query_id="id",
        worker_iteration=0,
        seed_work_id=None,
        elapsed_seconds=1.0,
        max_threads=8,
        error=None,
    )
    summary = summarize_concurrency([record], minimum_samples=50, first_error=None)
    assert summary["verdict_cap"] == "conditional"
    assert summary["classes"]["routine"]["insufficient_sample"] is True
    assert summary["queries"]["q01"]["count"] == 1
