from pathlib import Path

import pytest

from openalex_spike.manifest import EntityManifest
from openalex_spike.sampling import SelectedFile


@pytest.fixture
def fixture_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def works_manifest(fixture_dir: Path) -> EntityManifest:
    return EntityManifest.from_path(fixture_dir / "works-manifest.json")


@pytest.fixture
def selected_file() -> SelectedFile:
    return SelectedFile(
        url="s3://openalex/data/parquet/works/updated_date=2022-07-31/part_0000.parquet",
        content_length=15,
        record_count=1,
        updated_date="2022-07-31",
        stratum=2,
        rank="fixture-rank",
    )
