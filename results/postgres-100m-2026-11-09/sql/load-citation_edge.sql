INSERT INTO pg.public.citation_edge SELECT * FROM read_parquet('/Users/yorrickjansen/work/data/openalex-postgres-100m-20261109/projected/citation_edge.parquet');
