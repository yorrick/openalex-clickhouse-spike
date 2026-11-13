# Archived extraction spike

These are throwaway experimental scripts, not a production exporter or service. They write relative to their own path: copy scripts and input.json to a study under ~/work/data before reproducing; never run them inside the Git checkout. Original data: ~/work/data/openalex-duckdb-slicing-20261113. Raw Parquet, generated files and raw API records remain there, outside Git.

run_spike.py runs cache-disabled local/S3 cases; default_cache_variant.py adds the corrected default-cache arm; partition_local.py rewrites all cached records by publication year; api_compare.py retrieves a previously known ID list, not a query-defined export. Input, repeats and guards are study-specific. No AWS account or S3 writes are used. SQL files preserve the executed statements verbatim, including local output paths.

The observed package versions are in requirements.lock. The httpfs extension was installed before timed runs; extension installation is not part of the measured COPY. Profiles, process measurements and structured HTTP receipts are in the results directory. Physical disk bandwidth and IOPS were not measured.
