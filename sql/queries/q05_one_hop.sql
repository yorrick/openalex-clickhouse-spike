SELECT 'outgoing' AS direction, cited_work_id AS neighbour_work_id
FROM openalex_spike.citation_edge
WHERE citing_work_id = {seed_work_id:UInt64}
UNION ALL
SELECT 'incoming' AS direction, citing_work_id AS neighbour_work_id
FROM openalex_spike.citation_edge
WHERE cited_work_id = {seed_work_id:UInt64};
