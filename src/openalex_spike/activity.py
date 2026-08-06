from __future__ import annotations

from typing import Protocol
import re


class MergeActivityError(RuntimeError):
    pass


class MergeActivityService(Protocol):
    def query_json(self, sql: str) -> list[dict[str, object]]: ...

    def execute_script(self, sql: str) -> None: ...


def collect_merge_activity(
    service: MergeActivityService,
    *,
    phase_start_unix_us: int,
    phase_end_unix_us: int,
    benchmark_database: str,
) -> dict[str, object]:
    if phase_start_unix_us <= 0 or phase_end_unix_us < phase_start_unix_us:
        raise MergeActivityError("invalid benchmark phase interval")
    if not re.fullmatch(r"[A-Za-z0-9_]+", benchmark_database):
        raise MergeActivityError("invalid benchmark database name")

    snapshot_rows = service.query_json(
        "WITH toUnixTimestamp64Micro(now64(6)) AS observed_at_unix_us "
        "SELECT observed_at_unix_us, "
        "observed_at_unix_us - toInt64(m.elapsed * 1000000) "
        "AS started_at_unix_us, "
        "m.database, m.table, m.elapsed AS elapsed_seconds, m.progress, "
        "m.num_parts, m.total_size_bytes_compressed, "
        "m.bytes_read_uncompressed, m.rows_read, "
        "m.bytes_written_uncompressed, m.rows_written, m.memory_usage "
        "FROM system.one AS anchor LEFT JOIN system.merges AS m ON 1 "
        "ORDER BY m.database, m.table, started_at_unix_us"
    )
    if not snapshot_rows:
        raise MergeActivityError("system.merges snapshot returned no anchor row")
    observed_times = {
        int(row["observed_at_unix_us"]) for row in snapshot_rows
    }
    if len(observed_times) != 1:
        raise MergeActivityError("system.merges snapshot used inconsistent clocks")
    snapshot_observed_at_unix_us = observed_times.pop()
    snapshot_delay_us = snapshot_observed_at_unix_us - phase_end_unix_us
    if snapshot_delay_us < 0:
        raise MergeActivityError("system.merges snapshot predates phase end")
    in_flight = [row for row in snapshot_rows if row["database"]]

    # Capture the phase-end in-flight set before flushing. The flush then makes
    # completed part-log events at the boundary visible for the historical read.
    service.execute_script("SYSTEM FLUSH LOGS")
    coverage_rows = service.query_json(
        "SELECT count() AS row_count, "
        "toUnixTimestamp64Micro(minOrNull(event_time_microseconds)) "
        "AS minimum_event_at_unix_us, "
        "toUnixTimestamp64Micro(maxOrNull(event_time_microseconds)) "
        "AS maximum_event_at_unix_us "
        "FROM system.part_log WHERE event_type = 'MergeParts'"
    )
    if len(coverage_rows) != 1:
        raise MergeActivityError("part_log coverage query returned an invalid result")
    coverage = coverage_rows[0]
    row_count = int(coverage["row_count"])
    minimum_event = coverage["minimum_event_at_unix_us"]
    maximum_event = coverage["maximum_event_at_unix_us"]
    if row_count <= 0 or minimum_event is None or maximum_event is None:
        raise MergeActivityError("part_log has no completed merge history")
    if int(minimum_event) > phase_start_unix_us:
        raise MergeActivityError("part_log does not cover phase start")

    completed = service.query_json(
        "SELECT "
        "toUnixTimestamp64Micro(event_time_microseconds) - "
        "toInt64(duration_ms) * 1000 AS started_at_unix_us, "
        "toUnixTimestamp64Micro(event_time_microseconds) AS finished_at_unix_us, "
        "duration_ms, database, table, part_name, length(merged_from) "
        "AS source_part_count, rows, read_rows, read_bytes, size_in_bytes, "
        "peak_memory_usage, "
        "ProfileEvents['OSCPUWaitMicroseconds'] AS os_cpu_wait_time_us, "
        "ProfileEvents['DiskReadElapsedMicroseconds'] AS disk_read_elapsed_us "
        "FROM system.part_log WHERE event_type = 'MergeParts' "
        f"AND toUnixTimestamp64Micro(event_time_microseconds) >= {phase_start_unix_us} "
        "AND toUnixTimestamp64Micro(event_time_microseconds) - "
        f"toInt64(duration_ms) * 1000 <= {phase_end_unix_us} "
        "ORDER BY finished_at_unix_us, database, table, part_name"
    )
    return {
        "schema_version": 1,
        "status": "complete",
        "source": {
            "completed": "system.part_log",
            "in_flight_at_phase_end": "system.merges",
        },
        "phase_start_unix_us": phase_start_unix_us,
        "phase_end_unix_us": phase_end_unix_us,
        "in_flight_snapshot_observed_at_unix_us": snapshot_observed_at_unix_us,
        "in_flight_snapshot_delay_us": snapshot_delay_us,
        "benchmark_database": benchmark_database,
        "part_log_flushed_before_read": True,
        "part_log_coverage": {
            "row_count": row_count,
            "minimum_event_at_unix_us": int(minimum_event),
            "maximum_event_at_unix_us": int(maximum_event),
        },
        "completed_merges": completed,
        "in_flight_at_phase_end": in_flight,
    }


def summarize_merge_activity(
    activity: dict[str, object], *, benchmark_database: str
) -> dict[str, object]:
    completed = list(activity["completed_merges"])
    in_flight = list(activity["in_flight_at_phase_end"])
    system_completed = [row for row in completed if row["database"] == "system"]
    benchmark_completed = [
        row for row in completed if row["database"] == benchmark_database
    ]
    foreign_completed = [
        row
        for row in completed
        if row["database"] not in {"system", benchmark_database}
    ]
    foreign_in_flight = [
        row
        for row in in_flight
        if row["database"] not in {"system", benchmark_database}
    ]
    return {
        "schema_version": int(activity["schema_version"]),
        "status": activity["status"],
        "part_log_coverage": activity["part_log_coverage"],
        "completed_merge_count": len(completed),
        "completed_system_merge_count": len(system_completed),
        "completed_benchmark_merge_count": len(benchmark_completed),
        "completed_foreign_merge_count": len(foreign_completed),
        "maximum_completed_merge_ms": max(
            (int(row["duration_ms"]) for row in completed), default=0
        ),
        "maximum_completed_system_merge_ms": max(
            (int(row["duration_ms"]) for row in system_completed), default=0
        ),
        "in_flight_merge_count": len(in_flight),
        "in_flight_system_merge_count": sum(
            row["database"] == "system" for row in in_flight
        ),
        "in_flight_benchmark_merge_count": sum(
            row["database"] == benchmark_database for row in in_flight
        ),
        "in_flight_foreign_merge_count": len(foreign_in_flight),
        "foreign_databases": sorted(
            {
                str(row["database"])
                for row in foreign_completed + foreign_in_flight
            }
        ),
    }
