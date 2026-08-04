INSERT INTO openalex_spike.authors
SELECT
    openalex_numeric_id(authorship.author.id) AS author_id,
    max(authorship.author.id),
    max(authorship.author.display_name),
    nullIf(max(authorship.author.orcid), '')
FROM file('{{WORKS_GLOB}}', Parquet)
ARRAY JOIN authorships AS authorship
WHERE author_id IS NOT NULL
GROUP BY author_id;

INSERT INTO openalex_spike.institutions
SELECT openalex_numeric_id(id), id, display_name, nullIf(country_code, ''), type
FROM file('{{INSTITUTIONS_GLOB}}', Parquet)
WHERE openalex_numeric_id(id) IS NOT NULL;

INSERT INTO openalex_spike.sources
SELECT openalex_numeric_id(id), id, display_name, nullIf(issn_l, ''), type
FROM file('{{SOURCES_GLOB}}', Parquet)
WHERE openalex_numeric_id(id) IS NOT NULL;

INSERT INTO openalex_spike.topics
SELECT
    openalex_numeric_id(id),
    display_name,
    openalex_hierarchy_id(subfield.id),
    openalex_hierarchy_id(field.id),
    openalex_hierarchy_id(domain.id)
FROM file('{{TOPICS_GLOB}}', Parquet)
WHERE openalex_numeric_id(id) IS NOT NULL
  AND openalex_hierarchy_id(subfield.id) IS NOT NULL
  AND openalex_hierarchy_id(field.id) IS NOT NULL
  AND openalex_hierarchy_id(domain.id) IS NOT NULL;
