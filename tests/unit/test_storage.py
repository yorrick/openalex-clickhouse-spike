from threading import Event

import pytest

from openalex_spike.storage import (
    CapacityEstimate,
    StorageMonitor,
    StorageSample,
    classify_capacity,
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
