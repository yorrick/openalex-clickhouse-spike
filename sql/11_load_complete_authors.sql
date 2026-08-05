INSERT INTO openalex_spike.authors
SELECT
    openalex_numeric_id(id),
    id,
    display_name,
    nullIf(orcid, '')
FROM file('{{AUTHORS_GLOB}}', Parquet)
WHERE openalex_numeric_id(id) IS NOT NULL;
