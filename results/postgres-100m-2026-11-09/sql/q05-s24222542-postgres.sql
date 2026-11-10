SELECT 'outgoing' AS direction, cited_work_id AS neighbour_work_id
FROM public.citation_edge
WHERE citing_work_id = 24222542
UNION ALL
SELECT 'incoming' AS direction, citing_work_id AS neighbour_work_id
FROM public.citation_edge
WHERE cited_work_id = 24222542;
