ALTER TABLE openalex_spike.citation_edge ADD PROJECTION by_cited
(
    SELECT citing_work_id, cited_work_id, citing_year
    ORDER BY (cited_work_id, citing_work_id)
);

ALTER TABLE openalex_spike.citation_edge MATERIALIZE PROJECTION by_cited;
