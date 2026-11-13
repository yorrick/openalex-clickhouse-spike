# PostgreSQL and ClickHouse at 200 million Works on EC2

Measured 12 November 2026 on **200,313,862 Works**. ClickHouse established a warm median below 60 seconds for **six of seven query families**, PostgreSQL for **three of seven**. ClickHouse author aggregation remains unvalidated at the 24 GiB query limit: two executions completed around 58 seconds, then another failed for memory, leaving no valid three-warm median.

Both engines ran sequentially on one EC2 host with the same **16 CPU / 32 GiB container budget**. The results favor ClickHouse for this selected analytical workload, while PostgreSQL was faster for the indexed graph lookups. They do not rule out other PostgreSQL configurations, establish full-corpus latency, or validate the separately requested richer final schema. The historical full-experiment external AI CLI review did not complete. A later scoped Claude review verified the six citation timing cases; see the [timing interpretation](citation-timing-interpretation.md) for its findings and limits.

## Performance and the earlier laptop run

Seconds below are medians of three warm executions after one first observation. q05/q06 use the largest of the three fixed-seed medians, independently for each engine. A timeout is an incomplete observation, not a measured 300-second median. The author failure is also incomplete, not a 58-second result.

| Query family and exact SQL | Local PG 100.09m s | Local CH 100.09m s | EC2 PG 200.31m s | EC2 CH 200.31m s | Raw Athena 200.31m s |
|---|---:|---:|---:|---:|---:|
| q01 Year/type/OA counts ([PG](../experiments/ec2-200m/sql/executed-postgres-q01.sql), [CH](../experiments/ec2-200m/sql/executed-clickhouse-q01.sql)) | 16.837 | 0.186 | 5.687 | 0.437 | 162.242 |
| q02 Topic/year metrics ([PG](../experiments/ec2-200m/sql/executed-postgres-q02-shm32-work512.sql), [CH](../experiments/ec2-200m/sql/executed-clickhouse-q02-grace16.sql)) | 84.083 | 13.601 | Timeout (300 s) | 37.630 | 158.519 |
| q03 Top 1000 authors ([PG](../experiments/ec2-200m/sql/executed-postgres-q03-shm32-work512.sql), [CH](../experiments/ec2-200m/sql/executed-clickhouse-q03-grace16.sql)) | 81.338 | 18.140 | Timeout (300 s) | Memory failure; no median | 160.842 |
| q04 International collaboration ([PG](../experiments/ec2-200m/sql/executed-postgres-q04.sql), [CH](../experiments/ec2-200m/sql/executed-clickhouse-q04-countrysets.sql)) | 74.584 | 34.348 | 215.461 | 6.986 | 147.467 |
| q05 One-hop citations ([PG](../experiments/ec2-200m/sql/executed-postgres-q05-s51557542.sql), [CH](../experiments/ec2-200m/sql/executed-clickhouse-q05-s51557542.sql)) | Not run | 0.029 | 0.000106 | 0.140 | 160.851 |
| q06 Two-hop citations ([PG](../experiments/ec2-200m/sql/executed-postgres-q06-s51557542.sql), [CH](../experiments/ec2-200m/sql/executed-clickhouse-q06-s51557542.sql)) | Not run | 0.193 | 0.002708 | 0.413 | 163.949 |
| q07 Citation/year top 1000 ([PG](../experiments/ec2-200m/sql/executed-postgres-q07-ordered-count.sql), [CH](../experiments/ec2-200m/sql/executed-clickhouse-q07.sql)) | Not run | 18.867 | Timeout (300 s) | 29.127 | 174.883 |

The [100m laptop report](postgres-100m-benchmark.md) and [32m report, including 2m/10m history](postgres-scaling-benchmark.md) contain the earlier profiles. The laptop was an Apple M5 Max (18 cores, 128 GiB host RAM), with 16 CPU / 32 GiB containers in a Docker VM and VirtioFS data mounts. EC2 used native Linux ARM and gp3. PostgreSQL 100m had 12 indexes because the host disk guard stopped citation-index creation; 200m has all 14. SQL and selected profiles also changed. This table compares observed setups and cannot isolate a volume growth law.

