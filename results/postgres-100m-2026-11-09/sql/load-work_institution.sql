INSERT INTO pg.public.work_institution SELECT * FROM read_parquet('/Users/yorrickjansen/work/data/openalex-postgres-100m-20261109/projected/work_institution.parquet');
