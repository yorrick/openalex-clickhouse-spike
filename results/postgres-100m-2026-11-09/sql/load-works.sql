INSERT INTO pg.public.works SELECT * FROM read_parquet('/Users/yorrickjansen/work/data/openalex-postgres-100m-20261109/projected/works.parquet');
