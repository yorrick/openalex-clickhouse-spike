# PostgreSQL and ClickHouse at 200 million Works on EC2

Status: experiment in progress. No 200m database-query latency is claimed yet. The earlier [100m laptop results](postgres-100m-benchmark.md) are a different hardware environment and cannot isolate the effect of doubling volume. The required external CLI review has not completed: both prescribed OpenRouter reviewer attempts hit the personal key's hard quota; Claude Code was excluded for PostgreSQL by the user. This report stays a draft.

## Cohort and resources

The historical June 2026 cohort contains 200,313,862 Works in 955 pinned S3 objects, including all 480 objects from the 100m cohort. It represents 39.25% of that snapshot's 510,372,821 Works. The same complete 119,129,660 Authors, 127,784 Institutions, 283,287 Sources and 4,516 Topics are retained. The benchmark keeps the existing 42 columns across nine tables; the separate request to validate an enriched schema is pending.

| Item | Configuration |
|---|---|
| AWS account / region | Certification 502425560524 / us-east-1 |
| Host | Ubuntu 24.04 ARM, m7g.4xlarge, 16 Graviton cores / 64 GiB RAM |
| Each database | Sequential execution, 16 CPU / 32 GiB Docker limits, no swap |
| PostgreSQL | Same pinned PostgreSQL image as 100m, 8 GiB shared buffers, 8 workers per Gather / 16 global workers |
| PostgreSQL indexing | Planned full 14-index design, including both citation directions; actual validity and sizes must be verified after preparation |
| ClickHouse | Same pinned image as 100m, 16 threads, 24 GiB query cap, explicit hash joins, 4 GiB aggregation/sort spill thresholds, reverse citation projection |
| Scratch EBS | Encrypted 1024 GiB gp3, 6000 IOPS / 500 MiB/s, same disk for both engines |
| Raw Works / all input | 288.202 GB / 341.270 GB in the full provenance catalog (3572 objects); the five loaded entity types use341.240 GB (3179 objects) |
| Source transport | Direct public S3 historical-version download to EC2; separate S3 server-side copy for Athena; no raw laptop upload |
| Termination deadline | 2026-11-13 06:58:25 UTC; guest expiry plus independent EventBridge schedule |
| Retention | New instance/disks are ephemeral; earlier retained raw EBS is preserved |

GB means 10^9 bytes; GiB means 2^30 bytes. Configured resources do not mean they are fully used. The report will include observed CPU, memory and disk counters, alongside these allocations.

## Query measurements

Both engines start from their selected 100m SQL and settings. PostgreSQL has numeric preaggregation and late name lookup for authors/topics, a country-set rewrite for collaboration, and work_mem=2GB with nested loops discouraged for q02/q03/q04. q01 and graph queries use 128MB, q07 starts with 512MB. ClickHouse has numeric topic preaggregation, valid author-ID aggregation/ranking before names, sorted MergeTree tables and the reverse citation projection. This compares selected tuned configurations, not exhaustively optimized engines. Each failing family permits at most one evidence-directed trial without increasing its CPU/RAM allocation, with original failures preserved.

One first observation and three warm native executions are planned for each of eleven cases across seven families, with a 300-second limit. Graph families use the largest of the three fixed-seed medians. PostgreSQL uses EXPLAIN ANALYZE/BUFFERS/WAL/SETTINGS with TIMING OFF; ClickHouse uses FORMAT Null and query_log duration. Result transfer is measured separately. Whole typed result multisets are compared, preserving duplicates and NULLs. Raw Athena uses its own normalization and three service-total observations with result reuse disabled; its timing boundary includes planning, queue and result output.

| Family | PostgreSQL EC2 200m median s | ClickHouse EC2 200m median s | Raw Athena 200m median s |
|---|---|---|---|
| q01 Year/type/open-access counts | Pending | Pending | Pending |
| q02 Topic/year metrics | Pending | Pending | Pending |
| q03 Top 1000 authors | Pending | Pending | Pending |
| q04 International collaboration | Pending | Pending | Pending |
| q05 One-hop citations, 3 seeds | Pending | Pending | Pending |
| q06 Two-hop citations, 3 seeds | Pending | Pending | Pending |
| q07 Top cited Works/year | Pending | Pending | Pending |

CPU, current/anonymous/file memory, memory events, native I/O and host iostat/vmstat traces are collected. Cache is cleared on this dedicated host before each engine's query phase; the three reported repetitions are warm and are not a cold-cache SLA. Short graph queries have coarse resource attribution. Preparation, maintenance, output QA and native timing have distinct scopes.

## Preparation QA and cost envelope

The miniature harness has passed eleven complete typed PostgreSQL/ClickHouse result comparisons. These are fixture checks, not 200m performance figures. The check exposed and corrected an empty DuckDB home directory under cloud-init/SSM, the SSM default shell, ClickHouse bind-directory ownership, and a readiness query selecting the benchmark database before it existed. Original failures and minimal probes are retained.

All raw downloads passed size, full SHA256 and Parquet footer checks in859.252s. The catalog also retains393unused lookup-entity files totaling30.131MB; their presence caused a scope-loop error after Authors projection, corrected by explicitly limiting projection to the five benchmark entities. Completed download proofs and author payloads are reused on resume. The independent private S3 copy is complete and raw Athena timing has started. Each source requires an exact size, full SHA256 (matched to earlier sealed SHA256 where available) and Parquet footer count before use. Both engines receive identical sealed normalized payloads. A separate PyArrow/Python scalar/list audit checks a bounded sample against actual retained Parquet values before loading. Its completion, full database/index counts and raw Athena fingerprints are still pending.

The official AWS Price List API reports $0.6528/hour for this EC2 type. Twelve hours of instance, public IPv4 and provisioned EBS are estimated at $9.7755 using explicit gp3 storage/IOPS/throughput rates. Athena has a 128 GB per-query scan fuse and 1.6 TB series reservation budget ($8 at the assumed $5/decimal TB); an additional $1 is reserved for requests/storage/downloads. The total estimate is $18.7755 within a $25 experiment envelope. These are estimates, not a reconciled invoice; local hardware/electricity and previously retained EBS are excluded.

Final costs, coverage, fingerprints, observed resource tables and cleanup receipts will be added after the run. No full-corpus feasibility or hardware minimum is established by this experiment. [Frozen input and preflight evidence](../results/ec2-200m-2026-11-12/) and [exact experiment harness](../experiments/ec2-200m/) are retained alongside the [plan](../experiments/ec2-200m/plan.md).
