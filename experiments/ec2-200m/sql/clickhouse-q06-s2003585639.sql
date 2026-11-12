SELECT count(DISTINCT b.cited_work_id) AS second_hop_works
            FROM citation_edge a JOIN citation_edge b
            ON a.cited_work_id=b.citing_work_id WHERE a.citing_work_id=2003585639;
