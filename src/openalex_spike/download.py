from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Mapping, Sequence
import errno
import hashlib
import json
import os
import time

import httpx
import pyarrow.parquet as pq

from openalex_spike.manifest import (
    SELECTED_SMALL_ENTITIES,
    EntityManifest,
    ManifestFile,
)
from openalex_spike.sampling import SelectedFile


FileRecord = ManifestFile | SelectedFile
RETRY_DELAYS_SECONDS = (2, 8, 30)


def public_https(url: str) -> str:
    prefix = "s3://openalex/"
    if not url.startswith(prefix):
        raise ValueError(f"unsupported OpenAlex object URL: {url}")
    return f"https://openalex.s3.amazonaws.com/{url.removeprefix(prefix)}"


def object_path(objects_dir: Path, url: str) -> Path:
    digest = hashlib.sha256(url.encode()).hexdigest()
    return objects_dir / f"{digest}.parquet"


def _stream_download(
    client: httpx.Client, file: FileRecord, destination: Path
) -> Path:
    partial = destination.with_name(f"{destination.name}.partial")
    partial.unlink(missing_ok=True)
    byte_count = 0
    try:
        with client.stream("GET", public_https(file.url)) as response:
            response.raise_for_status()
            with partial.open("wb") as output:
                for chunk in response.iter_bytes():
                    output.write(chunk)
                    byte_count += len(chunk)
                output.flush()
                os.fsync(output.fileno())
        if byte_count != file.content_length:
            raise ValueError(
                f"download length mismatch for {file.url}: "
                f"{byte_count} != {file.content_length}"
            )
        os.replace(partial, destination)
        return destination
    except Exception:
        partial.unlink(missing_ok=True)
        raise


def download_one(file: FileRecord, objects_dir: Path) -> Path:
    """Download one object, retrying the same URL only after fixed delays."""
    objects_dir.mkdir(parents=True, exist_ok=True)
    destination = object_path(objects_dir, file.url)
    if destination.exists():
        if destination.stat().st_size != file.content_length:
            raise ValueError(f"existing object length mismatch: {destination}")
        return destination

    failures: list[Exception] = []
    # One initial attempt followed by exactly three retries at the fixed delays.
    for attempt in range(len(RETRY_DELAYS_SECONDS) + 1):
        try:
            with httpx.Client(follow_redirects=True, timeout=120) as client:
                return _stream_download(client, file, destination)
        except (httpx.HTTPError, OSError, ValueError) as error:
            failures.append(error)
            if attempt == len(RETRY_DELAYS_SECONDS):
                break
            time.sleep(RETRY_DELAYS_SECONDS[attempt])
    raise RuntimeError(
        f"failed to download {file.url} after {len(failures)} attempts"
    ) from failures[-1]


def download_files(
    files: Sequence[FileRecord], objects_dir: Path
) -> dict[str, Path]:
    unique = {file.url: file for file in files}
    results: dict[str, Path] = {}
    with ThreadPoolExecutor(max_workers=min(4, max(1, len(unique)))) as executor:
        futures = {
            executor.submit(download_one, file, objects_dir): url
            for url, file in unique.items()
        }
        for future in as_completed(futures):
            url = futures[future]
            results[url] = future.result()
    return results


def parquet_row_count(path: Path) -> int:
    metadata = pq.ParquetFile(path).metadata
    if metadata is None:
        raise ValueError(f"Parquet footer is missing: {path}")
    return metadata.num_rows


def verify_downloads(
    selections: Mapping[str, Sequence[FileRecord]],
    object_paths: Mapping[str, Path],
    destination: Path,
) -> dict:
    tiers = {}
    for tier, files in selections.items():
        verified_files = []
        for file in files:
            path = object_paths[file.url]
            actual_bytes = path.stat().st_size
            if actual_bytes != file.content_length:
                raise ValueError(
                    f"verified length mismatch for {file.url}: "
                    f"{actual_bytes} != {file.content_length}"
                )
            actual_rows = parquet_row_count(path)
            if actual_rows != file.record_count:
                raise ValueError(
                    f"Parquet row mismatch for {file.url}: "
                    f"{actual_rows} != {file.record_count}"
                )
            verified_files.append(
                {
                    "url": file.url,
                    "path": str(path),
                    "content_length": actual_bytes,
                    "record_count": actual_rows,
                }
            )
        tiers[tier] = {
            "content_length": sum(item["content_length"] for item in verified_files),
            "record_count": sum(item["record_count"] for item in verified_files),
            "files": verified_files,
        }
    result = {"tiers": tiers}
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def materialize_tier_links(
    raw_root: Path,
    selections: Mapping[str, Sequence[FileRecord]],
    object_paths: Mapping[str, Path],
    *,
    entity: str = "works",
) -> list[Path]:
    links = []
    for tier, files in selections.items():
        tier_dir = raw_root / "tiers" / tier / entity
        tier_dir.mkdir(parents=True, exist_ok=True)
        for file in files:
            source = object_paths[file.url]
            destination = tier_dir / source.name
            if destination.exists():
                if destination.stat().st_ino != source.stat().st_ino:
                    raise ValueError(f"tier path is not the expected hard link: {destination}")
            else:
                try:
                    os.link(source, destination)
                except OSError as error:
                    if error.errno == errno.EXDEV:
                        raise RuntimeError(
                            "object and tier directories are on different filesystems; "
                            "copy fallback is disabled"
                        ) from error
                    raise
            links.append(destination)
    return links


def materialize_supporting_entities(
    raw_root: Path,
    tier_names: Sequence[str],
    manifests: Mapping[str, EntityManifest],
    object_paths: Mapping[str, Path],
    *,
    include_complete_authors: bool,
) -> list[Path]:
    """Link only the explicitly approved complete supporting entities."""
    approved = set(SELECTED_SMALL_ENTITIES)
    if include_complete_authors:
        approved.add("authors")
    links = []
    for entity in sorted(approved & manifests.keys()):
        selections = {tier: manifests[entity].files for tier in tier_names}
        links.extend(
            materialize_tier_links(
                raw_root, selections, object_paths, entity=entity
            )
        )
    return links
