INSERT INTO pg.public.work_author SELECT * FROM read_parquet('/Users/yorrickjansen/work/data/openalex-postgres-100m-20261109/projected/work_author.parquet');
