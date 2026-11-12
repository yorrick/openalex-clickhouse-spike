WITH top_author_ids AS MATERIALIZED (
    SELECT g.author_id, g.works, g.citations
    FROM (
        SELECT wa.author_id,
               count(DISTINCT wa.work_id) AS works,
               sum(w.cited_by_count) AS citations
        FROM public.work_author wa
        JOIN public.works w ON wa.work_id=w.work_id
        GROUP BY wa.author_id
    ) g
    JOIN (SELECT author_id FROM public.authors ORDER BY author_id OFFSET 0) valid_author
      ON valid_author.author_id=g.author_id
    ORDER BY g.works DESC, g.author_id
    LIMIT 1000
)
SELECT t.author_id, a.display_name, t.works, t.citations
FROM top_author_ids t
JOIN LATERAL (
    SELECT display_name FROM public.authors a
    WHERE a.author_id=t.author_id LIMIT 1
) a ON TRUE
ORDER BY t.works DESC, t.author_id;
