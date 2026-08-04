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
    elapsed_seconds: float
    max_threads: int
    error: str | None


def build_worker_schedules(
    catalog: Sequence[BenchmarkQuery],
) -> tuple[tuple[BenchmarkQuery, ...], ...]:
    gated = tuple(query for query in catalog if not query.diagnostic)
    if not gated:
        raise ValueError("concurrency catalog has no gating queries")
    return tuple(gated[offset:] + gated[:offset] for offset in range(3))


def run_closed_loop(
    catalog: Sequence[BenchmarkQuery],
    client_factory: Callable[[int], BenchmarkClient],
    envelope: QueryEnvelope,
    *,
    seed_work_ids: tuple[int, int, int],
    minimum_samples: int,
    maximum_seconds: float,
    clock: Callable[[], float] = monotonic,
) -> tuple[list[ConcurrentRecord], str | None]:
    schedules = build_worker_schedules(catalog)
    deadline = clock() + maximum_seconds
    stop = Event()
    lock = Lock()
    output: Queue[ConcurrentRecord] = Queue()
    counts = {query_class: 0 for query_class in GATED_CLASSES}
    first_error: list[str] = []
    settings = envelope_settings(envelope, max_threads=8)

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
                    elapsed_seconds=float(telemetry["elapsed_seconds"]),
                    max_threads=int(settings["max_threads"]),
                    error=None,
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

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(worker, worker_id) for worker_id in range(3)]
        for future in futures:
            future.result()

    records = []
    while not output.empty():
        records.append(output.get())
    records.sort(key=lambda record: (record.worker_id, record.query_id))
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
        durations = [
            record.elapsed_seconds
            for record in records
            if record.query_class == query_class and record.error is None
        ]
        class_summary[query_class] = {
            "count": len(durations),
            "median_seconds": (
                sorted(durations)[(len(durations) - 1) // 2] if durations else None
            ),
            "p95_seconds": _nearest_rank_p95(durations) if durations else None,
            "maximum_seconds": max(durations) if durations else None,
            "insufficient_sample": len(durations) < minimum_samples,
        }
    if first_error:
        verdict_cap = "fail"
    elif any(item["insufficient_sample"] for item in class_summary.values()):
        verdict_cap = "conditional"
    else:
        verdict_cap = "pass"
    return {
        "classes": class_summary,
        "first_error": first_error,
        "forced_verdict": "fail" if first_error else None,
        "verdict_cap": verdict_cap,
    }


def write_concurrency_records(destination: Path, records: Sequence[ConcurrentRecord]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w") as output:
        for record in records:
            output.write(json.dumps(asdict(record), sort_keys=True) + "\n")
