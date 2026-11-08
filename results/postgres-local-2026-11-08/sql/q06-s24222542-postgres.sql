SELECT count(DISTINCT second.cited_work_id) AS second_hop_works
FROM public.citation_edge AS first
INNER JOIN public.citation_edge AS second
    ON first.cited_work_id = second.citing_work_id
WHERE first.citing_work_id = 24222542;
