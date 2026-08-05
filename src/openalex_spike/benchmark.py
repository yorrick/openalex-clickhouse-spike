from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol, Sequence
import uuid

from openalex_spike.config import QueryEnvelope


QUERY_CONTRACT = {
    "q01": ("q01_works_by_year.sql", "routine", False),
    "q02": ("q02_topic_totals.sql", "join", False),
    "q03": ("q03_author_output.sql", "join", False),
    "q04": ("q04_collaboration.sql", "join", False),
    "q05": ("q05_one_hop.sql", "one_hop", False),
    "q06": ("q06_two_hop.sql", "two_hop", True),
    "q07": ("q07_citations_by_year.sql", "routine", False),
}
QUERY_NAMESPACE = uuid.UUID("9bb27f3d-3971-5010-a257-595c6b0d5daa")


@dataclass(frozen=True)
class BenchmarkQuery:
    name: str
    filename: str
    query_class: str
    diagnostic: bool
    sql: str
    requires_seed: bool


@dataclass(frozen=True)
class SequentialRecord:
    query_name: str
    query_class: str
    query_id: str
    run_kind: str
    run_number: int
    gating: bool
    elapsed_seconds: float
    read_rows: int
    read_bytes: int
    result_rows: int
    peak_memory_bytes: int
    spill_bytes: int
    seed_work_id: int | None
    started_at_unix_us: int
    finished_at_unix_us: int
    real_time_us: int
    user_time_us: int
    system_time_us: int
    os_cpu_virtual_time_us: int
    os_cpu_wait_time_us: int
    disk_read_elapsed_us: int
    synchronous_read_wait_us: int
    page_cache_miss_bytes: int
    page_cache_miss_elapsed_us: int
    os_read_bytes: int
    file_descriptor_read_bytes: int


class BenchmarkClient(Protocol):
    def execute(
        self,
        query: BenchmarkQuery,
        *,
        parameters: dict[str, int],
        settings: dict[str, int | str],
        query_id: str,
    ) -> dict[str, object]: ...


class ServiceBenchmarkClient:
    def __init__(self, service: object, database: str) -> None:
        self.service = service
        self.database = database

    def execute(
        self,
        query: BenchmarkQuery,
        *,
        parameters: dict[str, int],
        settings: dict[str, int | str],
        query_id: str,
    ) -> dict[str, object]:
        sql = query.sql.replace("openalex_spike", self.database)
        return self.service.execute_benchmark_query(
            sql,
            parameters=parameters,
            settings=settings,
            query_id=query_id,
        )


def load_query_catalog(directory: Path | str) -> tuple[BenchmarkQuery, ...]:
    directory = Path(directory)
    catalog = []
    for name, (filename, query_class, diagnostic) in QUERY_CONTRACT.items():
        sql = (directory / filename).read_text()
        requires_seed = "{seed_work_id:UInt64}" in sql
        if requires_seed != (name in {"q05", "q06"}):
            raise ValueError(f"unexpected seed placeholder contract in {filename}")
        catalog.append(
            BenchmarkQuery(
                name=name,
                filename=filename,
                query_class=query_class,
                diagnostic=diagnostic,
                sql=sql,
                requires_seed=requires_seed,
            )
        )
    return tuple(catalog)


def envelope_settings(
    envelope: QueryEnvelope, *, max_threads: int
) -> dict[str, int | str]:
    return {
        "max_threads": max_threads,
        "max_memory_usage": envelope.max_memory_usage_gib * (1 << 30),
        "max_bytes_before_external_group_by": envelope.spill_gib * (1 << 30),
        "max_bytes_before_external_sort": envelope.spill_gib * (1 << 30),
        "join_algorithm": "auto",
    }


def run_sequential(
    catalog: Sequence[BenchmarkQuery],
    client_factory: Callable[[], BenchmarkClient],
    restart: Callable[[], None],
    envelope: QueryEnvelope,
    *,
    seed_work_ids: tuple[int, int, int],
    max_threads: int = 16,
) -> list[SequentialRecord]:
    if max_threads <= 0:
        raise ValueError("sequential query threads must be positive")
    records = []
    settings = envelope_settings(envelope, max_threads=max_threads)
    for query in catalog:
        restart()
        client = client_factory()
        for run_number in range(6):
            run_kind = "post_restart_run" if run_number == 0 else "warm_run"
            query_id = str(
                uuid.uuid5(
                    QUERY_NAMESPACE,
                    f"{query.name}:{run_kind}:{run_number}",
                )
            )
            seed_work_id = (
                seed_work_ids[run_number % len(seed_work_ids)]
                if query.requires_seed
                else None
            )
            telemetry = client.execute(
                query,
                parameters=(
                    {"seed_work_id": seed_work_id}
                    if seed_work_id is not None
                    else {}
                ),
                settings=settings,
                query_id=query_id,
            )
            records.append(
                SequentialRecord(
                    query_name=query.name,
                    query_class=query.query_class,
                    query_id=query_id,
                    run_kind=run_kind,
                    run_number=run_number,
                    gating=not query.diagnostic,
                    elapsed_seconds=float(telemetry["elapsed_seconds"]),
                    read_rows=int(telemetry["read_rows"]),
                    read_bytes=int(telemetry["read_bytes"]),
                    result_rows=int(telemetry["result_rows"]),
                    peak_memory_bytes=int(telemetry["peak_memory_bytes"]),
                    spill_bytes=int(telemetry["spill_bytes"]),
                    seed_work_id=seed_work_id,
                    started_at_unix_us=int(telemetry["started_at_unix_us"]),
                    finished_at_unix_us=int(telemetry["finished_at_unix_us"]),
                    real_time_us=int(telemetry["real_time_us"]),
                    user_time_us=int(telemetry["user_time_us"]),
                    system_time_us=int(telemetry["system_time_us"]),
                    os_cpu_virtual_time_us=int(
                        telemetry["os_cpu_virtual_time_us"]
                    ),
                    os_cpu_wait_time_us=int(telemetry["os_cpu_wait_time_us"]),
                    disk_read_elapsed_us=int(telemetry["disk_read_elapsed_us"]),
                    synchronous_read_wait_us=int(
                        telemetry["synchronous_read_wait_us"]
                    ),
                    page_cache_miss_bytes=int(telemetry["page_cache_miss_bytes"]),
                    page_cache_miss_elapsed_us=int(
                        telemetry["page_cache_miss_elapsed_us"]
                    ),
                    os_read_bytes=int(telemetry["os_read_bytes"]),
                    file_descriptor_read_bytes=int(
                        telemetry["file_descriptor_read_bytes"]
                    ),
                )
            )
    return records
