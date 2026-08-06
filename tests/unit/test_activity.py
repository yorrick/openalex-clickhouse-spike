import pytest

from openalex_spike.activity import (
    MergeActivityError,
    collect_merge_activity,
    summarize_merge_activity,
)


class FakeService:
    def __init__(self, *, coverage_start=900, fail_on=None, active_merge=True):
        self.coverage_start = coverage_start
        self.fail_on = fail_on
        self.active_merge = active_merge
        self.calls = []

    def query_json(self, sql):
        self.calls.append(("query", sql))
        if self.fail_on and self.fail_on in sql:
            raise RuntimeError("telemetry read failed")
        if "system.merges" in sql:
            if not self.active_merge:
                return [
                    {
                        "observed_at_unix_us": 2_000,
                        "started_at_unix_us": 2_000,
                        "database": None,
                    }
                ]
            return [
                {
                    "observed_at_unix_us": 2_000,
                    "started_at_unix_us": 1_500,
                    "database": "system",
                    "table": "query_log",
                    "elapsed_seconds": 0.0005,
                    "progress": 0.5,
                    "num_parts": 2,
                    "total_size_bytes_compressed": 100,
                    "bytes_read_uncompressed": 200,
                    "rows_read": 3,
                    "bytes_written_uncompressed": 50,
                    "rows_written": 1,
                    "memory_usage": 64,
                }
            ]
        if "count() AS row_count" in sql:
            return [
                {
                    "row_count": 10,
                    "minimum_event_at_unix_us": self.coverage_start,
                    "maximum_event_at_unix_us": 2_100,
                }
            ]
        if "FROM system.part_log" in sql:
            return [
                {
                    "started_at_unix_us": 1_100,
                    "finished_at_unix_us": 1_900,
                    "duration_ms": 1,
                    "database": "system",
                    "table": "query_log",
                    "part_name": "all_1_2_1",
                    "source_part_count": 2,
                    "rows": 3,
                    "read_rows": 4,
                    "read_bytes": 5,
                    "size_in_bytes": 6,
                    "peak_memory_usage": 7,
                    "os_cpu_wait_time_us": 8,
                    "disk_read_elapsed_us": 9,
                }
            ]
        raise AssertionError(sql)

    def execute_script(self, sql):
        self.calls.append(("execute", sql))


def test_collect_merge_activity_snapshots_inflight_then_flushes_and_reads_history():
    service = FakeService()

    activity = collect_merge_activity(
        service,
        phase_start_unix_us=1_000,
        phase_end_unix_us=2_000,
        benchmark_database="openalex_stage2_test_12345678",
    )

    assert activity["schema_version"] == 1
    assert activity["status"] == "complete"
    assert len(activity["in_flight_at_phase_end"]) == 1
    assert len(activity["completed_merges"]) == 1
    assert activity["in_flight_snapshot_observed_at_unix_us"] == 2_000
    assert activity["in_flight_snapshot_delay_us"] == 0
    assert [kind for kind, _ in service.calls] == [
        "query",
        "execute",
        "query",
        "query",
    ]
    assert service.calls[1] == ("execute", "SYSTEM FLUSH LOGS")
    completed_sql = service.calls[-1][1]
    assert "event_time_microseconds" in completed_sql
    assert "duration_ms" in completed_sql


def test_collect_merge_activity_preserves_empty_snapshot_timestamp():
    activity = collect_merge_activity(
        FakeService(active_merge=False),
        phase_start_unix_us=1_000,
        phase_end_unix_us=2_000,
        benchmark_database="openalex_stage2_test_12345678",
    )

    assert activity["in_flight_at_phase_end"] == []
    assert activity["in_flight_snapshot_observed_at_unix_us"] == 2_000
    assert activity["in_flight_snapshot_delay_us"] == 0


def test_collect_merge_activity_rejects_truncated_part_log_coverage():
    service = FakeService(coverage_start=1_001)

    with pytest.raises(MergeActivityError, match="does not cover phase start"):
        collect_merge_activity(
            service,
            phase_start_unix_us=1_000,
            phase_end_unix_us=2_000,
            benchmark_database="openalex_stage2_test_12345678",
        )


def test_collect_merge_activity_does_not_hide_read_failures():
    service = FakeService(fail_on="system.part_log")

    with pytest.raises(RuntimeError, match="telemetry read failed"):
        collect_merge_activity(
            service,
            phase_start_unix_us=1_000,
            phase_end_unix_us=2_000,
            benchmark_database="openalex_stage2_test_12345678",
        )


def test_merge_activity_summary_separates_system_and_benchmark_merges():
    activity = {
        "schema_version": 1,
        "status": "complete",
        "part_log_coverage": {"row_count": 10},
        "completed_merges": [
            {"database": "system", "duration_ms": 7_000},
            {"database": "openalex", "duration_ms": 3_000},
        ],
        "in_flight_at_phase_end": [
            {"database": "system", "elapsed_seconds": 2.0}
        ],
    }

    summary = summarize_merge_activity(activity, benchmark_database="openalex")

    assert summary["completed_merge_count"] == 2
    assert summary["completed_system_merge_count"] == 1
    assert summary["completed_benchmark_merge_count"] == 1
    assert summary["maximum_completed_system_merge_ms"] == 7_000
    assert summary["in_flight_merge_count"] == 1
    assert summary["completed_foreign_merge_count"] == 0
    assert summary["foreign_databases"] == []


def test_merge_activity_summary_surfaces_foreign_database_contamination():
    activity = {
        "schema_version": 1,
        "status": "complete",
        "part_log_coverage": {"row_count": 10},
        "completed_merges": [
            {"database": "openalex_stage2_prior", "duration_ms": 8_000},
        ],
        "in_flight_at_phase_end": [
            {"database": "openalex_stage2_other", "elapsed_seconds": 2.0},
        ],
    }

    summary = summarize_merge_activity(activity, benchmark_database="openalex")

    assert summary["completed_foreign_merge_count"] == 1
    assert summary["in_flight_foreign_merge_count"] == 1
    assert summary["foreign_databases"] == [
        "openalex_stage2_other",
        "openalex_stage2_prior",
    ]
