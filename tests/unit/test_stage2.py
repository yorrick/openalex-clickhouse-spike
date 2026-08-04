from pathlib import Path

import pytest

from openalex_spike.stage2 import (
    GIB,
    Stage2PrerequisiteError,
    build_run_identity,
    nested_stage2_tiers,
    require_resume_identity,
    required_build_free_bytes,
    required_download_free_bytes,
    stage2_local_verdict,
)


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


def test_32_gib_success_is_conditional_but_errors_still_fail():
    assert (
        stage2_local_verdict(
            memory_gib=32, first_error=None, server_restarted=False
        )
        == "conditional"
    )
    assert (
        stage2_local_verdict(
            memory_gib=32, first_error="query failed", server_restarted=False
        )
        == "fail"
    )