The 200m run exposed memory thresholds: the unchanged ClickHouse hash-join profiles for q02/q03/q04 failed before tuning. q02 then completed at 37.630 s with partitioned joins, and the q04 country-set rewrite completed at 6.986 s. PostgreSQL q01 became faster on EC2 despite more rows, while q04 became slower. These observations do not support fitting a single linear latency curve across the two machines. No controlled minimum-CPU, minimum-RAM, cold-cache, concurrency or full-corpus SLA was measured.

Native timings exclude result transfer. PostgreSQL reports EXPLAIN execution time, excluding planning; ClickHouse reports query-log duration with FORMAT Null. Sub-millisecond PostgreSQL graph values are not application response times. Athena uses service total time, including queue, planning and output, with result reuse disabled. Its independent raw-Parquet views repeat normalization and are not an optimized flattened/CTAS lake layout, so this is a workflow comparison rather than a pure engine-only comparison.

## Data volume, entities and fields

The pinned historical June 2026 snapshot contains 510,372,821 Works. This cohort is **39.25%** of it, with 127,375,852 core Works and 72,938,010 XPAC Works. Its 955 Work files preserve all 480 files in the earlier 100m selection. The four complete historical dimensions below remain fixed. Referenced Works outside the selected cohort can be target IDs, but their outgoing edges are not added; graph queries operate on the selected edge cohort.

| Loaded table | Exact rows | Selected columns | PG table + indexes GB | CH active parts GB |
|---|---:|---|---:|---:|
| `works` | 200,313,862 | work_id, canonical_id, publication_year, work_type, source_id, is_oa, is_xpac, cited_by_count, primary_topic_id | 34.293 | 3.688 |
| `work_author` | 324,997,581 | work_id, author_id, author_position, is_corresponding | 37.420 | 2.440 |
| `work_institution` | 240,576,651 | work_id, author_id, institution_id | 27.007 | 1.651 |
| `work_topic` | 410,939,659 | work_id, topic_id, score, is_primary | 47.365 | 3.509 |
| `citation_edge` | 1,250,072,961 | citing_work_id, cited_work_id, citing_year | 166.626 | 17.222 |
| `authors` | 119,129,660 | author_id, canonical_id, display_name, orcid | 13.696 | 3.312 |
| `institutions` | 127,784 | institution_id, canonical_id, display_name, country_code, institution_type | 0.018 | 0.004 |
| `sources` | 283,287 | source_id, canonical_id, display_name, issn_l, source_type | 0.043 | 0.011 |
| `topics` | 4,516 | topic_id, display_name, subfield_id, field_id, domain_id | 0.001 | 0.000 |

The nine tables contain **2,546,445,961 rows and 42 selected columns**. PostgreSQL database contents total **326.477 GB**, including **175.711 GB of indexes**; this excludes WAL and temporary files. ClickHouse active parts total **31.837 GB**, including the **9.453 GB reverse citation projection**. Main compressed column data is 22.380 GB, a narrower measure than total stored parts. Final bind-directory sizes, including engine logs/WAL, are 330.797 GB for PostgreSQL and 32.015 GB for ClickHouse. Compressed disk size does not equal query working memory, as the hash-join failures demonstrate.

Raw Works total 288.202 GB. The full provenance catalog has 3,572 objects and 341.270 GB across 20 entity types; the five loaded source entities account for 3,179 objects and 341.240 GB. The other 393 lookup files total 30.131 MB and are not loaded into this benchmark schema. Shared normalized Parquet totals **20.284 GB in 6,999 fragments**. GB means 10^9 bytes; GiB means 2^30 bytes. A footer sample of one pinned source file per entity showed SNAPPY compression; this is a sample, not an assertion about every shard.

