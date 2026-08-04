SELECT countDistinct(second.cited_work_id) AS second_hop_works
FROM openalex_spike.citation_edge AS first
INNER JOIN openalex_spike.citation_edge AS second
    ON first.cited_work_id = second.citing_work_id
WHERE first.citing_work_id = {seed_work_id:UInt64};
