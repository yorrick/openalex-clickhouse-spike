import errno
from pathlib import Path
from threading import Event

import pytest

from openalex_spike.storage import (
    CapacityEstimate,
    DecimatedFilesystemSampler,
    DirectoryUsage,
    StorageMonitor,
    StorageSample,
    classify_capacity,
    collect_storage_sample,
    directory_allocated_usage,
    estimate_works_derived,
    with_headroom,
)


def test_citation_edges_scale_by_edges_per_work_not_raw_bytes():
    estimate = estimate_works_derived(
        sample_work_rows=1_000,
        sample_output_rows=25_000,
        sample_native_bytes=200_000,
        full_work_rows=510_372_821,
    )
    assert estimate.output_rows == 12_759_320_525
    assert estimate.native_bytes == 102_074_564_200


def test_capacity_classification_uses_conservative_headroom():
    estimate = CapacityEstimate(output_rows=100, native_bytes=20_000)
    conservative = with_headroom(estimate, fraction=1.0)
    assert conservative.native_bytes == 40_000
    assert classify_capacity(40_000, available_bytes=50_000) == "Likely fits"
    assert classify_capacity(50_000, available_bytes=50_000) == "Uncertain"
    assert classify_capacity(60_000, available_bytes=50_000) == "Likely exceeds"


def test_storage_monitor_forces_a_final_sample():
    sampled = Event()
    call_count = 0

    def sample():
        nonlocal call_count
        call_count += 1
        sampled.set()
        return StorageSample(float(call_count), {}, {}, call_count)

    monitor = StorageMonitor(sample, interval_seconds=60)
    monitor.start()
    assert sampled.wait(1)
    samples = monitor.stop()

    assert len(samples) == 2
    assert samples[-1].filesystem_bytes == 2


def test_storage_monitor_wraps_final_sample_failure():
    sampled = Event()
    call_count = 0

    def sample():
        nonlocal call_count
        call_count += 1
        if call_count == 2:
            raise ValueError("final probe failed")
        sampled.set()
        return StorageSample(float(call_count), {}, {}, call_count)

    monitor = StorageMonitor(sample, interval_seconds=60)
    monitor.start()
    assert sampled.wait(1)

    with pytest.raises(RuntimeError, match="final sample failed") as captured:
        monitor.stop()
    assert isinstance(captured.value.__cause__, ValueError)


def test_storage_monitor_uses_explicit_exact_final_sample():
    sampled = Event()

    def sample():
        sampled.set()
        return StorageSample(1.0, {}, {}, 10)

    monitor = StorageMonitor(
        sample,
        interval_seconds=60,
        final_sample=lambda: StorageSample(2.0, {}, {}, 20),
    )
    monitor.start()
    assert sampled.wait(1)
    samples = monitor.stop()

    assert [item.filesystem_bytes for item in samples] == [10, 20]


def test_storage_sample_new_telemetry_is_positionally_compatible():
    sample = StorageSample(1.0, {}, {}, 10)

    assert sample.filesystem_vanished_files == 0
    assert sample.filesystem_vanished_directories == 0


def test_directory_usage_counts_only_children_that_vanish_after_listing(
    tmp_path, monkeypatch
):
    stable = tmp_path / "stable.bin"
    stable.write_bytes(b"stable")
    vanished = tmp_path / "vanished.bin"
    original_stat = Path.stat

    monkeypatch.setattr(
        "openalex_spike.storage.os.walk",
        lambda path, onerror: [(str(tmp_path), [], [stable.name, vanished.name])],
    )

    def stat(path, *args, **kwargs):
        if path == vanished:
            raise FileNotFoundError(path)
        return original_stat(path, *args, **kwargs)

    monkeypatch.setattr(Path, "stat", stat)

    usage = directory_allocated_usage(tmp_path)

    assert usage == DirectoryUsage(
        allocated_bytes=original_stat(stable).st_blocks * 512,
        vanished_files=1,
    )


def test_directory_usage_does_not_suppress_permission_errors(tmp_path, monkeypatch):
    protected = tmp_path / "protected.bin"
    protected.write_bytes(b"protected")
    original_stat = Path.stat
    monkeypatch.setattr(
        "openalex_spike.storage.os.walk",
        lambda path, onerror: [(str(tmp_path), [], [protected.name])],
    )

    def stat(path, *args, **kwargs):
        if path == protected:
            raise PermissionError(path)
        return original_stat(path, *args, **kwargs)

    monkeypatch.setattr(Path, "stat", stat)

    with pytest.raises(PermissionError):
        directory_allocated_usage(tmp_path)


def test_directory_usage_still_raises_when_root_vanishes(tmp_path, monkeypatch):
    def failed_walk(path, onerror):
        onerror(FileNotFoundError(errno.ENOENT, "vanished", str(path)))
        return []

    monkeypatch.setattr("openalex_spike.storage.os.walk", failed_walk)

    with pytest.raises(FileNotFoundError):
        directory_allocated_usage(tmp_path)


def test_directory_usage_counts_vanished_descendant_directory(tmp_path, monkeypatch):
    stable = tmp_path / "stable.bin"
    stable.write_bytes(b"stable")
    vanished = tmp_path / "tmp_insert_202608_10_10_0"

    def walked(path, onerror):
        onerror(FileNotFoundError(errno.ENOENT, "vanished", str(vanished)))
        return [(str(tmp_path), [], [stable.name])]

    monkeypatch.setattr("openalex_spike.storage.os.walk", walked)

    usage = directory_allocated_usage(tmp_path)

    assert usage == DirectoryUsage(
        allocated_bytes=stable.stat().st_blocks * 512,
        vanished_files=0,
        vanished_directories=1,
    )


