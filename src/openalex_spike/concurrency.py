from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from math import ceil
from pathlib import Path
from queue import Queue
from threading import Event, Lock
from time import monotonic
from typing import Callable, Sequence
import json
import uuid

from openalex_spike.benchmark import (
    BenchmarkClient,
    BenchmarkQuery,
    envelope_settings,
)
from openalex_spike.config import QueryEnvelope


CONCURRENCY_NAMESPACE = uuid.UUID("c05be588-953c-55d7-9489-13e23e4b7251")
GATED_CLASSES = ("routine", "join", "one_hop")


@dataclass(frozen=True)
class ConcurrentRecord:
    worker_id: int
    query_name: str
    query_class: str
    query_id: str
    worker_iteration: int
    seed_work_id: int | None
    elapsed_seconds: float
    max_threads: int
    error: str | None
    read_rows: int = 0
    read_bytes: int = 0
    peak_memory_bytes: int = 0
    spill_bytes: int = 0
    started_at_unix_us: int = 0
    finished_at_unix_us: int = 0
    real_time_us: int = 0
    user_time_us: int = 0
    system_time_us: int = 0
    os_cpu_virtual_time_us: int = 0
    os_cpu_wait_time_us: int = 0
    disk_read_elapsed_us: int = 0
    synchronous_read_wait_us: int = 0
    page_cache_miss_bytes: int = 0
    page_cache_miss_elapsed_us: int = 0
    os_read_bytes: int = 0
    file_descriptor_read_bytes: int = 0


def build_worker_schedules(
    catalog: Sequence[BenchmarkQuery], *, workers: int = 3
) -> tuple[tuple[BenchmarkQuery, ...], ...]:
    if workers <= 0:
        raise ValueError("concurrency workers must be positive")
    gated = tuple(query for query in catalog if not query.diagnostic)
    if not gated:
        raise ValueError("concurrency catalog has no gating queries")
    return tuple(
        gated[offset % len(gated) :] + gated[: offset % len(gated)]
        for offset in range(workers)
    )


