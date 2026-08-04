SELECT
    citing_year,
    cited_work_id,
    count() AS citations
FROM openalex_spike.citation_edge
GROUP BY citing_year, cited_work_id
ORDER BY citations DESC, cited_work_id
LIMIT 1000;
