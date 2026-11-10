# OpenAlex: PostgreSQL at 100 million Works

PostgreSQL did not establish the sub-60-second warm median target at 100m Works for q02, q03, q04. Volume growth stopped at this cohort. ClickHouse met the one-minute median target for all seven families at this cohort. This favors ClickHouse for the tested analytical workload and resource budget. The comparison describes this laptop configuration and selected schema. It does not establish a universal PostgreSQL limit or prove that the full corpus needs a cluster.

## Query measurements

All values are seconds. PostgreSQL and ClickHouse report the median of three warm native executions after one first observation. Athena reports the median of three service total times, including queue, planning and result output, with result reuse disabled. For q05/q06, each family reports the largest of the three fixed seed medians. Incomplete cases have no fabricated median.

| Query family | PG 31.89m, selected profile | PG 100.09m, selected profile | Local CH 100.09m | Athena 100.09m, raw Parquet |
|---|---:|---:|---:|---:|
| q01: Year/type/open-access counts | 5.576943 | 16.836854 | 0.186000 | 83.150000 |
| q02: Topic/year metrics | 41.452837 | 84.083428 | 13.601000 | 77.877000 |
| q03: Top 1000 authors | 25.191693 | 81.338434 | 18.140000 | 103.381000 |
| q04: International country collaboration | 34.192637 | 74.583536 | 34.348000 | 78.959000 |
| q05: One-hop citations, 3 seeds | 0.000160 | Not run (storage limit) | 0.029000 | 74.504000 |
| q06: Two-hop citations, 3 seeds | 0.001509 | Not run (storage limit) | 0.193000 | 79.273000 |
| q07: Top 1000 citation/year counts | 54.507393 | Not run (storage limit) | 18.867000 | 81.556000 |

PostgreSQL starts with the selected 32m profiles: `work_mem=128MB` for q01/q05/q06, `512MB` for q02/q03/q04/q07, and author preaggregation with `enable_nestloop=off` for q03. The final decision JSON records any bounded 100m trial and every selected case label. ClickHouse uses 16 threads. q01 was measured with a 12 GiB query limit and automatic join selection. q02-q07 use a 24 GiB query limit, explicit hash joins and 4 GiB external aggregation/sort thresholds, within the unchanged 32 GiB container. q02 aggregates numeric topic/year statistics before joining names. Its initial 12 GiB profile used an external join and took 228.282 s for the first observation; that interrupted profile has no three-warm median or full-result QA. The original q03 reached its 24 GiB query limit and has no completed timing; the selected variant filters valid Author IDs, aggregates numeric statistics and ranks 1000 IDs before fetching names. All completed selected variants pass full-result QA. These are selected observed profiles, not controlled estimates of the speedup caused by one setting.

[Exact SQL](../results/postgres-100m-2026-11-09/sql) and [full evidence](../results/postgres-100m-2026-11-09/) include every native observation, PostgreSQL plan, requested/effective setting, full-result fingerprint and resource trace. PostgreSQL native time excludes planning and output fetching; ClickHouse uses `FORMAT Null`. Athena service total time is an operational latency measure, not the same timing boundary.

## Data and storage

The nested historical cohort contains 480 pinned Work files, including all 154 from the previous cohort: **100,087,422 Works**, or 19.61% of the 510,372,821 Works in the June snapshot. That denominator is historical. All 119,129,660 Authors and the same complete historical Institutions, Sources and Topics are retained. Only 42 normalized columns across 9 tables are loaded, not every OpenAlex field or entity type.

| Table | Exact loaded rows |
|---|---:|
| `works` | 100,087,422 |
| `work_author` | 161,436,293 |
| `work_institution` | 118,632,954 |
| `work_topic` | 205,306,863 |
| `citation_edge` | 622,671,173 |
| `authors` | 119,129,660 |
| `institutions` | 127,784 |
| `sources` | 283,287 |
| `topics` | 4,516 |

The tables contain **1,327,679,952 normalized rows** in total.