Raw data was downloaded directly from public historical S3 VersionIds onto EC2, with size, full SHA256 and footer-count verification. No raw data was uploaded from or downloaded to the laptop. Athena used a separate server-side copy of those exact source versions. Both native engines consumed identical sealed normalized payloads. The wider set of useful final fields/entities remains pending and is not silently included in these measurements.

## Configured and observed resources

| Item | Observed configuration |
|---|---|
| AWS account / region | Certification 502425560524 / us-east-1 |
| Host | Ubuntu 24.04 ARM, m7g.4xlarge, 16 Graviton cores / 64 GiB RAM |
| Each database | Sequential Docker execution, 16 CPU / 32 GiB memory limits, no swap |
| PostgreSQL | 18.6, pinned image; 8 GiB shared buffers; 8 workers per Gather / 16 global parallel workers; durability enabled |
| ClickHouse | 26.3.12.3 pinned image; 16 query threads; 24 GiB query cap |
| EBS | Encrypted 1,024 GiB gp3 scratch, 6,000 IOPS / 500 MiB/s; 32 GiB root; both deleted |
| Timing collection | Native Linux cgroup CPU, memory, events and block I/O at about 0.5 s; host iostat/vmstat at 1 s |

The following completed-family rows use the selected profile and, for graph families, the seed with the largest median. CPU is total cgroup CPU time divided by the combined three warm windows. RAM is the maximum sampled container usage across those windows. Read/write volumes are medians; bandwidth and IOPS use total counters divided by total windows. All per-seed traces are retained.

| Engine / family (seed for graph rows) | Avg busy cores / 16 | Peak container GiB | Peak anon / shmem GiB | Median read / write GiB | Avg read / write MiB/s | Avg read / write IOPS |
|---|---:|---:|---:|---:|---:|---:|
| postgres q01 | 9.75 | 30.52 | 0.25 / 8.20 | 0.000 / 0.001 | 0.4 / 0.2 | 16.3 / 4.3 |
| postgres q04 | 1.69 | 32.00 | 14.02 / 8.21 | 30.686 / 0.000 | 143.6 / 0.0 | 1216.2 / 0.1 |
| postgres q05-s2003585639 | 0.03 | 24.94 | 0.01 / 8.20 | 0.000 / 0.000 | 0.0 / 0.0 | 0.0 / 0.0 |
| postgres q06-s2003585639 | 0.21 | 24.95 | 0.01 / 8.20 | 0.000 / 0.000 | 0.0 / 0.0 | 0.0 / 0.0 |
| clickhouse q01 | 12.55 | 2.22 | 1.55 / 0.00 | 0.000 / 0.000 | 0.0 / 0.0 | 0.0 / 0.0 |
| clickhouse q02 | 5.90 | 14.98 | 6.11 / 0.00 | 0.002 / 3.087 | 0.1 / 83.3 | 0.9 / 362.0 |
| clickhouse q04 | 14.08 | 19.97 | 13.61 / 0.00 | 0.000 / 0.008 | 0.0 / 0.8 | 0.3 / 100.3 |
| clickhouse q05-s2003585639 | 1.21 | 11.16 | 1.95 / 0.00 | 0.000 / 0.000 | 0.0 / 0.0 | 0.0 / 0.0 |
| clickhouse q06-s24222542 | 10.50 | 11.12 | 1.93 / 0.00 | 0.000 / 0.000 | 0.0 / 0.0 | 0.0 / 0.0 |
| clickhouse q07 | 15.20 | 28.69 | 11.91 / 0.00 | 0.000 / 6.088 | 0.0 / 205.3 | 0.1 / 863.1 |

Memory includes already resident server state and file cache; these values are not incremental RAM required by a query. Anonymous memory omits shared buffers, and shmem overlaps file accounting. Peaks can occur at different times and must not be added. Short graph resource windows have coarse attribution. The OS page cache was dropped before each main engine query phase, while internal database caches were not reset; the first observation is therefore not guaranteed cold. The reported repetitions are warm. Near-zero warm physical reads do not establish a minimum EBS bandwidth for loading or cold execution.

