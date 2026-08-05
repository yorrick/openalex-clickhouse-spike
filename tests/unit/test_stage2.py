from pathlib import Path

import pytest

from openalex_spike.stage2 import (
    GIB,
    Stage2PrerequisiteError,
    build_run_identity,
    nested_stage2_tiers,
    require_complete_concurrency_samples,
    require_resume_identity,
    required_build_free_bytes,
    required_download_free_bytes,
    stage2_performance_verdict,
    stage2_local_verdict,
    worst_stage2_verdict,
)
from openalex_spike.config import VerdictThresholds


def test_max_tier_materializes_every_nested_stage2_tier():
    assert nested_stage2_tiers("stage2_large") == (
        "stage2_small",
        "stage2_medium",
        "stage2_large",
    )
    assert nested_stage2_tiers("stage2_medium") == (
        "stage2_small",
        "stage2_medium",
    )
    assert nested_stage2_tiers("stage1") == ("stage1",)


def test_disk_budget_keeps_raw_native_projection_merge_and_reserve_separate():
    assert required_download_free_bytes(
        remaining_object_bytes=100,
        maximum_raw_input_bytes=1_000,
    ) == 100 + 2_000 + 50 * GIB
    assert required_build_free_bytes(maximum_raw_input_bytes=1_000) == (
        2_000 + 50 * GIB
    )


def test_resume_identity_includes_memory_config_and_rendered_sql():
    base = {
        "run_id": "stage2",
        "memory_gib": 32,
        "tiers": ["stage2_small"],
        "selection_sha256": "selection",
        "download_state_sha256": "download",
        "config_sha256": "config-a",
        "rendered_sql_sha256": {"schema": "sql-a"},
    }
    recorded = build_run_identity(**base)
    require_resume_identity(recorded, build_run_identity(**base))

    changed = build_run_identity(**{**base, "config_sha256": "config-b"})
    with pytest.raises(Stage2PrerequisiteError, match="new --run-id"):
        require_resume_identity(recorded, changed)


def test_versioned_identity_pins_every_execution_resource():
    base = {
        "run_id": "resource-run",
        "memory_gib": 50,
        "tiers": ["stage2_large"],
        "selection_sha256": "selection",
        "download_state_sha256": "download",
        "config_sha256": "config",
        "rendered_sql_sha256": {"schema": "sql"},
    }
    execution = {
        "cpus": 16,
        "workers": 1,
        "query_threads": 8,
        "maximum_seconds": 18_000,
    }
    legacy = build_run_identity(**base)
    current = build_run_identity(**base, execution=execution)

    assert "identity_version" not in legacy
    assert current["identity_version"] == 2
    assert current["execution"] == execution
    for field in execution:
        changed = build_run_identity(
            **base,
            execution={**execution, field: execution[field] + 1},
        )
        with pytest.raises(Stage2PrerequisiteError, match="new --run-id"):
            require_resume_identity(current, changed)


def _thresholds() -> VerdictThresholds:
    return VerdictThresholds(
        minimum_ordinary_author_reference_coverage=0.999,
        minimum_samples=50,
        maximum_seconds=3600,
        pass_routine_p95_seconds=15,
        pass_join_p95_seconds=45,
        conditional_routine_p95_seconds=30,
        conditional_join_p95_seconds=120,
    )


def _concurrent_summary(
    *,
    routine_p95: float = 15,
    join_p95: float = 45,
    one_hop_p95: float = 10_000,
    insufficient: str | None = None,
    forced_verdict: str | None = None,
    server_restarted: bool = False,
) -> dict[str, object]:
    classes = {
        "routine": {
            "p95_seconds": routine_p95,
            "insufficient_sample": insufficient == "routine",
        },
        "join": {
            "p95_seconds": join_p95,
            "insufficient_sample": insufficient == "join",
        },
        "one_hop": {
            "p95_seconds": one_hop_p95,
            "insufficient_sample": insufficient == "one_hop",
        },
    }
    return {
        "classes": classes,
        "forced_verdict": forced_verdict,
        "verdict_cap": (
            "fail"
            if forced_verdict
            else "conditional"
            if insufficient
            else "pass"
        ),
        "server_restarted": server_restarted,
    }


@pytest.mark.parametrize(
    ("routine_p95", "join_p95", "expected"),
    [
        (15, 45, "pass"),
        (30, 120, "conditional"),
        (15.001, 45, "conditional"),
        (30.001, 45, "fail"),
        (15, 120.001, "fail"),
    ],
)
def test_performance_verdict_pins_exact_latency_boundaries(
    routine_p95: float, join_p95: float, expected: str
) -> None:
    assert (
        stage2_performance_verdict(
            _concurrent_summary(
                routine_p95=routine_p95,
                join_p95=join_p95,
            ),
            _thresholds(),
        )
        == expected
    )


def test_performance_verdict_consumes_existing_caps_and_restart_signal():
    assert (
        stage2_performance_verdict(
            _concurrent_summary(insufficient="one_hop"), _thresholds()
        )
        == "conditional"
    )
    assert (
        stage2_performance_verdict(
            _concurrent_summary(forced_verdict="fail"), _thresholds()
        )
        == "fail"
    )
    assert (
        stage2_performance_verdict(
            _concurrent_summary(server_restarted=True), _thresholds()
        )
        == "fail"
    )


def test_one_hop_has_no_invented_latency_ceiling():
    assert (
        stage2_performance_verdict(
            _concurrent_summary(one_hop_p95=10_000), _thresholds()
        )
        == "pass"
    )


def test_resource_comparison_rejects_under_sampled_evidence():
    with pytest.raises(Stage2PrerequisiteError, match="under-sampled.*one_hop"):
        require_complete_concurrency_samples(
            _concurrent_summary(insufficient="one_hop")
        )

    require_complete_concurrency_samples(_concurrent_summary())


def test_worst_tier_preserves_a_single_restart_failure():
    per_tier = [
        stage2_performance_verdict(_concurrent_summary(), _thresholds()),
        stage2_performance_verdict(
            _concurrent_summary(server_restarted=True), _thresholds()
        ),
    ]
    assert worst_stage2_verdict(per_tier) == "fail"
    assert (
        stage2_local_verdict(
            memory_gib=32,
            performance_verdict=worst_stage2_verdict(per_tier),
        )
        == "fail"
    )


def test_32_gib_success_is_conditional_and_unknown_memory_is_refused():
    assert (
        stage2_local_verdict(memory_gib=32, performance_verdict="pass")
        == "conditional"
    )
    assert (
        stage2_local_verdict(memory_gib=50, performance_verdict="conditional")
        == "conditional"
    )
    with pytest.raises(Stage2PrerequisiteError, match="unsupported"):
        stage2_local_verdict(memory_gib=64, performance_verdict="pass")
