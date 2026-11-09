# PostgreSQL local OpenAlex benchmark

The [31.89m-Work extension and bounded tuning results](postgres-scaling-benchmark.md) continue this study on 9 November, with the same container CPU and memory caps.

Recorded 8 November 2026. This compares stock PostgreSQL query execution against the already recorded ClickHouse and Athena setups, using the same historical input files and the same selected analytical fields. No EC2 instance was launched. This starter pass measured 2.00m and 10.11m Works; 31.89m Works and the full corpus were not run in PostgreSQL.

## Environment and timing method

- Laptop: 18 CPU cores, 128 GiB RAM. Docker Desktop ARM64 VM: 16 CPUs, approximately 47 GiB RAM. Existing background containers were preserved; this is a shared laptop, not a dedicated laboratory host.
- PostgreSQL 18.6, official ARM64 `postgres:18` image, container cap **16 CPUs / 32 GiB**, shared buffers **8 GiB**, work memory **128 MiB**, up to 8 parallel workers per Gather and 16 globally. Actual worker use depends on the plan. Logged tables, fsync, full-page writes and synchronous commit remain enabled. Exact effective settings and image digest are archived.
- Data uses a dedicated **host bind mount** because the Docker VM had only 8.1 GB free. The host had 411 GiB available before loading. No unrelated containers were stopped and the VM configuration was not changed. VirtioFS and host caching influence I/O; these results cannot be transferred directly to native Linux EC2 storage.
- One primer followed by **three warm runs per case**. PostgreSQL timings are native `Execution Time` from `EXPLAIN (ANALYZE, BUFFERS, WAL, SETTINGS, TIMING OFF, FORMAT JSON)`, so per-node timer overhead is disabled. Planning and client wall times are recorded separately. EXPLAIN still adds instrumentation; its execution time is not an exact equivalent of ClickHouse query-log time or Athena service time.
- A separate complete result fetch is canonicalized using the existing typed multiset oracle. Each of the 11 cases per cohort must match its recorded row count and SHA256. Three fixed seeds are used for each graph family; summary rows report the largest seed median. Each engine can have a different worst seed.
- SQL uses the archived ClickHouse query body, preserving its ordering and limits, with standard PostgreSQL syntax (`count(*)`, `count(DISTINCT ...)`) and local table qualifiers. Athena used logically equivalent queries, some without a final full-result ordering. Historical local ClickHouse used five warm repeats; its OCI image differs from the new runs. These are comparisons of measured setups, not isolated engine or hardware effects.

## Query results

| Works | Query | PostgreSQL warm median s | PostgreSQL warm min to max s | Historical local ClickHouse s | EC2 ClickHouse s | Athena s | Output QA |
|---:|---|---:|---:|---:|---:|---:|---|
| 2,002,982 | q01: Publication counts | 0.051200 | 0.050644 to 0.053728 | 0.060 | 0.018 | 4.345 | MATCH |
| 2,002,982 | q02: Topic statistics | 1.208148 | 1.189756 to 1.233339 | 1.363 | 0.657 | 5.617 | MATCH |
| 2,002,982 | q03: Author output | 24.642830 | 14.408786 to 26.293645 | 33.630 | 1.042 | 148.720 | MATCH |
| 2,002,982 | q04: International collaboration | 1.788761 | 1.770015 to 1.831324 | 1.109 | 0.755 | 10.922 | MATCH |
| 2,002,982 | q05: One-hop citations | 0.000080 | 0.000078 to 0.000082 | 0.011 | 0.003 | 5.060 | MATCH |
| 2,002,982 | q06: Two-hop citations | 0.000778 | 0.000772 to 0.000792 | 0.200 | 0.021 | 5.430 | MATCH |
| 2,002,982 | q07: Citations by year | 11.463833 | 11.355848 to 11.527993 | 2.502 | 0.182 | 5.521 | MATCH |
| 10,109,733 | q01: Publication counts | 0.245462 | 0.240292 to 0.245974 | 0.027 | 0.035 | 14.352 | MATCH |
| 10,109,733 | q02: Topic statistics | 8.454475 | 8.358484 to 8.507210 | 10.780 | 15.990 | 13.757 | MATCH |
| 10,109,733 | q03: Author output | 59.708365 | 57.878652 to 68.669498 | 2.978 | 5.619 | 135.099 | MATCH |
| 10,109,733 | q04: International collaboration | 34.375334 | 33.967077 to 34.712445 | 2.512 | 5.706 | 14.325 | MATCH |
| 10,109,733 | q05: One-hop citations | 0.000123 | 0.000103 to 0.000123 | 0.007 | 0.004 | 13.964 | MATCH |
| 10,109,733 | q06: Two-hop citations | 0.001031 | 0.001009 to 0.001031 | 0.103 | 0.055 | 13.357 | MATCH |
| 10,109,733 | q07: Citations by year | 18.128842 | 18.127674 to 18.674409 | 1.250 | 1.620 | 12.803 | MATCH |

