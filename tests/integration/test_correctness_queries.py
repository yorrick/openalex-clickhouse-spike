import json

import pytest

from openalex_spike.clickhouse import ClickHouseService
from openalex_spike.correctness import evaluate_stage1, require_all, write_correctness
from tests.integration.test_transform_sql import _render, _write_parquet_fixtures


@pytest.mark.integration
def test_fixture_rebuilds_have_identical_correctness_hashes():
    service = ClickHouseService()
    _write_parquet_fixtures(service.project_dir / ".data" / "raw")
    sql_dir = service.project_dir / "sql"
    replacements = {
        "WORKS_GLOB": "fixtures/works/*.parquet",
        "AUTHORS_GLOB": "fixtures/authors/*.parquet",
        "INSTITUTIONS_GLOB": "fixtures/institutions/*.parquet",
        "SOURCES_GLOB": "fixtures/sources/*.parquet",
        "TOPICS_GLOB": "fixtures/topics/*.parquet",
    }
    databases = ("openalex_fixture_a", "openalex_fixture_b")
    hashes = []
    service.up(memory_gb=32, cpus=16)
    try:
        for database in databases:
            service.execute_script(f"DROP DATABASE IF EXISTS {database}")
            for filename in (
                "00_schema.sql",
                "10_load_dimensions.sql",
                "20_load_works.sql",
            ):
                sql = _render(sql_dir / filename, replacements).replace(
                    "openalex_spike", database
                )
                service.execute_script(sql)
            raw_output = service.execute_script(
                _render(sql_dir / "05_raw_evidence.sql", replacements)
            )
            raw_rows = [json.loads(line) for line in raw_output.splitlines()]
            raw_evidence = {**raw_rows[0], **raw_rows[1]}
            gates, query_evidence, distributions = evaluate_stage1(
                service.query_json,
                database=database,
                works_glob="fixtures/works/*.parquet",
                expected_manifest_rows=2,
                raw_evidence=raw_evidence,
            )
            output = write_correctness(
                service.project_dir / ".data" / "fixture-results" / database / "correctness.json",
                gates,
                query_evidence,
                distributions,
            )
            require_all(gates)
            missing_institutions = next(
                gate for gate in gates if gate.name == "missing_institutions"
            )
            assert missing_institutions.actual == 1
            assert missing_institutions.passed is False
            assert missing_institutions.blocking is False
            assert distributions["referential_coverage"][
                "institution_reference_coverage_ratio"
            ] == pytest.approx(2 / 3)
            assert distributions["missing_institution_sample"] == [
                {
                    "institution_id": 99,
                    "display_name": "Removed Institute",
                    "raw_bridge_rows": 1,
                }
            ]
            hashes.append(output["normalized_sha256"])
        assert hashes[0] == hashes[1]
    finally:
        for database in databases:
            service.execute_script(f"DROP DATABASE IF EXISTS {database}")
        service.down()
