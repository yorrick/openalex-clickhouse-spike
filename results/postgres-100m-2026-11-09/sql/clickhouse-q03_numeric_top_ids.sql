SELECT t.author_id AS author_id, a.display_name AS display_name,
       t.works AS works, t.citations AS citations
FROM authors a
INNER JOIN (
    SELECT wa.author_id AS author_id,
           countDistinct(wa.work_id) AS works,
           sum(w.cited_by_count) AS citations
    FROM work_author wa
    INNER JOIN works w ON wa.work_id=w.work_id
    WHERE wa.author_id IN (SELECT author_id FROM authors)
    GROUP BY wa.author_id
    ORDER BY works DESC, author_id
    LIMIT 1000
) t ON a.author_id=t.author_id
ORDER BY t.works DESC, t.author_id;