Incomplete selected attempts have their own telemetry, without a fabricated warm median:

| Incomplete selected profile | Observation | Resource window s | Avg busy cores | Peak container GiB | Read / write GiB |
|---|---|---:|---:|---:|---:|
| postgres q02-shm32-work512 | first attempt, timeout | 302.995 | 2.58 | 32.00 | 66.905 / 37.366 |
| postgres q03-shm32-work512 | first attempt, timeout | 302.949 | 1.81 | 32.00 | 56.223 / 27.512 |
| postgres q07-ordered-count | first attempt, timeout | 300.013 | 1.00 | 30.15 | 19.192 / 0.000 |
| clickhouse q03-grace16 | second warm attempt, memory failure | 57.003 | 7.16 | 32.00 | 1.091 / 6.480 |

PostgreSQL collaboration averaged 1.69 busy cores out of 16; its ordered citation trial averaged about one. ClickHouse collaboration averaged 14.08 and citation aggregation 15.20. This identifies substantial utilization differences in these selected plans, not proof that more vCPUs alone would fix PostgreSQL. Athena does not expose an equivalent per-query CPU/RAM allocation through this experiment; scan and service metrics are retained instead.

## Tuning, loading and QA

PostgreSQL had the full 14-index design, including both citation directions. Topic and author SQL preaggregate numeric IDs and fetch names late; collaboration uses distinct country sets. The original 2 GiB work_mem q02/q03 attempts exhausted Docker's separate 8 GiB shared-memory filesystem. A repair recreated only the stopped container against the same PGDATA, raised the tmpfs ceiling to 32 GiB within the unchanged 32 GiB total memory limit, and used 512 MB work_mem per operation. Both then reached the 300-second deadline without a shared-memory failure. q07 also timed out with grouping reordered to use the existing cited-work-leading index, incremental sort and enable_hashagg=off. The baseline failures and all repaired profiles are preserved.

