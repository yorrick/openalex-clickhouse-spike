SELECT
    citing_year,
    cited_work_id,
    count(*) AS citations
FROM public.citation_edge
GROUP BY cited_work_id, citing_year
ORDER BY citations DESC, cited_work_id, citing_year NULLS LAST
LIMIT 1000;
