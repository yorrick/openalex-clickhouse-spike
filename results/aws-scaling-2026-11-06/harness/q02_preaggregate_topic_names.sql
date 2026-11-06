WITH stats AS (
    SELECT w.publication_year, wt.topic_id,
           countDistinct(w.work_id) AS works,
           sum(w.cited_by_count) AS citations
    FROM openalex_spike.works AS w
    INNER JOIN openalex_spike.work_topic AS wt ON w.work_id=wt.work_id
    GROUP BY w.publication_year, wt.topic_id
)
SELECT s.publication_year AS publication_year,
       t.topic_id AS `t.topic_id`,
       t.display_name AS display_name,
       s.works AS works,
       s.citations AS citations
FROM stats AS s
INNER JOIN openalex_spike.topics AS t ON s.topic_id=t.topic_id
ORDER BY publication_year, t.topic_id;
