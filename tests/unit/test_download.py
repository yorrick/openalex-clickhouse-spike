from dataclasses import replace
import json

import pyarrow as pa
import pyarrow.parquet as pq

from openalex_spike.download import (
    materialize_supporting_entities,
    materialize_tier_links,
    public_https,
    verify_downloads,
)
from openalex_spike.manifest import EntityManifest, ManifestFile


def test_public_s3_url_conversion():
    assert (
        public_https("s3://openalex/data/parquet/works/x.parquet")
        == "https://openalex.s3.amazonaws.com/data/parquet/works/x.parquet"
    )


def test_materialized_tiers_share_inode(tmp_path, selected_file):
    object_path = tmp_path / "objects" / "abc.parquet"
    object_path.parent.mkdir()
    object_path.write_bytes(b"PAR1fixturePAR1")
    links = materialize_tier_links(
        tmp_path,
        {"small": [selected_file]},
        {selected_file.url: object_path},
    )
    assert links[0].stat().st_ino == object_path.stat().st_ino


def test_verify_downloads_checks_parquet_rows_and_writes_totals(
    tmp_path, selected_file
):
    parquet_path = tmp_path / "objects" / "fixture.parquet"
    parquet_path.parent.mkdir()
    pq.write_table(pa.table({"id": ["W1"]}), parquet_path)
    selected_file = replace(
        selected_file,
        content_length=parquet_path.stat().st_size,
        record_count=1,
    )
    output = tmp_path / "verification.json"
    result = verify_downloads(
        {"stage1": [selected_file]}, {selected_file.url: parquet_path}, output
    )
    assert result["tiers"]["stage1"]["record_count"] == 1
    assert json.loads(output.read_text()) == result


def test_supporting_entities_include_authors_and_dimensions_but_not_awards(tmp_path):
    manifests = {}
    objects = {}
    for entity in ("authors", "institutions", "awards"):
        file = ManifestFile(
            url=f"s3://openalex/data/parquet/{entity}/updated_date=2026-01-01/x.parquet",
            content_length=4,
            record_count=1,
        )
        manifests[entity] = EntityManifest("2026-06-26", entity, 4, 1, (file,))
        path = tmp_path / "objects" / f"{entity}.parquet"
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(b"PAR1")
        objects[file.url] = path

    links = materialize_supporting_entities(
        tmp_path,
        ["stage1"],
        manifests,
        objects,
        include_complete_authors=True,
    )

    assert {path.parent.name for path in links} == {"authors", "institutions"}
    assert not (tmp_path / "tiers" / "stage1" / "awards").exists()
