"""Throwaway, sample-only Athena reference SQL for the recorded experiment."""

import pyarrow as pa

PROJECTION = {
    "authors": ("id", "display_name"),
    "works": (
        "id", "publication_year", "type", "authorships", "primary_topic",
        "topics", "open_access", "is_xpac", "cited_by_count", "referenced_works",
    ),
    "institutions": ("id", "display_name", "country_code", "type"),
    "sources": ("id", "display_name", "issn_l", "type"),
    "topics": ("id", "display_name", "subfield", "field", "domain"),
}


def hive_type(t):
    if pa.types.is_string(t) or pa.types.is_large_string(t):
        return "string"
    if pa.types.is_boolean(t):
        return "boolean"
    if pa.types.is_int8(t) or pa.types.is_int16(t) or pa.types.is_int32(t):
        return "int"
    if pa.types.is_int64(t):
        return "bigint"
    if pa.types.is_float32(t):
        return "float"
    if pa.types.is_float64(t):
        return "double"
    if pa.types.is_list(t) or pa.types.is_large_list(t):
        return f"array<{hive_type(t.value_type)}>"
    if pa.types.is_struct(t):
        return "struct<" + ",".join(
            f"`{f.name}`:{hive_type(f.type)}" for f in t
        ) + ">"
    if pa.types.is_map(t):
        return f"map<{hive_type(t.key_type)},{hive_type(t.item_type)}>"
    raise ValueError(f"No observed Athena mapping for {t}")


def external_table(entity, schema, manifest_location):
    columns = ",\n".join(
        f"`{name}` {hive_type(schema.field(name).type)}"
        for name in PROJECTION[entity]
    )
    return f"""CREATE EXTERNAL TABLE raw_{entity} ({columns})
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
WITH SERDEPROPERTIES ('parquet.column.index.access'='false')
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.SymlinkTextInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION '{manifest_location}'"""


def numeric_id(expr):
    return f"try_cast(regexp_extract({expr}, '[A-Z]([0-9]+)$', 1) AS bigint)"


def hierarchy_id(expr):
    return f"try_cast(regexp_extract({expr}, '/([0-9]+)$', 1) AS bigint)"


def views():
    work = numeric_id("w.id")
    author = numeric_id("a.author.id")
    institution = numeric_id("i.id")
    topic = numeric_id("t.id")
    cited = numeric_id("ref")
    year = "CASE WHEN w.publication_year BETWEEN 0 AND 65535 THEN w.publication_year END"
    return {
        "works": f"""SELECT {work} AS work_id, {year} AS publication_year,
            w.type AS work_type, coalesce(w.open_access.is_oa, false) AS is_oa,
            coalesce(w.is_xpac, false) AS is_xpac,
            cast(w.cited_by_count AS bigint) AS cited_by_count
            FROM raw_works w WHERE {work} IS NOT NULL""",
        "authors": f"""SELECT {numeric_id('id')} AS author_id, display_name
            FROM raw_authors WHERE {numeric_id('id')} IS NOT NULL""",
        "work_author": f"""SELECT {work} AS work_id, {author} AS author_id
            FROM raw_works w CROSS JOIN UNNEST(w.authorships) AS u(a)
            WHERE {work} IS NOT NULL AND {author} IS NOT NULL""",
        "work_institution": f"""SELECT DISTINCT {work} AS work_id,
            {author} AS author_id, {institution} AS institution_id
            FROM raw_works w CROSS JOIN UNNEST(w.authorships) AS u(a)
            CROSS JOIN UNNEST(a.institutions) AS v(i)
            WHERE {work} IS NOT NULL AND {author} IS NOT NULL
            AND {institution} IS NOT NULL""",
        "institutions": f"""SELECT {numeric_id('id')} AS institution_id,
            nullif(country_code, '') AS country_code
            FROM raw_institutions WHERE {numeric_id('id')} IS NOT NULL""",
        "topics": f"""SELECT {numeric_id('id')} AS topic_id, display_name
            FROM raw_topics WHERE {numeric_id('id')} IS NOT NULL
            AND {hierarchy_id('subfield.id')} IS NOT NULL
            AND {hierarchy_id('field.id')} IS NOT NULL
            AND {hierarchy_id('domain.id')} IS NOT NULL""",
        "work_topic": f"""SELECT {work} AS work_id, {topic} AS topic_id
            FROM raw_works w CROSS JOIN UNNEST(w.topics) AS u(t)
            WHERE {work} IS NOT NULL AND {topic} IS NOT NULL
            AND t.score IS NOT NULL""",
        "citation_edge": f"""SELECT {work} AS citing_work_id,
            {cited} AS cited_work_id, min({year}) AS citing_year
            FROM raw_works w CROSS JOIN UNNEST(w.referenced_works) AS u(ref)
            WHERE {work} IS NOT NULL AND {cited} IS NOT NULL
            GROUP BY {work}, {cited}""",
    }