The raw Work objects total 141.981 GB; all selected raw objects including fixed dimensions total 195.050 GB. The 9 normalized local Parquet payloads total 12.271 GB. PostgreSQL occupies 118.986 GB for the database, including 38.347 GB of its 12 completed indexes; this excludes WAL and the two citation indexes that were not completed. All 9 tables are loaded. At 100m, only q01-q04 were measured in PostgreSQL: citation-index creation hit the host disk guard, and the aggregate families already missed the one-minute target. PG citation cells are unmeasured, not timeouts or zeroes. ClickHouse active parts occupy 17.867 GB on disk, including 12.954 GB of compressed column data. These describe different physical layouts and are labelled separately. GB means 10^9 bytes; GiB means 2^30 bytes.

## CPU, memory and I/O

Both local engines have **16 CPU / 32 GiB container limits**, with no container swap, on an Apple M5 Max laptop with 18 physical cores and 128 GiB host RAM. Athena on-demand CPU and RAM allocation are not exposed by this test. Queries run one at a time; concurrency was not tested. The Docker VM has 16 CPUs and approximately 47 GiB RAM. PostgreSQL uses 8 GiB shared buffers, up to 8 workers per Gather and 16 global parallel workers. Data uses host bind mounts through VirtioFS, with host file caching outside container accounting. The engines run sequentially; unrelated laptop/VM activity is not isolated.

| Family | Engine | Median average busy cores, warm window | Largest sampled container RAM, warm GiB |
|---|---|---:|---:|
| q01 | PostgreSQL | 1.46 | 27.87 |
| q01 | ClickHouse | 6.36 | 11.60 |
| q02 | PostgreSQL | 4.30 | 32.00 |
| q02 | ClickHouse | 6.49 | 19.93 |
| q03 | PostgreSQL | 3.04 | 32.00 |
| q03 | ClickHouse | 4.61 | 23.30 |
| q04 | PostgreSQL | 1.65 | 32.00 |
| q04 | ClickHouse | 2.47 | 30.03 |
| q05 | ClickHouse | 0.40 | 8.40 |
| q06 | ClickHouse | 6.76 | 8.88 |
| q07 | ClickHouse | 12.80 | 23.00 |

CPU is cgroup CPU time divided by the instrumented client window. Memory includes shared buffers and file cache; it is not the allocation of just one query. File/shmem counters overlap. Graph queries are too short for reliable CPU/RAM attribution at this sampling interval. Traces include cgroup I/O/pressure and unisolated host disk counters. PostgreSQL plans include logical shared/temp blocks and I/O timings; ClickHouse logs include read bytes and ProfileEvents.

VirtioFS may leave cgroup block I/O empty. Logical reads and shared host counters do not establish physical SSD bandwidth or minimum provisioned IOPS. Allocating 16 CPUs does not mean 16 cores are busy. These measurements do not prove a minimum native Linux hardware configuration or that adding CPUs alone would remove serial or spill bottlenecks.

## Preparation and result QA

Raw objects were copied directly from immutable public S3 versions into a private temporary bucket in certification account 502425560524, `us-east-1`. No raw laptop data was uploaded. The initial 80 GiB host reserve stopped a citation-index build; aggregate measurements then used a protected 40 GiB reserve. Existing backups and historical databases were preserved. All 480 Work footer counts match the pinned manifest. AWS recorded full-object SHA256 for every copied object: 2771 existing objects also match prior full SHA256, while 326 new historical objects have newly recorded server checksums.

The first laptop remote-column projection was interrupted while incomplete because the observed preparation was network-bound. After a real CTAS value/codec probe, Athena produced 5 normalized Work/relationship payloads in AWS. Those flat files were downloaded and consolidated locally. Fixed dimensions came from the existing verified local cache. Bulk COPY, index creation and vacuum timings are archived separately. Citation COPY committed, but its first validation count hit the five-minute deadline before its exact COPY duration was saved; the recovered full count matched 622,671,173 rows without reloading. That COPY duration is unavailable. Index maintenance used a separate 30-minute deadline, 8 GiB maintenance memory and up to 8 maintenance workers, within the same container limits. Incomplete preparation attempts and their costs remain in the evidence, rather than being presented as completed load performance.

