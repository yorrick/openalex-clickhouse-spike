WITH stats AS (
    SELECT w.publication_year, wt.topic_id,
           count(DISTINCT w.work_id) AS works,
           sum(w.cited_by_count) AS citations
    FROM public.works w
    JOIN public.work_topic wt ON w.work_id=wt.work_id
    GROUP BY w.publication_year, wt.topic_id
)
SELECT s.publication_year, t.topic_id, t.display_name, s.works, s.citations
FROM stats s JOIN public.topics t ON s.topic_id=t.topic_id
ORDER BY s.publication_year, s.works DESC;
