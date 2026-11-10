SELECT g.author_id, a.display_name, g.works, g.citations
FROM (
    SELECT wa.author_id,
           count(DISTINCT wa.work_id) AS works,
           sum(w.cited_by_count) AS citations
    FROM work_author wa
    JOIN works w ON wa.work_id=w.work_id
    GROUP BY wa.author_id
    ORDER BY works DESC, wa.author_id
) g
JOIN LATERAL (
    SELECT display_name
    FROM authors a
    WHERE a.author_id=g.author_id
    LIMIT 1
) a ON TRUE
ORDER BY g.works DESC, g.author_id
LIMIT 1000;
