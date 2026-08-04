WITH raw_edges AS
(
    SELECT
        id,
        referenced_id,
        openalex_numeric_id(id) AS citing_id,
        openalex_numeric_id(referenced_id) AS cited_id,
        citing_id IS NOT NULL AND cited_id IS NOT NULL AS valid
    FROM file('{{WORKS_GLOB}}', Parquet)
    ARRAY JOIN referenced_works AS referenced_id
)
SELECT
    count() AS raw_reference_entries,
    countIf(NOT valid) AS rejected_id_entries,
    uniqExactIf(tuple(citing_id, cited_id), valid) AS distinct_valid_pairs,
    countIf(valid) - distinct_valid_pairs AS duplicate_pair_delta
FROM raw_edges
FORMAT JSONEachRow;

SELECT countIf(topic.score IS NULL) AS null_topic_scores
FROM file('{{WORKS_GLOB}}', Parquet)
ARRAY JOIN topics AS topic
FORMAT JSONEachRow;
