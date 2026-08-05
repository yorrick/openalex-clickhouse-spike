from __future__ import annotations

from pathlib import Path
from shutil import disk_usage
from typing import Mapping, Sequence
import hashlib
import json

from openalex_spike.config import VerdictThresholds


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


VERDICT_SEVERITY = {"pass": 0, "conditional": 1, "fail": 2}


def worst_stage2_verdict(verdicts: Sequence[str]) -> str:
    if not verdicts:
        raise ValueError("at least one Stage 2 verdict is required")
    try:
        return max(verdicts, key=VERDICT_SEVERITY.__getitem__)
    except KeyError as error:
        raise ValueError(f"unsupported Stage 2 verdict: {error.args[0]}") from error


def stage2_performance_verdict(
    summary: Mapping[str, object], thresholds: VerdictThresholds
) -> str:
    forced = summary.get("forced_verdict")
    cap = summary.get("verdict_cap")
    if forced not in {None, "fail"}:
        raise ValueError(f"unsupported forced verdict: {forced}")
    if cap not in {"pass", "conditional", "fail"}:
        raise ValueError(f"unsupported concurrency verdict cap: {cap}")
    if forced == "fail" or cap == "fail" or bool(summary.get("server_restarted")):
        return "fail"

    classes = summary.get("classes")
    if not isinstance(classes, Mapping):
        raise ValueError("concurrency summary is missing class evidence")
    verdict = "conditional" if cap == "conditional" else "pass"
    latency_thresholds = {
        "routine": (
            thresholds.pass_routine_p95_seconds,
            thresholds.conditional_routine_p95_seconds,
        ),
        "join": (
            thresholds.pass_join_p95_seconds,
            thresholds.conditional_join_p95_seconds,
        ),
    }
    for query_class, (pass_ceiling, conditional_ceiling) in latency_thresholds.items():
        evidence = classes.get(query_class)
        if not isinstance(evidence, Mapping):
            raise ValueError(f"concurrency summary is missing {query_class} evidence")
        if bool(evidence.get("insufficient_sample")):
            continue
        p95 = evidence.get("p95_seconds")
        if p95 is None:
            raise ValueError(f"sampled {query_class} class has no p95")
        duration = float(p95)
        if duration > conditional_ceiling:
            return "fail"
        if duration > pass_ceiling:
            verdict = "conditional"
    return verdict


def stage2_local_verdict(*, memory_gib: int, performance_verdict: str) -> str:
    if memory_gib not in {32, 50}:
        raise Stage2PrerequisiteError(
            f"unsupported Stage 2 memory envelope: {memory_gib} GiB"
        )
    if performance_verdict not in VERDICT_SEVERITY:
        raise ValueError(f"unsupported performance verdict: {performance_verdict}")
    if performance_verdict == "fail":
        return "fail"
    if memory_gib == 32 or performance_verdict == "conditional":
        return "conditional"
    return "pass"
