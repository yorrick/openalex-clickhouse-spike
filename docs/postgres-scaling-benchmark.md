# PostgreSQL scaling on the local laptop

The extension to **100,087,422 Works**, with a matched local ClickHouse comparison, is in [the 100m report](postgres-100m-benchmark.md). PostgreSQL volume growth stopped there after the bounded aggregate profiles remained above one minute.

Measured 9 November 2026. The next tier contains **31,885,241 Works** (6.247% of the historical 510,372,821-Work snapshot), with all **119,129,660 Authors**, 127,784 Institutions, 283,287 Sources and 4,516 Topics retained. This is every record in those selected cohorts and the same 42 selected analytical columns as the prior comparison, not all available fields or every OpenAlex entity type.

## Decision

The bounded tuning profiles meet the warm-median criterion at 31.89m Works; a 100m run still requires a source and peak-disk preflight.

This tests one 16-CPU / 32-GiB Docker configuration and selected analytical fields on a shared laptop with VirtioFS. It does not rule out PostgreSQL on a larger native Linux server, establish a scaling law or a full-corpus SLA. Best observed settings across exploratory profiles are reported explicitly; no isolated causal speedup is claimed without controls.

| Family | Best observed profile | Warm median s | Three warm observations s | Busy cores, median | Sampled container peak GiB | Requested settings |
|---|---|---:|---|---:|---:|---|
| q01 | [q01](../results/postgres-scaling-2026-11-09/sql/q01.sql) | 5.577 | 5.614 / 5.480 / 5.577 | 1.87 | 12.67 | `{}` |
| q02 | [q02_wm512](../results/postgres-scaling-2026-11-09/sql/q02_wm512.sql) | 41.453 | 50.781 / 41.453 / 40.499 | 3.30 | 23.62 | `{"work_mem": "512MB"}` |
| q03 | [q03_preaggregate_authors_wm512_no_nestloop](../results/postgres-scaling-2026-11-09/sql/q03_preaggregate_authors_wm512_no_nestloop.sql) | 25.192 | 24.573 / 25.192 / 27.110 | 2.41 | 28.02 | `{"enable_nestloop": "off", "work_mem": "512MB"}` |
| q04 | [q04_wm512](../results/postgres-scaling-2026-11-09/sql/q04_wm512.sql) | 34.193 | 34.729 / 34.193 / 32.996 | 1.01 | 11.27 | `{"work_mem": "512MB"}` |
| q05 | [q05-s2003585639](../results/postgres-scaling-2026-11-09/sql/q05-s2003585639.sql) | 0.000160 | 0.000167 / 0.000160 / 0.000158 | 0.14 | 8.39 | `{}` |
| q06 | [q06-s2003585639](../results/postgres-scaling-2026-11-09/sql/q06-s2003585639.sql) | 0.001509 | 0.001509 / 0.001630 / 0.001444 | 0.18 | 8.39 | `{}` |
| q07 | [q07_wm512](../results/postgres-scaling-2026-11-09/sql/q07_wm512.sql) | 54.507 | 55.340 / 53.782 / 54.507 | 1.01 | 18.45 | `{"work_mem": "512MB"}` |

The best-profile table selects from the declared experiments. Graph rows use the largest seed median; tiny-query CPU averages are coarse. It is not an unchanged-configuration growth series. Empty settings mean the 128-MB baseline; exact SQL is linked for every profile.

## Query performance

Seconds below are warm medians. PostgreSQL has one initial observation plus three warm runs; initial observations are not deliberately cold-cache measurements. Statements have a 300-second timeout; a canceled case is incomplete, not a measured 300-second native execution. The two graph families show the largest of three seed medians independently for each engine. The complete per-seed results, plans, exact SQL and typed output hashes are archived. Separate QA-fetch durations include another execution, fetching and canonicalization, not transfer alone.

| Query | PG baseline 2.00m s | PG baseline 10.11m s | PG baseline 31.89m s | PG best profile 31.89m s | Local CH 31.89m s | EC2 CH 31.89m s | Athena 31.89m s |
|---|---:|---:|---:|---:|---:|---:|---:|
| q01: Publication counts | 0.051 | 0.245 | 5.577 | 5.577 | 1.538 | 0.076 | 36.338 |
| q02: Topic statistics | 1.208 | 8.454 | 75.887 | 41.453 | 65.285 | 65.512 | 43.261 |
| q03: Author output | 24.643 | 59.708 | Timeout / partial | 25.192 | 9.896 | 17.630 | 130.395 |
| q04: International collaboration | 1.789 | 34.375 | Timeout / partial | 34.193 | 11.465 | 24.270 | 36.921 |
| q05: One-hop citations | 0.000080 | 0.000123 | 0.000160 | 0.000160 | 0.011 | 0.004 | 38.131 |
| q06: Two-hop citations | 0.000778 | 0.001031 | 0.001509 | 0.001509 | 0.322 | 0.174 | 39.546 |
| q07: Citations by year | 11.464 | 18.129 | 81.494 | 54.507 | 3.781 | 4.947 | 39.825 |