**Warm is a measured condition, not a guarantee.** At 2.00m Works, original q03 took 80.31 s on the primer and 24.64 / 14.41 / 26.29 s on the three warm runs. No deliberate cold-cache reset was performed. The warm median meets 60 s, but its primer does not, and the spread is material.

## CPU, memory and I/O

| Works | Query / selected seed | Average busy cores, median | Container memory peak GiB | Anon peak GiB | File peak GiB | PG shared-buffer reads GB, median | PG temp writes GB, median | Max workers in any Gather |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2,002,982 | q01 | coarse | 8.70 | 0.01 | 8.59 | 0.000 | 0.000 | 4 |
| 2,002,982 | q02 | 2.91 | 9.42 | 0.57 | 8.76 | 0.000 | 0.000 | 3 |
| 2,002,982 | q03 | 0.71 | 18.74 | 0.72 | 17.95 | 4.123 | 0.000 | 0 |
| 2,002,982 | q04 | 0.98 | 13.33 | 0.28 | 12.92 | 0.000 | 0.000 | 0 |
| 2,002,982 | q05-s2003585639 | coarse | 13.12 | 0.06 | 12.92 | 0.000 | 0.000 | 0 |
| 2,002,982 | q06-s2003585639 | coarse | 13.12 | 0.06 | 12.93 | 0.000 | 0.000 | 0 |
| 2,002,982 | q07 | 0.80 | 14.51 | 0.30 | 14.07 | 0.000 | 0.670 | 0 |
| 10,109,733 | q01 | 4.55 | 8.65 | 0.03 | 8.48 | 0.000 | 0.000 | 5 |
| 10,109,733 | q02 | 2.99 | 12.03 | 0.96 | 11.01 | 0.000 | 1.780 | 5 |
| 10,109,733 | q03 | 0.99 | 22.04 | 0.87 | 21.01 | 13.164 | 0.000 | 0 |
| 10,109,733 | q04 | 0.46 | 22.19 | 0.29 | 21.75 | 0.000 | 3.362 | 0 |
| 10,109,733 | q05-s2003585639 | coarse | 21.88 | 0.04 | 21.69 | 0.000 | 0.000 | 0 |
| 10,109,733 | q06-s2003585639 | coarse | 21.89 | 0.04 | 21.69 | 0.000 | 0.000 | 0 |
| 10,109,733 | q07 | 1.01 | 24.44 | 0.05 | 24.23 | 0.000 | 0.000 | 0 |

CPU comes from container cgroup CPU deltas over the instrumented client window, including monitoring and background PostgreSQL work. It is not isolated backend CPU. Sub-100-ms queries have insufficient sampling resolution for a reliable isolated CPU estimate. Container memory includes shared buffers and caches; `file` includes shared-memory pages, so file and shmem must not be added together. Maxima of the separate categories need not be simultaneous.

Shared-buffer reads are PostgreSQL cache misses, which may still be satisfied by OS or host caches; they are **not physical disk bytes**. Root EXPLAIN counters are used once, without summing descendant nodes. Temp writes indicate PostgreSQL spill activity. Cgroup block-I/O accounting can miss host bind-mount/VirtioFS operations; host disk counters are recorded separately but include unrelated host activity. No minimum disk bandwidth is inferred.

## Loading and storage

