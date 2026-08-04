SELECT publication_year, work_type, is_oa, is_xpac, count() AS works
FROM openalex_spike.works
GROUP BY publication_year, work_type, is_oa, is_xpac
ORDER BY publication_year, work_type, is_oa, is_xpac;
