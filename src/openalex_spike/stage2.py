from __future__ import annotations

from pathlib import Path
from shutil import disk_usage
from typing import Mapping, Sequence
import hashlib
import json


STAGE2_TIERS = ("stage2_small", "stage2_medium", "stage2_large")
GIB = 1 << 30
STAGE2_DISK_RESERVE_BYTES = 50 * GIB


class Stage2PrerequisiteError(RuntimeError):
    pass


def nested_stage2_tiers(requested_tier: str) -> tuple[str, ...]:
    if requested_tier == "stage1":
        return (requested_tier,)
    if requested_tier not in STAGE2_TIERS:
        raise ValueError(f"unsupported tier: {requested_tier}")
    return STAGE2_TIERS[: STAGE2_TIERS.index(requested_tier) + 1]


def maximum_input_bytes(
    selection: Mapping[str, object],
    pin_state: Mapping[str, object],
) -> int:
    tiers = selection["tiers"]
    entities = pin_state["entities"]
    large = tiers["stage2_large"]
    authors = entities["authors"]
    supporting = sum(
        int(document["content_length"])
        for name, document in entities.items()
        if name not in {"authors", "works"}
    )
    return (
        sum(int(item["content_length"]) for item in large["files"])
        + int(authors["content_length"])
        + supporting
    )


def required_download_free_bytes(
    *, remaining_object_bytes: int, maximum_raw_input_bytes: int
) -> int:
    if remaining_object_bytes < 0 or maximum_raw_input_bytes <= 0:
        raise ValueError("disk-budget inputs must be non-negative")
    return (
        remaining_object_bytes
        + (2 * maximum_raw_input_bytes)
        + STAGE2_DISK_RESERVE_BYTES
    )


def required_build_free_bytes(*, maximum_raw_input_bytes: int) -> int:
    if maximum_raw_input_bytes <= 0:
        raise ValueError("maximum raw input must be positive")
    return (2 * maximum_raw_input_bytes) + STAGE2_DISK_RESERVE_BYTES


def require_free_space(path: Path, *, required_bytes: int, purpose: str) -> int:
    available = disk_usage(path).free
    if available < required_bytes:
        raise Stage2PrerequisiteError(
            f"insufficient free space for {purpose}: "
            f"requires {required_bytes:,} bytes, found {available:,} bytes"
        )
    return available


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_run_identity(
    *,
    run_id: str,
    memory_gib: int,
    tiers: Sequence[str],
    selection_sha256: str,
    download_state_sha256: str,
    config_sha256: str,
    rendered_sql_sha256: Mapping[str, str],
) -> dict[str, object]:
    document: dict[str, object] = {
        "run_id": run_id,
        "memory_gib": memory_gib,
        "tiers": list(tiers),
        "selection_sha256": selection_sha256,
        "download_state_sha256": download_state_sha256,
        "config_sha256": config_sha256,
        "rendered_sql_sha256": dict(sorted(rendered_sql_sha256.items())),
    }
    encoded = json.dumps(document, separators=(",", ":"), sort_keys=True).encode()
    document["sha256"] = hashlib.sha256(encoded).hexdigest()
    return document


def require_resume_identity(
    recorded: Mapping[str, object], current: Mapping[str, object]
) -> None:
    if recorded != current:
        raise Stage2PrerequisiteError(
            "Stage 2 resume identity changed; use an explicit new --run-id"
        )


def artifact_hashes(paths: Sequence[Path], *, root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): file_sha256(path)
        for path in sorted(paths)
    }


def verify_artifact_hashes(
    hashes: Mapping[str, str], *, root: Path
) -> None:
    for relative, expected in hashes.items():
        path = root / relative
        if not path.exists() or file_sha256(path) != expected:
            raise Stage2PrerequisiteError(
                f"Stage 2 resume artifact changed or is missing: {path}"
            )


def stage2_local_verdict(
    *, memory_gib: int, first_error: str | None, server_restarted: bool
) -> str:
    if first_error or server_restarted:
        return "fail"
    if memory_gib == 32:
        return "conditional"
    return "pass"
