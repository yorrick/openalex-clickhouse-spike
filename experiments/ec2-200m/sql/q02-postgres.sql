SELECT
    w.publication_year,
    t.topic_id,
    t.display_name,
    count(DISTINCT w.work_id) AS works,
    sum(w.cited_by_count) AS citations
FROM public.works AS w
INNER JOIN public.work_topic AS wt ON w.work_id = wt.work_id
INNER JOIN public.topics AS t ON wt.topic_id = t.topic_id
GROUP BY w.publication_year, t.topic_id, t.display_name
ORDER BY w.publication_year, works DESC;
