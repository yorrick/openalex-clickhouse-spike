from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Mapping, Sequence
import hashlib
import json

from openalex_spike.manifest import ManifestFile


ALGORITHM = "cumulative-bytes-four-strata-v2"
STAGE1_BIAS_CAVEAT = (
    "Stage 1 seeds each stratum with a file no larger than one quarter of its "
    "target. This size conditioning favors smaller files and makes Stage 1 a "
    "correctness sample, not a representative performance sample."
)


@dataclass(frozen=True)
class SelectedFile:
    url: str
    content_length: int
    record_count: int
    updated_date: str
    stratum: int
    rank: str


def stable_rank(seed: str, url: str) -> str:
    return hashlib.sha256(f"{seed}\0{url}".encode()).hexdigest()


def _stratify(files: Sequence[ManifestFile], seed: str) -> tuple[SelectedFile, ...]:
    ordered = sorted(files, key=lambda file: (file.updated_date, file.url))
    total_bytes = sum(file.content_length for file in ordered)
    if total_bytes <= 0:
        raise ValueError("cannot sample an empty manifest")

    cumulative_bytes = 0
    selected_files = []
    for file in ordered:
        stratum = min(3, (4 * cumulative_bytes) // total_bytes)
        selected_files.append(
            SelectedFile(
                url=file.url,
                content_length=file.content_length,
                record_count=file.record_count,
                updated_date=file.updated_date,
                stratum=stratum,
                rank=stable_rank(seed, file.url),
            )
        )
        cumulative_bytes += file.content_length
    return tuple(selected_files)


def _stage1_seeds(
    queues: Mapping[int, Sequence[SelectedFile]], target: int
) -> tuple[SelectedFile, ...]:
    """Construct four-stratum coverage without consuming the target in one file."""
    max_seed_file_bytes = target // 4
    if max_seed_file_bytes <= 0:
        raise ValueError("Stage 1 target must be at least four bytes")
    seeds = []
    for stratum in range(4):
        eligible = [
            file
            for file in queues[stratum]
            if file.content_length <= max_seed_file_bytes
        ]
        if not eligible:
            raise ValueError(
                f"Stage 1 stratum {stratum} has no file at or below "
                f"the {max_seed_file_bytes}-byte coverage cap"
            )
        seeds.append(eligible[0])
    return tuple(seeds)


def stage1_coverage_metadata(
    files: Sequence[ManifestFile], target: int, seed: str
) -> dict[str, object]:
    """Describe the explicit Stage 1 coverage constraint and its sampling bias."""
    candidates = _stratify(files, seed)
    queues = {
        stratum: sorted(
            (file for file in candidates if file.stratum == stratum),
            key=lambda file: file.rank,
        )
        for stratum in range(4)
    }
    max_seed_file_bytes = int(target) // 4
    seeds = _stage1_seeds(queues, int(target))
    return {
        "scope": "first tier only",
        "max_seed_file_bytes": max_seed_file_bytes,
        "cap_derivation": "floor(first_tier_target_bytes / 4)",
        "bias_caveat": STAGE1_BIAS_CAVEAT,
        "strata": {
            str(stratum): {
                "eligible_files": sum(
                    file.content_length <= max_seed_file_bytes
                    for file in queues[stratum]
                ),
                "total_files": len(queues[stratum]),
                "seed_file": asdict(seeds[stratum]),
            }
            for stratum in range(4)
        },
    }


def select_nested(
    files: Sequence[ManifestFile], targets: Mapping[str, int], seed: str
) -> dict[str, tuple[SelectedFile, ...]]:
    """Select deterministic, byte-stratified tiers whose file sets are nested."""
    target_items = list(targets.items())
    target_values = [int(value) for _, value in target_items]
    if not target_values or target_values != sorted(target_values):
        raise ValueError("tier targets must be present and increasing")

    candidates = _stratify(files, seed)
    queues = {
        stratum: sorted(
            (file for file in candidates if file.stratum == stratum),
            key=lambda file: file.rank,
        )
        for stratum in range(4)
    }
    current: list[SelectedFile] = []
    used: set[str] = set()
    selected_by_tier: dict[str, tuple[SelectedFile, ...]] = {}

    first_tier_name, first_target = target_items[0]
    for chosen in _stage1_seeds(queues, int(first_target)):
        current.append(chosen)
        used.add(chosen.url)

    for tier_name, target in target_items:
        target = int(target)
        stratum_bytes = {
            stratum: sum(
                file.content_length for file in current if file.stratum == stratum
            )
            for stratum in range(4)
        }
        while sum(file.content_length for file in current) < target:
            available = {
                stratum: next(
                    (file for file in queues[stratum] if file.url not in used), None
                )
                for stratum in range(4)
            }
            available = {
                stratum: file for stratum, file in available.items() if file is not None
            }
            if not available:
                raise ValueError(f"manifest cannot satisfy tier {tier_name} ({target} bytes)")
            desired_per_stratum = target / 4
            chosen_stratum = max(
                available,
                key=lambda stratum: (desired_per_stratum - stratum_bytes[stratum], -stratum),
            )
            chosen = available[chosen_stratum]
            current.append(chosen)
            used.add(chosen.url)
            stratum_bytes[chosen_stratum] += chosen.content_length

        if tier_name == first_tier_name and {file.stratum for file in current} != {
            0,
            1,
            2,
            3,
        }:
            raise ValueError("Stage 1 cannot include all four cumulative-byte strata")
        actual_bytes = sum(file.content_length for file in current)
        largest_file = max(file.content_length for file in current)
        if actual_bytes - target > largest_file:
            raise ValueError(f"tier {tier_name} overshoot exceeds its largest file")
        selected_by_tier[tier_name] = tuple(current)

    return selected_by_tier


def write_selection(
    destination: Path,
    selection: Mapping[str, Sequence[SelectedFile]],
    targets: Mapping[str, int],
    seed: str,
    manifest_etag: str,
    manifest_sha256: str,
    manifest_files: Sequence[ManifestFile],
) -> None:
    first_tier, first_target = next(iter(targets.items()))
    document = {
        "algorithm": ALGORITHM,
        "seed": seed,
        "manifest": {"etag": manifest_etag, "sha256": manifest_sha256},
        "stage1_coverage_policy": {
            "tier": first_tier,
            **stage1_coverage_metadata(manifest_files, int(first_target), seed),
        },
        "tiers": {
            tier: {
                "target_bytes": int(targets[tier]),
                "actual_bytes": sum(file.content_length for file in files),
                "record_count": sum(file.record_count for file in files),
                "files": [asdict(file) for file in files],
            }
            for tier, files in selection.items()
        },
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
