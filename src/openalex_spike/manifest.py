from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
import hashlib
import json
import os

import httpx


SELECTED_SMALL_ENTITIES = (
    "institutions",
    "sources",
    "publishers",
    "funders",
    "topics",
    "subfields",
    "fields",
    "domains",
    "concepts",
    "keywords",
    "continents",
    "countries",
    "institution-types",
    "languages",
    "licenses",
    "sdgs",
    "source-types",
    "work-types",
)


@dataclass(frozen=True)
class ManifestFile:
    url: str
    content_length: int
    record_count: int

    @property
    def updated_date(self) -> str:
        marker = "updated_date="
        if marker not in self.url:
            raise ValueError(f"missing updated_date in {self.url}")
        return self.url.split(marker, 1)[1].split("/", 1)[0]


@dataclass(frozen=True)
class EntityManifest:
    date: str
    entity: str
    content_length: int
    record_count: int
    files: tuple[ManifestFile, ...]

    @classmethod
    def from_path(cls, path: Path) -> "EntityManifest":
        raw = json.loads(path.read_text())
        files = tuple(
            ManifestFile(
                url=item["url"],
                content_length=int(item["meta"]["content_length"]),
                record_count=int(item["meta"]["record_count"]),
            )
            for item in raw["files"]
        )
        if sum(file.content_length for file in files) != int(raw["content_length"]):
            raise ValueError("entity file bytes do not reconcile")
        if sum(file.record_count for file in files) != int(raw["record_count"]):
            raise ValueError("entity record counts do not reconcile")
        return cls(
            date=raw["date"],
            entity=raw["entity"],
            content_length=int(raw["content_length"]),
            record_count=int(raw["record_count"]),
            files=files,
        )


def reconcile_entities(path: Path) -> int:
    raw = json.loads(path.read_text())
    actual = sum(int(entity["content_length"]) for entity in raw["entities"])
    expected = int(raw["meta"]["content_length"])
    if actual != expected:
        raise ValueError(f"combined manifest mismatch: {actual} != {expected}")
    return actual


def pin_url(client: httpx.Client, url: str, destination: Path) -> dict[str, Any]:
    """Download a manifest and pin its transport and content identity."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    data_tmp = destination.with_name(f"{destination.name}.tmp")
    metadata_path = destination.with_name(f"{destination.name}.metadata.json")
    metadata_tmp = metadata_path.with_name(f"{metadata_path.name}.tmp")

    try:
        with client.stream("GET", url) as response:
            response.raise_for_status()
            etag = response.headers.get("ETag")
            if not etag:
                raise ValueError(f"manifest response has no ETag: {url}")
            digest = hashlib.sha256()
            byte_count = 0
            with data_tmp.open("wb") as output:
                for chunk in response.iter_bytes():
                    output.write(chunk)
                    digest.update(chunk)
                    byte_count += len(chunk)
                output.flush()
                os.fsync(output.fileno())

            declared_length = response.headers.get("Content-Length")
            if declared_length is not None and byte_count != int(declared_length):
                raise ValueError(
                    f"manifest length mismatch for {url}: {byte_count} != {declared_length}"
                )
            metadata = {
                "url": url,
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "etag": etag,
                "last_modified": response.headers.get("Last-Modified"),
                "content_length": byte_count,
                "sha256": digest.hexdigest(),
            }
            with metadata_tmp.open("w") as output:
                json.dump(metadata, output, indent=2, sort_keys=True)
                output.write("\n")
                output.flush()
                os.fsync(output.fileno())
            os.replace(data_tmp, destination)
            os.replace(metadata_tmp, metadata_path)
            return metadata
    except Exception:
        data_tmp.unlink(missing_ok=True)
        metadata_tmp.unlink(missing_ok=True)
        raise


def reconcile_pinned_manifests(
    combined_path: Path, entity_paths: Iterable[Path]
) -> dict[str, EntityManifest]:
    """Require pinned entity totals to match their combined-manifest entries."""
    combined = json.loads(combined_path.read_text())
    expected = {item["entity"]: item for item in combined["entities"]}
    manifests: dict[str, EntityManifest] = {}
    for path in entity_paths:
        manifest = EntityManifest.from_path(path)
        if manifest.entity not in expected:
            raise ValueError(f"{manifest.entity} absent from combined manifest")
        combined_entity = expected[manifest.entity]
        if manifest.date != combined["date"]:
            raise ValueError(f"manifest date mismatch for {manifest.entity}")
        if manifest.content_length != int(combined_entity["content_length"]):
            raise ValueError(f"manifest byte mismatch for {manifest.entity}")
        if manifest.record_count != int(combined_entity["record_count"]):
            raise ValueError(f"manifest row mismatch for {manifest.entity}")
        manifests[manifest.entity] = manifest
    return manifests


def entity_manifest_url(entity: str) -> str:
    return f"https://openalex.s3.amazonaws.com/data/parquet/{entity}/manifest.json"


def pin_manifest_set(
    destination: Path,
    combined_url: str,
    *,
    include_authors: bool,
    client: httpx.Client | None = None,
) -> dict[str, EntityManifest]:
    """Pin the combined and all manifests required by the experiment."""
    entities = ["works", *SELECTED_SMALL_ENTITIES]
    if include_authors:
        entities.append("authors")
    owns_client = client is None
    http_client = client or httpx.Client(follow_redirects=True, timeout=120)
    try:
        combined_path = destination / "combined-manifest.json"
        pin_url(http_client, combined_url, combined_path)
        entity_paths = []
        for entity in entities:
            path = destination / f"{entity}-manifest.json"
            pin_url(http_client, entity_manifest_url(entity), path)
            entity_paths.append(path)
        reconcile_entities(combined_path)
        return reconcile_pinned_manifests(combined_path, entity_paths)
    finally:
        if owns_client:
            http_client.close()
