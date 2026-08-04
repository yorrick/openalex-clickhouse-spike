SELECT
    w.publication_year,
    t.topic_id,
    t.display_name,
    countDistinct(w.work_id) AS works,
    sum(w.cited_by_count) AS citations
FROM openalex_spike.works AS w
INNER JOIN openalex_spike.work_topic AS wt ON w.work_id = wt.work_id
INNER JOIN openalex_spike.topics AS t ON wt.topic_id = t.topic_id
GROUP BY w.publication_year, t.topic_id, t.display_name
ORDER BY w.publication_year, works DESC;
