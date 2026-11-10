SELECT a.author_id AS author_id, a.display_name AS display_name,
            count(DISTINCT wa.work_id) AS works,
            sum(w.cited_by_count) AS citations
            FROM work_author wa JOIN authors a ON wa.author_id=a.author_id
            JOIN works w ON wa.work_id=w.work_id
            GROUP BY a.author_id, a.display_name
            ORDER BY works DESC, a.author_id LIMIT 1000;
