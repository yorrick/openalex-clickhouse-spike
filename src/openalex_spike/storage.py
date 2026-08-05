from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from threading import Event, Thread
from time import monotonic, time
from typing import Callable
import json
import os


@dataclass(frozen=True)
class CapacityEstimate:
    output_rows: int
    native_bytes: int


@dataclass(frozen=True)
class StorageSample:
    timestamp: float
    table_bytes: dict[str, int]
    projection_bytes: dict[str, int]
    filesystem_bytes: int
    filesystem_vanished_files: int = 0


@dataclass(frozen=True)
class DirectoryUsage:
    allocated_bytes: int
    vanished_files: int


def estimate_works_derived(
    *,
    sample_work_rows: int,
    sample_output_rows: int,
    sample_native_bytes: int,
    full_work_rows: int,
) -> CapacityEstimate:
    if min(sample_work_rows, sample_output_rows, sample_native_bytes) <= 0:
        raise ValueError("sample counts and bytes must be positive")
    output_rows = round(full_work_rows * sample_output_rows / sample_work_rows)
    native_bytes = round(output_rows * sample_native_bytes / sample_output_rows)
    return CapacityEstimate(output_rows=output_rows, native_bytes=native_bytes)


def with_headroom(estimate: CapacityEstimate, *, fraction: float) -> CapacityEstimate:
    if fraction < 0:
        raise ValueError("headroom fraction cannot be negative")
    multiplier = 1 + fraction
    return CapacityEstimate(
        output_rows=estimate.output_rows,
        native_bytes=round(estimate.native_bytes * multiplier),
    )


def classify_capacity(required_bytes: int, *, available_bytes: int) -> str:
    utilization = required_bytes / available_bytes
    if utilization < 0.9:
        return "Likely fits"
    if utilization <= 1.0:
        return "Uncertain"
    return "Likely exceeds"


def estimate_stratum_range(estimates: list[CapacityEstimate]) -> dict[str, int]:
    if not estimates:
        raise ValueError("at least one stratum estimate is required")
    ordered = sorted(estimate.native_bytes for estimate in estimates)
    return {
        "low_bytes": ordered[0],
        "expected_bytes": ordered[(len(ordered) - 1) // 2],
        "high_bytes": ordered[-1],
    }


def complete_dimension_estimate(rows: int, native_bytes: int) -> CapacityEstimate:
    return CapacityEstimate(output_rows=rows, native_bytes=native_bytes)


def projection_estimate(base_native_bytes: int, observed_ratio: float) -> int:
    if observed_ratio < 0:
        raise ValueError("projection ratio cannot be negative")
    return round(base_native_bytes * observed_ratio)


def layout_bytes(
    base_bytes: int, projection_bytes: int, *, concurrent_generations: int
) -> int:
    if concurrent_generations not in {1, 2}:
        raise ValueError("only one- and two-generation layouts are modeled")
    return (base_bytes + projection_bytes) * concurrent_generations


def directory_allocated_usage(path: Path) -> DirectoryUsage:
    total = 0
    vanished_files = 0
    if not path.exists():
        return DirectoryUsage(allocated_bytes=0, vanished_files=0)

    def raise_walk_error(error: OSError) -> None:
        raise error

    for root, _, files in os.walk(path, onerror=raise_walk_error):
        for filename in files:
            try:
                stat = (Path(root) / filename).stat()
            except FileNotFoundError:
                vanished_files += 1
                continue
            total += stat.st_blocks * 512
    return DirectoryUsage(allocated_bytes=total, vanished_files=vanished_files)


def directory_allocated_bytes(path: Path) -> int:
    return directory_allocated_usage(path).allocated_bytes


def collect_storage_sample(
    query_json: Callable[[str], list[dict[str, object]]],
    *,
    database: str,
    clickhouse_data_dir: Path,
    filesystem_usage: DirectoryUsage | None = None,
) -> StorageSample:
    part_rows = query_json(
        "SELECT table, sum(bytes_on_disk) AS bytes "
        "FROM system.parts WHERE active AND database = "
        f"'{database}' GROUP BY table ORDER BY table"
    )
    projection_rows = query_json(
        "SELECT table, sum(bytes_on_disk) AS bytes "
        "FROM system.projection_parts WHERE active AND database = "
        f"'{database}' GROUP BY table ORDER BY table"
    )
    usage = filesystem_usage or directory_allocated_usage(clickhouse_data_dir)
    return StorageSample(
        timestamp=time(),
        table_bytes={str(row["table"]): int(row["bytes"]) for row in part_rows},
        projection_bytes={
            str(row["table"]): int(row["bytes"]) for row in projection_rows
        },
        filesystem_bytes=usage.allocated_bytes,
        filesystem_vanished_files=usage.vanished_files,
    )


class DecimatedFilesystemSampler:
    """Poll ClickHouse parts frequently and the host filesystem less often."""

    def __init__(
        self,
        query_json: Callable[[str], list[dict[str, object]]],
        *,
        database: str,
        clickhouse_data_dir: Path,
        filesystem_interval_seconds: float = 30.0,
        clock: Callable[[], float] = monotonic,
    ) -> None:
        self.query_json = query_json
        self.database = database
        self.clickhouse_data_dir = clickhouse_data_dir
        self.filesystem_interval_seconds = filesystem_interval_seconds
        self.clock = clock
        self._last_filesystem_at: float | None = None
        self._filesystem_usage: DirectoryUsage | None = None

    def __call__(self) -> StorageSample:
        now = self.clock()
        if (
            self._last_filesystem_at is None
            or now - self._last_filesystem_at >= self.filesystem_interval_seconds
        ):
            self._filesystem_usage = directory_allocated_usage(
                self.clickhouse_data_dir
            )
            self._last_filesystem_at = now
        return collect_storage_sample(
            self.query_json,
            database=self.database,
            clickhouse_data_dir=self.clickhouse_data_dir,
            filesystem_usage=self._filesystem_usage,
        )

    def final(self) -> StorageSample:
        return collect_storage_sample(
            self.query_json,
            database=self.database,
            clickhouse_data_dir=self.clickhouse_data_dir,
        )


class StorageMonitor:
    def __init__(
        self,
        sample: Callable[[], StorageSample],
        *,
        interval_seconds: float = 1.0,
        final_sample: Callable[[], StorageSample] | None = None,
    ) -> None:
        self.sample = sample
        self.interval_seconds = interval_seconds
        self.final_sample = final_sample or sample
        self.samples: list[StorageSample] = []
        self._stop = Event()
        self._error: BaseException | None = None
        self._thread: Thread | None = None

    def start(self) -> None:
        if self._thread is not None:
            raise RuntimeError("storage monitor already started")

        def poll() -> None:
            try:
                while not self._stop.is_set():
                    self.samples.append(self.sample())
                    self._stop.wait(self.interval_seconds)
            except BaseException as error:
                self._error = error
                self._stop.set()

        self._thread = Thread(target=poll, name="storage-monitor", daemon=True)
        self._thread.start()

    def stop(self) -> list[StorageSample]:
        if self._thread is None:
            raise RuntimeError("storage monitor was not started")
        self._stop.set()
        self._thread.join()
        if self._error is not None:
            raise RuntimeError("storage monitor failed") from self._error
        try:
            self.samples.append(self.final_sample())
        except BaseException as error:
            raise RuntimeError("storage monitor final sample failed") from error
        return list(self.samples)


def write_storage_samples(destination: Path, samples: list[StorageSample]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps([asdict(sample) for sample in samples], indent=2, sort_keys=True)
        + "\n"
    )
