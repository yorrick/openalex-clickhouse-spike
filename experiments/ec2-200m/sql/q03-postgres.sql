SELECT
    a.author_id,
    a.display_name,
    count(DISTINCT wa.work_id) AS works,
    sum(w.cited_by_count) AS citations
FROM public.work_author AS wa
INNER JOIN public.authors AS a ON wa.author_id = a.author_id
INNER JOIN public.works AS w ON wa.work_id = w.work_id
GROUP BY a.author_id, a.display_name
ORDER BY works DESC, a.author_id
LIMIT 1000;