def test_directory_usage_does_not_suppress_walk_permission_errors(
    tmp_path, monkeypatch
):
    def failed_walk(path, onerror):
        onerror(
            PermissionError(
                errno.EACCES,
                "permission denied",
                str(tmp_path / "protected"),
            )
        )
        return []

    monkeypatch.setattr("openalex_spike.storage.os.walk", failed_walk)

    with pytest.raises(PermissionError):
        directory_allocated_usage(tmp_path)


def test_directory_usage_does_not_suppress_other_walk_oserrors(
    tmp_path, monkeypatch
):
    def failed_walk(path, onerror):
        onerror(OSError(errno.EIO, "I/O error", str(tmp_path / "part")))
        return []

    monkeypatch.setattr("openalex_spike.storage.os.walk", failed_walk)

    with pytest.raises(OSError) as captured:
        directory_allocated_usage(tmp_path)
    assert captured.value.errno == errno.EIO


def test_directory_usage_separates_vanished_files_and_directories(
    tmp_path, monkeypatch
):
    vanished_file = tmp_path / "checksums.txt"
    vanished_directory = tmp_path / "tmp_insert_202608_10_10_0"
    original_stat = Path.stat

    def walked(path, onerror):
        onerror(
            FileNotFoundError(
                errno.ENOENT,
                "vanished",
                str(vanished_directory),
            )
        )
        return [(str(tmp_path), [], [vanished_file.name])]

    def stat(path, *args, **kwargs):
        if path == vanished_file:
            raise FileNotFoundError(path)
        return original_stat(path, *args, **kwargs)

    monkeypatch.setattr("openalex_spike.storage.os.walk", walked)
    monkeypatch.setattr(Path, "stat", stat)

    usage = directory_allocated_usage(tmp_path)

    assert usage.vanished_files == 1
    assert usage.vanished_directories == 1


def test_storage_monitor_final_sample_records_vanished_file(tmp_path, monkeypatch):
    vanished = tmp_path / "merged-part.bin"
    original_stat = Path.stat
    monkeypatch.setattr(
        "openalex_spike.storage.os.walk",
        lambda path, onerror: [(str(tmp_path), [], [vanished.name])],
    )

    def stat(path, *args, **kwargs):
        if path == vanished:
            raise FileNotFoundError(path)
        return original_stat(path, *args, **kwargs)

    monkeypatch.setattr(Path, "stat", stat)
    sampled = Event()

    def sample():
        sampled.set()
        return StorageSample(1.0, {}, {}, 0)

    monitor = StorageMonitor(
        sample,
        interval_seconds=60,
        final_sample=lambda: collect_storage_sample(
            lambda sql: [],
            database="openalex_stage2",
            clickhouse_data_dir=tmp_path,
        ),
    )
    monitor.start()
    assert sampled.wait(1)

    samples = monitor.stop()

    assert samples[-1].filesystem_bytes == 0
    assert samples[-1].filesystem_vanished_files == 1


def test_storage_monitor_final_sample_records_vanished_directory(
    tmp_path, monkeypatch
):
    vanished = tmp_path / "tmp_insert_202608_10_10_0"

    def walked(path, onerror):
        onerror(FileNotFoundError(errno.ENOENT, "vanished", str(vanished)))
        return []

    monkeypatch.setattr("openalex_spike.storage.os.walk", walked)
    sampled = Event()

    def sample():
        sampled.set()
        return StorageSample(1.0, {}, {}, 0)

    monitor = StorageMonitor(
        sample,
        interval_seconds=60,
        final_sample=lambda: collect_storage_sample(
            lambda sql: [],
            database="openalex_stage2",
            clickhouse_data_dir=tmp_path,
        ),
    )
    monitor.start()
    assert sampled.wait(1)

    samples = monitor.stop()

    assert samples[-1].filesystem_bytes == 0
    assert samples[-1].filesystem_vanished_directories == 1


def test_decimated_sampler_reuses_filesystem_value_between_fast_part_polls(
    tmp_path, monkeypatch
):
    clock_values = iter([0.0, 1.0, 31.0])
    filesystem_calls = []
    monkeypatch.setattr(
        "openalex_spike.storage.directory_allocated_usage",
        lambda path: filesystem_calls.append(path)
        or DirectoryUsage(
            len(filesystem_calls) * 100,
            len(filesystem_calls),
            len(filesystem_calls) * 10,
        ),
    )
    sampler = DecimatedFilesystemSampler(
        lambda sql: [],
        database="openalex_stage2",
        clickhouse_data_dir=tmp_path,
        clock=lambda: next(clock_values),
    )

    first = sampler()
    cached = sampler()
    refreshed = sampler()

    assert (first.filesystem_bytes, first.filesystem_vanished_files) == (100, 1)
    assert (cached.filesystem_bytes, cached.filesystem_vanished_files) == (100, 1)
    assert (refreshed.filesystem_bytes, refreshed.filesystem_vanished_files) == (
        200,
        2,
    )
    assert first.filesystem_vanished_directories == 10
    assert cached.filesystem_vanished_directories == 10
    assert refreshed.filesystem_vanished_directories == 20
    assert filesystem_calls == [tmp_path, tmp_path]