def queries(seed):
    seed = int(seed)
    return {
        "q01": """SELECT publication_year, work_type, is_oa, is_xpac,
            count(*) AS works FROM works
            GROUP BY publication_year, work_type, is_oa, is_xpac""",
        "q02": """SELECT w.publication_year, t.topic_id, t.display_name,
            count(DISTINCT w.work_id) AS works,
            sum(w.cited_by_count) AS citations
            FROM works w JOIN work_topic wt ON w.work_id=wt.work_id
            JOIN topics t ON wt.topic_id=t.topic_id
            GROUP BY w.publication_year, t.topic_id, t.display_name""",
        "q03": """SELECT a.author_id, a.display_name,
            count(DISTINCT wa.work_id) AS works,
            sum(w.cited_by_count) AS citations
            FROM work_author wa JOIN authors a ON wa.author_id=a.author_id
            JOIN works w ON wa.work_id=w.work_id
            GROUP BY a.author_id, a.display_name
            ORDER BY works DESC, a.author_id LIMIT 1000""",
        "q04": """WITH work_country AS (
            SELECT DISTINCT wi.work_id, i.country_code
            FROM work_institution wi JOIN institutions i
            ON wi.institution_id=i.institution_id
            WHERE i.country_code IS NOT NULL AND i.country_code != '')
            SELECT w.publication_year, a.country_code AS country_a,
            b.country_code AS country_b,
            count(DISTINCT a.work_id) AS collaborative_works
            FROM work_country a JOIN work_country b ON a.work_id=b.work_id
            AND a.country_code < b.country_code
            JOIN works w ON a.work_id=w.work_id
            GROUP BY w.publication_year, a.country_code, b.country_code""",
        "q05": f"""SELECT 'outgoing' AS direction, cited_work_id AS neighbour_work_id
            FROM citation_edge WHERE citing_work_id={seed}
            UNION ALL
            SELECT 'incoming' AS direction, citing_work_id AS neighbour_work_id
            FROM citation_edge WHERE cited_work_id={seed}""",
        "q06": f"""SELECT count(DISTINCT b.cited_work_id) AS second_hop_works
            FROM citation_edge a JOIN citation_edge b
            ON a.cited_work_id=b.citing_work_id WHERE a.citing_work_id={seed}""",
        "q07": """SELECT citing_year, cited_work_id, count(*) AS citations
            FROM citation_edge GROUP BY citing_year, cited_work_id
            ORDER BY citations DESC, cited_work_id, citing_year NULLS LAST LIMIT 1000""",
    }


RESULT_TYPES = {
    "q01": {"publication_year": "int", "work_type": "str", "is_oa": "bool", "is_xpac": "bool", "works": "int"},
    "q02": {"publication_year": "int", "topic_id": "int", "display_name": "str", "works": "int", "citations": "int"},
    "q03": {"author_id": "int", "display_name": "str", "works": "int", "citations": "int"},
    "q04": {"publication_year": "int", "country_a": "str", "country_b": "str", "collaborative_works": "int"},
    "q05": {"direction": "str", "neighbour_work_id": "int"},
    "q06": {"second_hop_works": "int"},
    "q07": {"citing_year": "int", "cited_work_id": "int", "citations": "int"},
}


def clickhouse_result_columns(query, rows):
    aliases = {'q02': {'t.topic_id': 'topic_id'}, 'q03': {'a.author_id': 'author_id'}}.get(query, {})
    result = []
    for row in rows:
        if any(source not in row or target in row for source, target in aliases.items()):
            raise ValueError(f'Unexpected ClickHouse column labels for {query}')
        result.append({aliases.get(key, key): value for key, value in row.items()})
    return result


def canonical_rows(query, rows):
    import json
    schema = RESULT_TYPES[query]
    result = []
    for row in rows:
        if set(row) != set(schema):
            raise ValueError(f"Unexpected columns for {query}: {set(row)}")
        values = []
        for column, kind in schema.items():
            value = row[column]
            if value is not None:
                if kind == "int":
                    value = int(value)
                elif kind == "bool":
                    if value not in (True, False, 0, 1, "true", "false", "0", "1"):
                        raise ValueError(f"Invalid boolean: {value!r}")
                    value = value in (True, 1, "true", "1")
                else:
                    value = str(value)
            values.append(value)
        result.append(json.dumps(values, ensure_ascii=False, separators=(",", ":")))
    return sorted(result)