def run_closed_loop(
    catalog: Sequence[BenchmarkQuery],
    client_factory: Callable[[int], BenchmarkClient],
    envelope: QueryEnvelope,
    *,
    seed_work_ids: tuple[int, int, int],
    minimum_samples: int,
    maximum_seconds: float,
    worker_count: int = 3,
    query_threads: int = 8,
    clock: Callable[[], float] = monotonic,
) -> tuple[list[ConcurrentRecord], str | None]:
    if worker_count <= 0:
        raise ValueError("concurrency worker count must be positive")
    if query_threads <= 0:
        raise ValueError("concurrent query threads must be positive")
    schedules = build_worker_schedules(catalog, workers=worker_count)
    deadline = clock() + maximum_seconds
    stop = Event()
    lock = Lock()
    output: Queue[ConcurrentRecord] = Queue()
    counts = {query_class: 0 for query_class in GATED_CLASSES}
    first_error: list[str] = []
    settings = envelope_settings(envelope, max_threads=query_threads)

    def all_classes_complete() -> bool:
        return all(counts[name] >= minimum_samples for name in GATED_CLASSES)

    def worker(worker_id: int) -> None:
        client = client_factory(worker_id)
        schedule = schedules[worker_id]
        iteration = 0
        while not stop.is_set() and clock() < deadline:
            with lock:
                if all_classes_complete():
                    stop.set()
                    return
            query = schedule[iteration % len(schedule)]
            query_id = str(
                uuid.uuid5(
                    CONCURRENCY_NAMESPACE,
                    f"worker:{worker_id}:iteration:{iteration}:{query.name}",
                )
            )
            seed = seed_work_ids[iteration % len(seed_work_ids)]
            try:
                telemetry = client.execute(
                    query,
                    parameters={"seed_work_id": seed} if query.requires_seed else {},
                    settings=settings,
                    query_id=query_id,
                )
                record = ConcurrentRecord(
                    worker_id=worker_id,
                    query_name=query.name,
                    query_class=query.query_class,
                    query_id=query_id,
                    worker_iteration=iteration,
                    seed_work_id=seed if query.requires_seed else None,
                    elapsed_seconds=float(telemetry["elapsed_seconds"]),
                    max_threads=int(settings["max_threads"]),
                    error=None,
                    read_rows=int(telemetry["read_rows"]),
                    read_bytes=int(telemetry["read_bytes"]),
                    peak_memory_bytes=int(telemetry["peak_memory_bytes"]),
                    spill_bytes=int(telemetry["spill_bytes"]),
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
                output.put(record)
                with lock:
                    counts[query.query_class] += 1
            except Exception as error:
                message = f"{type(error).__name__}: {error}"
                output.put(
                    ConcurrentRecord(
                        worker_id=worker_id,
                        query_name=query.name,
                        query_class=query.query_class,
                        query_id=query_id,
                        worker_iteration=iteration,
                        seed_work_id=seed if query.requires_seed else None,
                        elapsed_seconds=0.0,
                        max_threads=int(settings["max_threads"]),
                        error=message,
                    )
                )
                with lock:
                    if not first_error:
                        first_error.append(message)
                stop.set()
                return
            iteration += 1

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = [
            executor.submit(worker, worker_id) for worker_id in range(worker_count)
        ]
        for future in futures:
            future.result()

    records = []
    while not output.empty():
        records.append(output.get())
    records.sort(key=lambda record: (record.worker_id, record.worker_iteration))
    return records, first_error[0] if first_error else None


def _nearest_rank_p95(values: list[float]) -> float:
    ordered = sorted(values)
    return ordered[max(0, ceil(0.95 * len(ordered)) - 1)]


def summarize_concurrency(
    records: Sequence[ConcurrentRecord],
    *,
    minimum_samples: int,
    first_error: str | None,
) -> dict[str, object]:
    class_summary = {}
    for query_class in GATED_CLASSES:
        successful = [
            record
            for record in records
            if record.query_class == query_class and record.error is None
        ]
        durations = [record.elapsed_seconds for record in successful]
        class_summary[query_class] = {
            "count": len(durations),
            "median_seconds": (
                sorted(durations)[(len(durations) - 1) // 2] if durations else None
            ),
            "p95_seconds": _nearest_rank_p95(durations) if durations else None,
            "maximum_seconds": max(durations) if durations else None,
            "peak_memory_bytes": max(
                (record.peak_memory_bytes for record in successful), default=0
            ),
            "spill_bytes": sum(record.spill_bytes for record in successful),
            "read_rows": sum(record.read_rows for record in successful),
            "read_bytes": sum(record.read_bytes for record in successful),
            "insufficient_sample": len(durations) < minimum_samples,
        }
    query_summary = {}
    for query_name in sorted({record.query_name for record in records}):
        successful = [
            record
            for record in records
            if record.query_name == query_name and record.error is None
        ]
        durations = [record.elapsed_seconds for record in successful]
        query_summary[query_name] = {
            "count": len(durations),
            "median_seconds": (
                sorted(durations)[(len(durations) - 1) // 2] if durations else None
            ),
            "p95_seconds": _nearest_rank_p95(durations) if durations else None,
            "maximum_seconds": max(durations) if durations else None,
            "peak_memory_bytes": max(
                (record.peak_memory_bytes for record in successful), default=0
            ),
            "spill_bytes": sum(record.spill_bytes for record in successful),
        }
    if first_error:
        verdict_cap = "fail"
    elif any(item["insufficient_sample"] for item in class_summary.values()):
        verdict_cap = "conditional"
    else:
        verdict_cap = "pass"
    return {
        "classes": class_summary,
        "queries": query_summary,
        "first_error": first_error,
        "forced_verdict": "fail" if first_error else None,
        "verdict_cap": verdict_cap,
    }


def write_concurrency_records(destination: Path, records: Sequence[ConcurrentRecord]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w") as output:
        for record in records:
            output.write(json.dumps(asdict(record), sort_keys=True) + "\n")