ClickHouse began with 16 threads, explicit hash joins, a 24 GiB query cap, 4 GiB aggregation/sort spill thresholds and the reverse citation projection. Its three initial large-join failures attempted a 16 GiB hash-table growth. q02/q03 received one explicit grace-hash profile with 16 initial buckets and a 3 GiB per-join bound, retaining the SQL and overall allocation. A real miniature join probe passed before the full trials. This partitioning behavior is described in [ClickHouse's join implementation article](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2); actual results here were witnessed on the pinned image.

q04 received one country-set rewrite: form unique country arrays per Work, retain international Works, generate each unordered pair once, then count. PostgreSQL's successful Work primary key proves the Work join does not multiply rows. The array-function probe and the full 325,177-row output comparison passed. q03's grace profile completed a 58.747 s primer and one 58.056 s warm execution, then failed during the next warm execution with query-log code 241 while reading an intermediate stream at the 24 GiB limit. Its stderr also contains a container-hostname DNS warning; the server query log establishes that the measured failure was the memory exception. No second performance candidate was tried for that family. Author aggregation and the richer final schema still need validation before claiming all required queries meet the target.

| Preparation scope | PostgreSQL | ClickHouse |
|---|---:|---:|
| Nine-table COPY / INSERT execution totals | 1,113.456 s | 442.471 s |
| Index creation | 2,974.801 s, 14 indexes | Reverse projection maintained during inserts/merges |
| Maintenance | VACUUM ANALYZE 453.534 s | Nine OPTIMIZE FINAL statements, 319.255 s |

These are scoped operation totals, not complete end-to-end preparation times; count checks, shared normalization, downloads and other validation add time. The shared direct download/hash/footer phase took 859.252 s. The DuckDB bulk PostgreSQL loader avoids a per-row application insertion loop, but both engines still need the shared normalization for this nine-table schema. Production incremental updates and refresh costs were not benchmarked.

All **18 completed selected native cases** match the independent raw-Athena full typed result multisets. Incomplete author and timeout cases do not receive a QA claim. An independent Python/PyArrow raw-value audit passed for 36 files, including 2,322 Works, plus dimension samples. Every normalized fragment footer was checked for selected-column NULL counts and integer ranges. All 3,572 server-copy/EC2 full source hashes and footer counts match. The verifier independently recomputed **72 completed native observations, 94 resource traces including failed/baseline/QA attempts, and all 33 timed Athena CSV fingerprints**. Fixture checks passed all eleven logical cases before the real data run. Duplicate and NULL semantics are preserved.

## Athena scan and experiment cost

| Family | Timed runs | Observed scan GB range per run | Estimated cost of all timed runs USD |
|---|---:|---:|---:|
| q01 | 3 | 2.008 - 2.008 | 0.0301 |
| q02 | 3 | 8.395 - 8.395 | 0.1259 |
| q03 | 3 | 47.599 - 47.599 | 0.7140 |
| q04 | 3 | 87.836 - 87.836 | 1.3175 |
| q05 | 9 | 16.317 - 16.321 | 0.7344 |
| q06 | 9 | 16.317 - 16.321 | 0.7344 |
| q07 | 3 | 14.770 - 14.770 | 0.2216 |

There were 33 timed executions and six additional successful SELECT probes, with 14 DDL statements. Using a 10 MB minimum for the zero-scan SELECTs and rounding each charged query to MB gives **775.650 GB**, or **USD 3.87825 at the explicit USD 5 per decimal TB assumption**. Scan volumes vary between repetitions; the total uses each actual receipt. Complete outputs from all 39 successful SELECTs are archived locally and the timed fingerprints were reparsed.

| Cost scope | Estimated USD |
|---|---:|
| EC2, 3.7667 h at $0.6528/h | 2.4589 |
| gp3 storage + provisioned extra IOPS/throughput | 0.5989 |
| Public IPv4 | 0.0188 |
| Athena, including probes | 3.8783 |
| Subtotal | 6.9549 |
| Unreconciled S3 requests/storage/other allowance | 1.0000 |
| Estimate including allowance | **7.95** |

This is an estimate, not a reconciled AWS invoice. The official Price List API supplied the EC2/gp3 rates; EBS is prorated using November's 720 hours. The estimate uses launch to verified cleanup, within the USD 25 envelope. Taxes, laptop hardware/electricity and the older retained raw EBS are excluded. The latter was explicitly preserved and continues its separate storage charge.

## Evidence, cleanup and remaining limits

At **2026-11-12T22:44:35.229165+00:00**, the instance was terminated and both ephemeral EBS volumes were verified absent. The private bucket, Athena workgroup, Glue database, expiry schedule, security group, instance profile and both study IAM roles were deleted and checked absent. The previous retained volume `vol-039919b5eb12aeb46` remains present. No study compute or temporary bucket remains running.

The [result directory](../results/ec2-200m-2026-11-12/) contains the selected-case summaries, scan receipts, exact cleanup checks and frozen-evidence manifest. The [full frozen archive](../results/ec2-200m-2026-11-12/frozen-evidence.tar.gz) has 10,928 hashed files and excludes raw datasets, database files and credentials; its archive SHA256 is `2f0127b9df11c4450ac8ad39d12b49e4b42bc094da10dac626295a3118467f53`. [Experiment source and executed SQL](../experiments/ec2-200m/) preserve the original and selected profiles. The wider final schema, full-corpus latency and production update validation remain pending.

The external review did not complete. DeepSeek v4.1 Flash and GLM 5.3 Flash through the prescribed opencode CLI at max effort both returned the personal key's hard USD100/100 total-quota error, without a reset. Claude Code was excluded for PostgreSQL by the user, and no company credits were used. [Exact commands and failure status](../results/ec2-200m-2026-11-12/review-status.json) are retained. The benchmark evidence is now integrated into main. The [13 November citation timing audit](citation-timing-interpretation.md) subsequently completed a scoped Claude Code review; it does not constitute a full review of every experiment.
