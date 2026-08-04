INSERT INTO openalex_spike.works
SELECT
    openalex_numeric_id(id),
    id,
    accurateCastOrNull(publication_year, 'UInt16'),
    type,
    openalex_numeric_id(primary_location.source.id),
    coalesce(open_access.is_oa, false),
    coalesce(is_xpac, false),
    toUInt32(cited_by_count),
    openalex_numeric_id(primary_topic.id)
FROM file('{{WORKS_GLOB}}', Parquet)
WHERE openalex_numeric_id(id) IS NOT NULL;

INSERT INTO openalex_spike.citation_edge
SELECT citing_work_id, cited_work_id, min(citing_year)
FROM
(
    SELECT
        openalex_numeric_id(id) AS citing_work_id,
        openalex_numeric_id(referenced_id) AS cited_work_id,
        accurateCastOrNull(publication_year, 'UInt16') AS citing_year
    FROM file('{{WORKS_GLOB}}', Parquet)
    ARRAY JOIN referenced_works AS referenced_id
)
WHERE citing_work_id IS NOT NULL AND cited_work_id IS NOT NULL
GROUP BY citing_work_id, cited_work_id;

INSERT INTO openalex_spike.work_author
SELECT
    openalex_numeric_id(id),
    openalex_numeric_id(authorship.author.id),
    authorship.author_position,
    coalesce(authorship.is_corresponding, false)
FROM file('{{WORKS_GLOB}}', Parquet)
ARRAY JOIN authorships AS authorship
WHERE openalex_numeric_id(id) IS NOT NULL
  AND openalex_numeric_id(authorship.author.id) IS NOT NULL;

INSERT INTO openalex_spike.work_institution
SELECT DISTINCT
    openalex_numeric_id(id),
    openalex_numeric_id(authorship.author.id),
    openalex_numeric_id(institution.id)
FROM file('{{WORKS_GLOB}}', Parquet)
ARRAY JOIN authorships AS authorship
ARRAY JOIN authorship.institutions AS institution
WHERE openalex_numeric_id(id) IS NOT NULL
  AND openalex_numeric_id(authorship.author.id) IS NOT NULL
  AND openalex_numeric_id(institution.id) IS NOT NULL;

INSERT INTO openalex_spike.work_topic
SELECT
    openalex_numeric_id(id),
    openalex_numeric_id(topic.id),
    toFloat32(topic.score),
    ifNull(
        openalex_numeric_id(topic.id) = openalex_numeric_id(primary_topic.id),
        false
    )
FROM file('{{WORKS_GLOB}}', Parquet)
ARRAY JOIN topics AS topic
WHERE openalex_numeric_id(id) IS NOT NULL
  AND openalex_numeric_id(topic.id) IS NOT NULL
  AND topic.score IS NOT NULL;
