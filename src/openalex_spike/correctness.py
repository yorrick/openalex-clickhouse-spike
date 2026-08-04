from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable
import hashlib
import json
import re


class CorrectnessFailure(RuntimeError):
    def __init__(self, failed: list["GateResult"]) -> None:
        self.failed = failed
        super().__init__(
            json.dumps(
                {"failures": [asdict(result) for result in failed]},
                sort_keys=True,
            )
        )


@dataclass(frozen=True)
class GateResult:
    name: str
    passed: bool
    expected: int | str
    actual: int | str
    evidence: dict[str, object]
    blocking: bool = True


@dataclass(frozen=True)
class QueryEvidence:
    name: str
    sql: str
    sql_sha256: str
    rows: list[dict[str, object]]


QueryJson = Callable[[str], list[dict[str, object]]]


def require_all(results: list[GateResult]) -> None:
    failed = [result for result in results if result.blocking and not result.passed]
    if failed:
        raise CorrectnessFailure(failed)


def canonical_result_hash(rows: object) -> str:
    encoded = json.dumps(
        rows, separators=(",", ":"), sort_keys=True, ensure_ascii=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def _identifier(value: str) -> str:
    if not re.fullmatch(r"[a-z][a-z0-9_]*", value):
        raise ValueError(f"invalid ClickHouse identifier: {value}")
    return value


def _glob(value: str) -> str:
    if "'" in value or ".." in value or value.startswith("/"):
        raise ValueError(f"unsafe ClickHouse file glob: {value}")
    return value


def _run_query(
    query_json: QueryJson, evidence: list[QueryEvidence], name: str, sql: str
) -> list[dict[str, object]]:
    rows = query_json(sql)
    evidence.append(
        QueryEvidence(
            name=name,
            sql=sql,
            sql_sha256=hashlib.sha256(sql.encode()).hexdigest(),
            rows=rows,
        )
    )
    return rows


def evaluate_stage1(
    query_json: QueryJson,
    *,
    database: str,
    works_glob: str,
    expected_manifest_rows: int,
    raw_evidence: dict[str, int],
) -> tuple[list[GateResult], list[QueryEvidence], dict[str, object]]:
    database = _identifier(database)
    works_glob = _glob(works_glob)
    evidence: list[QueryEvidence] = []
    gates: list[GateResult] = []

    raw_works = _run_query(
        query_json,
        evidence,
        "raw_work_rows",
        f"SELECT count() AS rows, uniqExact(id) AS unique_ids "
        f"FROM file('{works_glob}', Parquet)",
    )[0]
    gates.extend(
        [
            GateResult(
                "manifest_rows_match_parquet",
                int(raw_works["rows"]) == expected_manifest_rows,
                expected_manifest_rows,
                int(raw_works["rows"]),
                {"query": "raw_work_rows"},
            ),
            GateResult(
                "raw_work_ids_are_unique",
                int(raw_works["rows"]) == int(raw_works["unique_ids"]),
                int(raw_works["rows"]),
                int(raw_works["unique_ids"]),
                {"query": "raw_work_rows"},
            ),
            GateResult(
                "raw_reference_ids_parse",
                int(raw_evidence["rejected_id_entries"]) == 0,
                0,
                int(raw_evidence["rejected_id_entries"]),
                {"raw_evidence": raw_evidence},
            ),
            GateResult(
                "topic_scores_are_non_null",
                int(raw_evidence["null_topic_scores"]) == 0,
                0,
                int(raw_evidence["null_topic_scores"]),
                {"raw_evidence": raw_evidence},
            ),
        ]
    )

    raw_bridges = _run_query(
        query_json,
        evidence,
        "raw_bridge_counts",
        f"SELECT "
        f"(SELECT count() FROM file('{works_glob}', Parquet) ARRAY JOIN authorships AS a "
        f"WHERE openalex_numeric_id(id) IS NOT NULL AND openalex_numeric_id(a.author.id) IS NOT NULL) AS authors, "
        f"(SELECT uniqExact(tuple(openalex_numeric_id(id), openalex_numeric_id(a.author.id), openalex_numeric_id(i.id))) "
        f"FROM file('{works_glob}', Parquet) ARRAY JOIN authorships AS a ARRAY JOIN a.institutions AS i "
        f"WHERE openalex_numeric_id(id) IS NOT NULL AND openalex_numeric_id(a.author.id) IS NOT NULL "
        f"AND openalex_numeric_id(i.id) IS NOT NULL) AS institutions, "
        f"(SELECT count() FROM file('{works_glob}', Parquet) ARRAY JOIN topics AS t "
        f"WHERE openalex_numeric_id(id) IS NOT NULL AND openalex_numeric_id(t.id) IS NOT NULL "
        f"AND t.score IS NOT NULL) AS topics",
    )[0]
    materialized = _run_query(
        query_json,
        evidence,
        "materialized_counts",
        f"SELECT "
        f"(SELECT count() FROM {database}.works) AS works, "
        f"(SELECT count() FROM {database}.work_author) AS authors, "
        f"(SELECT count() FROM {database}.work_institution) AS institutions, "
        f"(SELECT count() FROM {database}.work_topic) AS topics, "
        f"(SELECT count() FROM {database}.citation_edge) AS citations",
    )[0]
    for name in ("authors", "institutions", "topics"):
        gates.append(
            GateResult(
                f"{name}_bridge_reconciles",
                int(raw_bridges[name]) == int(materialized[name]),
                int(raw_bridges[name]),
                int(materialized[name]),
                {"raw_query": "raw_bridge_counts", "table_query": "materialized_counts"},
            )
        )
    gates.append(
        GateResult(
            "citation_pairs_reconcile",
            int(raw_evidence["distinct_valid_pairs"])
            == int(materialized["citations"]),
            int(raw_evidence["distinct_valid_pairs"]),
            int(materialized["citations"]),
            {"duplicate_pair_delta": raw_evidence["duplicate_pair_delta"]},
        )
    )

    referential = _run_query(
        query_json,
        evidence,
        "referential_coverage",
        f"SELECT "
        f"(SELECT count() FROM {database}.work_author wa LEFT ANTI JOIN {database}.works w ON wa.work_id=w.work_id) AS missing_works_for_authors, "
        f"(SELECT count() FROM {database}.work_author wa LEFT ANTI JOIN {database}.authors a ON wa.author_id=a.author_id) AS missing_authors, "
        f"(SELECT count() FROM {database}.work_institution) AS institution_bridge_rows, "
        f"(SELECT count() FROM {database}.work_institution wi LEFT ANTI JOIN {database}.institutions i ON wi.institution_id=i.institution_id) AS missing_institutions, "
        f"(SELECT uniqExact(wi.institution_id) FROM {database}.work_institution wi LEFT ANTI JOIN {database}.institutions i ON wi.institution_id=i.institution_id) AS distinct_missing_institution_ids, "
        f"(SELECT uniqExact(wi.work_id) FROM {database}.work_institution wi LEFT ANTI JOIN {database}.institutions i ON wi.institution_id=i.institution_id) AS works_with_missing_institutions, "
        f"(SELECT uniqExact(wi.author_id) FROM {database}.work_institution wi LEFT ANTI JOIN {database}.institutions i ON wi.institution_id=i.institution_id) AS authors_with_missing_institutions, "
        f"if(institution_bridge_rows = 0, 1., (institution_bridge_rows - missing_institutions) / institution_bridge_rows) AS institution_reference_coverage_ratio, "
        f"(SELECT count() FROM {database}.work_topic) AS topic_bridge_rows, "
        f"(SELECT count() FROM {database}.work_topic wt LEFT ANTI JOIN {database}.topics t ON wt.topic_id=t.topic_id) AS missing_topics, "
        f"(SELECT uniqExact(wt.topic_id) FROM {database}.work_topic wt LEFT ANTI JOIN {database}.topics t ON wt.topic_id=t.topic_id) AS distinct_missing_topic_ids, "
        f"if(topic_bridge_rows = 0, 1., (topic_bridge_rows - missing_topics) / topic_bridge_rows) AS topic_reference_coverage_ratio, "
        f"(SELECT count() FROM {database}.citation_edge) AS citation_edges, "
        f"(SELECT count() FROM {database}.citation_edge ce INNER JOIN {database}.works w ON ce.cited_work_id=w.work_id) AS retained_cited_edges, "
        f"if(citation_edges = 0, 1., retained_cited_edges / citation_edges) AS citation_retention_ratio",
    )[0]
    missing_institution_sample = _run_query(
        query_json,
        evidence,
        "missing_institution_sample",
        f"WITH missing_ids AS ("
        f"SELECT DISTINCT wi.institution_id FROM {database}.work_institution wi "
        f"LEFT ANTI JOIN {database}.institutions i ON wi.institution_id=i.institution_id"
        f") SELECT openalex_numeric_id(raw_institution.id) AS institution_id, "
        f"any(raw_institution.display_name) AS display_name, "
        f"count() AS raw_bridge_rows "
        f"FROM file('{works_glob}', Parquet) "
        f"ARRAY JOIN authorships AS authorship "
        f"ARRAY JOIN authorship.institutions AS raw_institution "
        f"WHERE openalex_numeric_id(raw_institution.id) IN missing_ids "
        f"GROUP BY institution_id ORDER BY raw_bridge_rows DESC, institution_id LIMIT 25",
    )
    for name in (
        "missing_works_for_authors",
        "missing_authors",
        "missing_topics",
    ):
        gates.append(
            GateResult(
                name,
                int(referential[name]) == 0,
                0,
                int(referential[name]),
                {"query": "referential_coverage"},
            )
        )
    gates.append(
        GateResult(
            "missing_institutions",
            int(referential["missing_institutions"]) == 0,
            0,
            int(referential["missing_institutions"]),
            {
                "query": "referential_coverage",
                "distinct_missing_ids": int(
                    referential["distinct_missing_institution_ids"]
                ),
                "sample_query": "missing_institution_sample",
            },
            blocking=False,
        )
    )

    primary_keys = {
        "works": "work_id",
        "authors": "author_id",
        "institutions": "institution_id",
        "sources": "source_id",
        "topics": "topic_id",
    }
    for table, key in primary_keys.items():
        rows = _run_query(
            query_json,
            evidence,
            f"{table}_id_uniqueness",
            f"SELECT count() AS rows, uniqExact({key}) AS unique_ids "
            f"FROM {database}.{table}",
        )[0]
        gates.append(
            GateResult(
                f"{table}_ids_are_unique",
                int(rows["rows"]) == int(rows["unique_ids"]),
                int(rows["rows"]),
                int(rows["unique_ids"]),
                {"query": f"{table}_id_uniqueness"},
            )
        )

    distributions = {
        "year_type_topic_xpac": _run_query(
            query_json,
            evidence,
            "year_type_topic_xpac_distribution",
            f"SELECT publication_year, work_type, primary_topic_id, is_xpac, count() AS works "
            f"FROM {database}.works GROUP BY ALL ORDER BY ALL",
        ),
        "authorships_per_work": _run_query(
            query_json,
            evidence,
            "authorships_per_work",
            f"SELECT authorships, count() AS works FROM "
            f"(SELECT work_id, count() AS authorships FROM {database}.work_author GROUP BY work_id) "
            f"GROUP BY authorships ORDER BY authorships",
        ),
        "referential_coverage": referential,
        "missing_institution_sample": missing_institution_sample,
        "materialized_counts": materialized,
    }
    return gates, evidence, distributions


def write_correctness(
    destination: Path,
    results: list[GateResult],
    queries: list[QueryEvidence],
    distributions: dict[str, object],
) -> dict[str, object]:
    normalized = {
        "gates": [asdict(result) for result in results],
        "distributions": distributions,
    }
    document = {
        **normalized,
        "queries": [asdict(query) for query in queries],
        "normalized_sha256": canonical_result_hash(normalized),
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    return document
