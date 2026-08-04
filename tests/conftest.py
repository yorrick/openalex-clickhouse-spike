from pathlib import Path

import pytest

from openalex_spike.manifest import EntityManifest


@pytest.fixture
def fixture_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def works_manifest(fixture_dir: Path) -> EntityManifest:
    return EntityManifest.from_path(fixture_dir / "works-manifest.json")