PostgreSQL native COPY accepts text, CSV and its own binary format, not Parquet ([PostgreSQL documentation](https://www.postgresql.org/docs/18/sql-copy.html)). That does not require a custom row-by-row parser: a small witnessed DuckDB SQL projection reads the Parquet files and bulk-writes them through its PostgreSQL extension into ordinary PostgreSQL tables ([DuckDB documentation](https://duckdb.org/docs/stable/extensions/postgres)). **DuckDB only loads the data; PostgreSQL runs every benchmark query.** No intermediate full CSV was materialized.

Both database designs require field selection and array/relationship normalization. ClickHouse performs that directly from Parquet in SQL. Here, DuckDB performs the same projection and PostgreSQL owns the resulting heap tables and ordinary B-tree indexes. No columnar PostgreSQL extension or foreign-data scan is used for the measured queries. An alternative documented by [pg_duckdb](https://github.com/duckdb/pg_duckdb) is to expose Parquet through PostgreSQL while DuckDB executes the analytical work. That alternative was not installed or tested here; it would answer a different engine-comparison question.

| Cohort | Complete Authors retained | Bulk insert seconds | Work-only bulk insert seconds | Index creation seconds, newly built | Database GB after indexing | Index GB |
|---|---:|---:|---:|---:|---:|---:|
| 2,002,982 Works | 119,129,660 | 146.05 | 63.98 | 132.68 | 17.366 | 4.698 |
| 10,109,733 Works | 119,129,660 | 416.13 | 416.13 | 209.91 | 30.638 | 12.073 |

Copy times exclude setup, source-file metadata checks, post-load row-count validation, index creation and final VACUUM/ANALYZE; those phases are separately archived. Load telemetry spans the copy plus its post-load row-count/size validation. Dimensions are loaded and indexed once and retained at larger tiers; Work-derived tables are reset and bulk-loaded with indexes rebuilt. Table byte counts include PostgreSQL row/storage overhead; they are not comparable to raw Parquet bytes as a pure compression ratio. All tiers contain the same selected fields as ClickHouse, not complete OpenAlex records.

## q03 rewrite on unchanged resources

| Works | SQL | Warm seconds | Median s | Exact output |
|---:|---|---|---:|---|
| 2,002,982 | Aggregate author IDs before parameterized name lookup | 5.846 / 5.284 / 5.233 | 5.284 | MATCH |
| 10,109,733 | Aggregate author IDs before parameterized name lookup | 31.120 / 30.477 / 30.815 | 30.815 | MATCH |

| Works | Original control A median s | Rewrite median s | Original control B median s | Symmetric A/B control ratio | 50% reduction target |
|---:|---:|---:|---:|---:|---|
| 10,109,733 | 59.708 | 30.815 | 52.848 | 1.1298 | Not met |

At 10m, the rewrite improved the observed median but did not meet the prospective target of a 50% reduction. Original-SQL controls were within the declared 1.20 ratio bound; cache and order sensitivity still exist. At 2m there was no bracketed control.

The baseline remains separate. For 2m Works, the prospective target was to halve the 24.643-s median, under identical resources. The observed rewrite median is 5.284 s, with the full 1,000-row output hash unchanged. It preserves COUNT DISTINCT and sum multiplicity. A parameterized name lookup occurs after author aggregation, and the inner lookup still filters unmatched authors before the final limit. The Authors primary key guarantees at most one matching name. This is a query-shape experiment, not a hardware upgrade. At 2m, the rewrite was measured later and no original-SQL control bracketed it; cache and order effects were not isolated, so the observed ratio is not a causal estimate attributable solely to SQL.

## Updating the dataset

A production sync needs staging plus identity/version tracking. Upsert changed parent entities by OpenAlex ID, replace the changed Works’ authorship/institution/topic/outgoing-citation rows in the same transaction, and process tombstones and merged IDs explicitly. Copying new snapshot files and appending them would retain obsolete versions and relationships. The current benchmark schema does not retain `updated_date`; an incremental loader would need version/checkpoint metadata.

The local probe stages real rows for 1,000 and 10,000 Works, increments citation counts, replays a parent UPSERT plus relationship replacement three times, verifies value idempotency, witnesses 100 tombstones, and rolls the transaction back. Baseline values and table counts are checked afterwards. These are **synthetic staged apply measurements**, excluding extraction, staging, COMMIT/fsync, real snapshot reconciliation, concurrency and full deletion/merge handling. They do not establish production update throughput. Incoming references owned by unaffected Works remain.

| Changed Works | Child rows staged, total | First apply native s | Replay native s | Value-idempotent |
|---:|---:|---:|---|---|
| 1,000 | 18,575 | 4.600 | 0.093 / 0.100 | Yes |
| 10,000 | 131,355 | 12.667 | 0.907 / 0.708 | Yes |

Initial loading can therefore be expressed as a modest set of SQL projections rather than a bespoke parser. Incremental sync has more bookkeeping than an append-only import, particularly replacing nested relationships, reconciling deletions/merges and keeping checkpoints. PostgreSQL provides transactional UPSERT and atomic relationship replacement, but index maintenance, WAL and vacuum work remain real costs; the rolled-back probe deliberately does not estimate all of them.

## Evidence and limits

- [Historical ClickHouse/Athena report](superpowers/2026-08-05-single-user-resource-benchmark-results.md) and [field coverage](openalex-field-inventory.md).
- Full local evidence under `~/work/data/openalex-postgres-20261108/`; archived summaries, plans, settings, hashes and harness are in [the result directory](../results/postgres-local-2026-11-08/). Passwords, PGDATA and temporary files are excluded.
- The user explicitly requested no Claude Code validation for PostgreSQL. Correctness here is backed by the real PostgreSQL executions, complete typed output comparisons and archived plans. No Claude validation was invoked for this work.
- No full corpus was loaded, no PostgreSQL cluster was tested, and no full-corpus latency or RAM requirement is inferred. A Docker bind-mount benchmark on this laptop does not establish an EC2 configuration.