These compare observed setups: historical local ClickHouse had different image/settings and five warm repeats; EC2 ClickHouse had 18 CPUs / 50 GiB versus local PostgreSQL at 16 CPUs / 32 GiB. Athena service time includes S3 result materialization. This is not an isolated hardware-matched engine comparison.

| Case | First observation s | Three warm observations s | Median s | Exact output QA |
|---|---:|---|---:|---|
| [q01](../results/postgres-scaling-2026-11-09/sql/q01.sql) | 7.205 | 5.614 / 5.480 / 5.577 | 5.577 | MATCH |
| [q02](../results/postgres-scaling-2026-11-09/sql/q02.sql) | 71.663 | 75.887 / 64.246 / 77.586 | 75.887 | MATCH |
| [q02_wm512](../results/postgres-scaling-2026-11-09/sql/q02_wm512.sql) | 37.594 | 50.781 / 41.453 / 40.499 | 41.453 | MATCH |
| [q03](../results/postgres-scaling-2026-11-09/sql/q03.sql) | None completed | None completed | timeout | Not completed |
| [q03_preaggregate_authors](../results/postgres-scaling-2026-11-09/sql/q03_preaggregate_authors.sql) | 248.806 | 184.979 / 176.758 / 201.880 | 184.979 | MATCH |
| [q03_preaggregate_authors_wm512](../results/postgres-scaling-2026-11-09/sql/q03_preaggregate_authors_wm512.sql) | 136.809 | 136.698 / 150.618 / 137.631 | 137.631 | MATCH |
| [q03_preaggregate_authors_wm512_no_nestloop](../results/postgres-scaling-2026-11-09/sql/q03_preaggregate_authors_wm512_no_nestloop.sql) | 28.194 | 24.573 / 25.192 / 27.110 | 25.192 | MATCH |
| [q04](../results/postgres-scaling-2026-11-09/sql/q04.sql) | None completed | None completed | timeout | Not completed |
| [q04_wm512](../results/postgres-scaling-2026-11-09/sql/q04_wm512.sql) | 47.712 | 34.729 / 34.193 / 32.996 | 34.193 | MATCH |
| [q05-s2003585639](../results/postgres-scaling-2026-11-09/sql/q05-s2003585639.sql) | 0.002035 | 0.000167 / 0.000160 / 0.000158 | 0.000160 | MATCH |
| [q05-s24222542](../results/postgres-scaling-2026-11-09/sql/q05-s24222542.sql) | 0.001544 | 0.000114 / 0.000144 / 0.000112 | 0.000114 | MATCH |
| [q05-s51557542](../results/postgres-scaling-2026-11-09/sql/q05-s51557542.sql) | 0.004160 | 0.000117 / 0.000099 / 0.000093 | 0.000099 | MATCH |
| [q06-s2003585639](../results/postgres-scaling-2026-11-09/sql/q06-s2003585639.sql) | 0.163 | 0.001509 / 0.001630 / 0.001444 | 0.001509 | MATCH |
| [q06-s24222542](../results/postgres-scaling-2026-11-09/sql/q06-s24222542.sql) | 0.044 | 0.000651 / 0.000695 / 0.000590 | 0.000651 | MATCH |
| [q06-s51557542](../results/postgres-scaling-2026-11-09/sql/q06-s51557542.sql) | 0.023 | 0.000260 / 0.000304 / 0.000396 | 0.000304 | MATCH |
| [q07](../results/postgres-scaling-2026-11-09/sql/q07.sql) | 107.978 | 101.709 / 81.494 / 63.575 | 81.494 | MATCH |
| [q07_wm512](../results/postgres-scaling-2026-11-09/sql/q07_wm512.sql) | 53.980 | 55.340 / 53.782 / 54.507 | 54.507 | MATCH |

## Bounded query tuning

Additional profiles were declared before their tests: first, work_mem = 512 MB on failing families (using the existing q03 pre-aggregation rewrite); then at most one query-specific arm for each still-failing q03/q04/q07 family. The reserved arms change q03 join planning, generate q04 country pairs from per-Work sets, or encourage a q07 hash aggregate with 8-GB work_mem and no parallel workers to bound its memory. The container stays at 16 CPUs / 32 GiB and shared_buffers stays at 8 GiB. work_mem applies per operation and potentially per worker, not as a whole-query cap. Settings are scoped to each trial connection; separate connections keep the 128-MB baseline. These exploratory trials are not all bracketed controls, so their observed differences are not isolated causal estimates.

| Variant or control | Requested settings | Median s | Median busy CPU cores | Sampled peak container GiB | PG shared reads GB | PG temporary writes GB |
|---|---|---:|---:|---:|---:|---:|
| q02_wm512 | `{"work_mem": "512MB"}` | 41.453 | 3.30 | 23.62 | 4.440 | 5.307 |
| q03_preaggregate_authors | `{}` | 184.979 | 1.00 | 12.96 | 0.000 | 0.593 |
| q03_preaggregate_authors_wm512 | `{"work_mem": "512MB"}` | 137.631 | 0.99 | 14.00 | 0.000 | 0.593 |
| q03_preaggregate_authors_wm512_no_nestloop | `{"enable_nestloop": "off", "work_mem": "512MB"}` | 25.192 | 2.41 | 28.02 | 6.318 | 0.593 |
| q04_wm512 | `{"work_mem": "512MB"}` | 34.193 | 1.01 | 11.27 | 0.000 | 0.000 |
| q07_wm512 | `{"work_mem": "512MB"}` | 54.507 | 1.01 | 18.45 | 0.000 | 0.000 |