Heap insertion order and preparation differ from the 32m test. Growth ratios are therefore descriptive observations, not an isolated asymptotic scaling law. With the same q01 profile, Work count grows 3.139 times and its median grows 3.019 times, consistent with approximately linear scanning over this interval. With the same selected 32m author profile, q03 grows from 25.192 to 102.889 s, a 4.084-fold increase; the retuned 100m result is 81.338 s. The topic and collaboration plans hit the 300 s deadline before retuning. These observations show plan and sort-memory thresholds, not a single smooth scaling curve. There are too few controlled scale points to certify a linear or nonlinear model.

Native queries use pre-flattened, indexed data; raw Athena repeats normalization per query. This does not test an optimized Athena CTAS layout. Citation edges originate from selected citing Works, and targets may lie outside the cohort.

Timed Athena queries still use views over the exact 480 raw Work files and fixed raw dimensions, rather than the normalized CTAS output. Full result sets are canonicalized with explicit integer, boolean, string and NULL types, preserving duplicate multiplicity. Every completed local case is compared against the full raw Athena result fingerprint. The verification file reports exact QA counts and independently reparses the archived full Athena CSV results. The CTAS transformation was also compared with the independent DuckDB normalizer on two real raw files (290,149 Works), with exact symmetric EXCEPT ALL equality across retained Work-derived fields. This is a sample transformation audit, not an independent transformation audit of all 100m Works.

Timed queries use a 300-second deadline. All 33 selected Athena executions completed within that deadline; no longer validation-only run was needed. An earlier q04 attempt was cancelled by the 40 GB scan fuse after 74.8 seconds. Its CTE reads the institution relationships twice; the per-query fuse was raised to 64 GB while the overall 700 GB study budget stayed unchanged. That cancellation is included in costs and is not presented as a performance timeout.

## Cost and cleanup

All Athena statements, including preparation, QA, interrupted work and repeats, total **484.261 GB** of rounded billable scan. At $5 per decimal TB, that is an estimated **$2.4213** in scan charges, not a final invoice.

The following costs describe one timed invocation, using the median scan volume and the largest seed median for graph families. They exclude S3 storage, requests and downloads.

| Family | Scanned GB per invocation | Estimated Athena scan cost |
|---|---:|---:|
| q01 | 1.002 | $0.0050 |
| q02 | 4.190 | $0.0209 |
| q03 | 24.712 | $0.1236 |
| q04 | 42.926 | $0.2146 |
| q05 | 8.139 | $0.0407 |
| q06 | 8.139 | $0.0407 |
| q07 | 7.361 | $0.0368 |

S3 charges are additional. About 10.093 GB of private S3 payload downloads are estimated, including normalized data and repeated result downloads. Assuming $0.09 per GiB, that adds $0 to $0.846 depending on the account-wide free allowance; the final invoice is not available. A conservative full-bucket-for-entire-lease storage estimate is $0.012, and the 3097 known COPY requests add about $0.0155 at $0.005 per 1000. Other S3 request charges were not metered separately. These rates are explicit estimate assumptions, not a complete invoice reconciliation. No EC2 instance was provisioned for this extension. Local hardware and electricity are excluded, and the previously retained raw EBS volume remains separate and unchanged. Pricing sources: [Athena](https://aws.amazon.com/athena/pricing/) and [S3](https://aws.amazon.com/s3/pricing/).

The private temporary bucket and its objects, Glue tables/database and Athena workgroup were deleted. API absence probes and terminal query receipts are archived. Normalized local payloads and full CSV results remain in the durable study directory. Repeating raw Athena QA later depends on continued availability of the pinned public versions.

This study does not establish full-corpus latency, a hardware minimum, or production incremental-update throughput. The prior results remain in [the 32m report](postgres-scaling-benchmark.md). External CLI review remains incomplete: the prior DeepSeek v4.1 Flash and GLM 5.3 Flash attempts through opencode hit the key's hard quota. Exact commands, models and failure output are retained in [the review status](../results/postgres-scaling-2026-11-09/scaling-review-status.json). No completed external review is claimed, and Claude Code validation was not requested.
