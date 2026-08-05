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