## Resources and storage

The existing container remains capped at **16 CPUs / 32 GiB**, with 8 GiB shared buffers, 128 MiB work memory and up to eight parallel workers per Gather. The laptop has 18 cores / 128 GiB; Docker exposes 16 cores / approximately 47 GiB. PGDATA uses the existing host bind mount through VirtioFS. Unrelated containers and Docker settings were left unchanged.

| Family, baseline | Median busy CPU cores | Sampled peak container GiB | PG shared-buffer reads GB, median | PG temporary writes GB, median | Maximum parallel workers launched |
|---|---:|---:|---:|---:|---:|
| q01 | 1.87 | 12.67 | 3.661 | 0.000 | 6 |
| q02 | 2.29 | 26.28 | 6.910 | 8.850 | 6 |
| q05 | 0.14 (coarse) | 8.39 | 0.000 | 0.000 | 0 |
| q06 | 0.18 (coarse) | 8.39 | 0.000 | 0.000 | 0 |
| q07 | 1.02 | 16.33 | 0.498 | 0.000 | 0 |

Canceled initial observations below are not warm medians. Their cgroup summaries remain available even though EXPLAIN did not return an actual plan; no physical-read or temporary-byte count is invented for them.

| Canceled case | Monitored seconds | Average busy cores | CPU seconds | Sampled peak container GiB |
|---|---:|---:|---:|---:|
| q03 | 300.13 | 0.66 | 197.61 | 16.04 |
| q04 | 300.08 | 0.33 | 99.01 | 11.19 |

Database after indexing: **64.910 GB**, including **31.059 GB of indexes**. This excludes WAL and temporary workspace.

Five Works-derived tables took **505.94 s** of bulk insert time in total; dimensions were retained. Index creation took **1257.84 s**, followed by VACUUM/ANALYZE. Load traces include post-copy validation; the reported insert seconds exclude it.

The initial authorship import was interrupted after the correlated UNNEST plan materialized and hashed wide nested lists; 71 GiB of scratch was observed during that load. The explicit revised loader uses SELECT-list UNNEST. Before replacement, both projections were executed on two real source files and compared with symmetric EXCEPT ALL: all four relationship multisets matched exactly. Final full table-count and query-output comparisons validate the complete loaded cohort. Completed load seconds above exclude the interrupted attempt, whose elapsed time and last resource sample are archived. A 10-second standalone count probe during rollback cleanup timed out; the loader subsequently performed its own empty-target check before inserting. No timing from that failed probe is used.

The first citation index took 294.234 s, close to the query deadline. The unfinished second citation index was deliberately canceled and rebuilt with a separate 30-minute maintenance deadline; query statements remained capped at 300 s. The completed index-time sum excludes that interrupted partial build, whose elapsed time is archived. All 14 indexes were checked valid and ready before query execution.

CPU is container usage over each instrumented client window, including background PostgreSQL and monitoring overhead. Memory is container occupancy, not query allocation or minimum RAM; file cache includes shared memory, so those categories must not be added. Host filesystem cache can help outside the container accounting, so the 32-GiB cap is not a total RAM budget for the whole stack. Shared-buffer reads can hit OS/host cache and are not physical disk bytes. Cgroup block I/O can miss VirtioFS traffic, while the separate host I/O counters include unrelated activity. No minimum SSD bandwidth is inferred.

## Evidence and limitations

- [Original 2m/10m PostgreSQL report](postgres-local-benchmark.md), [ClickHouse/Athena report](superpowers/2026-08-05-single-user-resource-benchmark-results.md), and [field coverage](openalex-field-inventory.md).
- [Archived scaling evidence](../results/postgres-scaling-2026-11-09/): exact SQL, plans, repeated timings, cgroup traces, loading/indexing/storage and full typed-result QA. Raw source files, passwords and PGDATA are excluded.
- No additional AWS or Athena runs were made: the exact existing 31.9m cohort and its recorded Athena/ClickHouse outputs were reused. Additional billed cloud cost is $0; local electricity and machine opportunity cost were not measured.
- Growth ratios from three nested, non-random cohorts do not establish a scaling law or full-corpus SLA. Complete Authors are fixed at every tier, so latency cannot be scaled uniformly by Work count.
- The relationship loader differs from the earlier tiers. Its revised projection is logically equivalent, but load-time growth is not an unchanged-loader comparison, and physical heap row order can differ. Query schema, indexes, PostgreSQL settings and resource caps remain unchanged for the baseline.
- No Claude Code validation was invoked, as requested. DeepSeek V4.1 Flash and GLM 5.3 Flash review attempts through the personal OpenRouter key both failed with a total key limit error; neither completed a review. The exact commands and failure evidence are archived in scaling-review-status.json and the review logs.
