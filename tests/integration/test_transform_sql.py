import json
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from openalex_spike.clickhouse import ClickHouseService


DATABASE = "openalex_spike"


def _write_parquet_fixtures(raw_root: Path) -> None:
    fixtures = raw_root / "fixtures"
    for entity in ("works", "institutions", "sources", "topics"):
        (fixtures / entity).mkdir(parents=True, exist_ok=True)

    works = [
        {
            "id": "https://openalex.org/W1",
            "publication_year": 2020,
            "type": "article",
            "primary_location": {"source": {"id": "https://openalex.org/S1"}},
            "open_access": {"is_oa": True},
            "is_xpac": False,
            "cited_by_count": 3,
            "primary_topic": {"id": "https://openalex.org/T1"},
            "referenced_works": [
                "https://openalex.org/W2",
                "https://openalex.org/W2",
                "https://openalex.org/W3",
            ],
            "authorships": [
                {
                    "author": {
                        "id": "https://openalex.org/A1",
                        "display_name": "Ada Author",
                        "orcid": "https://orcid.org/0000-0001",
                    },
                    "author_position": "first",
                    "is_corresponding": True,
                    "institutions": [
                        {"id": "https://openalex.org/I1", "display_name": "Institute One"},
                        {"id": "https://openalex.org/I99", "display_name": "Removed Institute"},
                    ],
                }
            ],
            "topics": [{"id": "https://openalex.org/T1", "score": 0.9}],
        },
        {
            "id": "https://openalex.org/W2",
            "publication_year": 2021,
            "type": "book",
            "primary_location": {"source": {"id": "https://openalex.org/S2"}},
            "open_access": {"is_oa": False},
            "is_xpac": True,
            "cited_by_count": 1,
            "primary_topic": {"id": "https://openalex.org/T2"},
            "referenced_works": None,
            "authorships": [
                {
                    "author": {
                        "id": "https://openalex.org/A2",
                        "display_name": "Bob Bibliometrician",
                        "orcid": None,
                    },
                    "author_position": "last",
                    "is_corresponding": False,
                    "institutions": [{"id": "https://openalex.org/I2"}],
                }
            ],
            "topics": [{"id": "https://openalex.org/T2", "score": 0.8}],
        },
    ]
    pq.write_table(pa.Table.from_pylist(works), fixtures / "works" / "fixture.parquet")
    pq.write_table(
        pa.Table.from_pylist(
            [
                {
                    "id": "https://openalex.org/I1",
                    "display_name": "Institute One",
                    "country_code": "CA",
                    "type": "education",
                },
                {
                    "id": "https://openalex.org/I2",
                    "display_name": "Institute Two",
                    "country_code": "US",
                    "type": "education",
                },
            ]
        ),
        fixtures / "institutions" / "fixture.parquet",
    )
    pq.write_table(
        pa.Table.from_pylist(
            [
                {
                    "id": "https://openalex.org/S1",
                    "display_name": "Source One",
                    "issn_l": "1234-5678",
                    "type": "journal",
                },
                {
                    "id": "https://openalex.org/S2",
                    "display_name": "Source Two",
                    "issn_l": None,
                    "type": "repository",
                },
            ]
        ),
        fixtures / "sources" / "fixture.parquet",
    )
    pq.write_table(
        pa.Table.from_pylist(
            [
                {
                    "id": "https://openalex.org/T1",
                    "display_name": "Topic One",
                    "subfield": {"id": "https://openalex.org/subfields/1"},
                    "field": {"id": "https://openalex.org/fields/2"},
                    "domain": {"id": "https://openalex.org/domains/3"},
                },
                {
                    "id": "https://openalex.org/T2",
                    "display_name": "Topic Two",
                    "subfield": {"id": "https://openalex.org/subfields/4"},
                    "field": {"id": "https://openalex.org/fields/5"},
                    "domain": {"id": "https://openalex.org/domains/6"},
                },
            ]
        ),
        fixtures / "topics" / "fixture.parquet",
    )


def _render(path: Path, replacements: dict[str, str]) -> str:
    sql = path.read_text()
    for name, value in replacements.items():
        sql = sql.replace(f"{{{{{name}}}}}", value)
    assert "{{" not in sql
    return sql


@pytest.mark.integration
def test_transformations_materialize_exact_fixture_counts():
    service = ClickHouseService()
    _write_parquet_fixtures(service.project_dir / ".data" / "raw")
    sql_dir = service.project_dir / "sql"
    replacements = {
        "WORKS_GLOB": "fixtures/works/*.parquet",
        "INSTITUTIONS_GLOB": "fixtures/institutions/*.parquet",
        "SOURCES_GLOB": "fixtures/sources/*.parquet",
        "TOPICS_GLOB": "fixtures/topics/*.parquet",
    }
    service.up(memory_gb=32, cpus=16)
    try:
        service.execute_script(f"DROP DATABASE IF EXISTS {DATABASE}")
        service.execute_script(_render(sql_dir / "00_schema.sql", replacements))
        raw_output = service.execute_script(
            _render(sql_dir / "05_raw_evidence.sql", replacements)
        )
        raw_rows = [json.loads(line) for line in raw_output.splitlines()]
        assert raw_rows == [
            {
                "raw_reference_entries": 3,
                "rejected_id_entries": 0,
                "distinct_valid_pairs": 2,
                "duplicate_pair_delta": 1,
            },
            {"null_topic_scores": 0},
        ]
        service.execute_script(_render(sql_dir / "10_load_dimensions.sql", replacements))
        service.execute_script(_render(sql_dir / "20_load_works.sql", replacements))
        counts = service.query_value(
            "SELECT arrayJoin([count(), "
            "(SELECT count() FROM openalex_spike.work_author), "
            "(SELECT count() FROM openalex_spike.work_institution), "
            "(SELECT count() FROM openalex_spike.work_topic), "
            "(SELECT count() FROM openalex_spike.citation_edge)]) "
            "FROM openalex_spike.works"
        ).splitlines()
        assert counts == ["2", "2", "3", "2", "2"]
        assert service.query_value(
            "SELECT toString(is_xpac) FROM openalex_spike.works WHERE work_id = 2"
        ) == "true"
        service.execute_script(_render(sql_dir / "30_reverse_projection.sql", replacements))
    finally:
        service.execute_script(f"DROP DATABASE IF EXISTS {DATABASE}")
        service.down()
