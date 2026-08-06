# OpenAlex ClickHouse validation spike

This repository tests whether the public OpenAlex Parquet snapshot can support
interactive bibliometric SQL in ClickHouse without first reconstructing a full
transactional relational database. Stage 1 is a correctness and query-smoke
experiment targeting 1 GiB of deterministically selected Works plus the
complete small dimensions. Across 60 real-manifest seeds, the Works selection
ranged from 1.00 to 2.07 GiB; the pinned run is 1.17 GiB. It is sample-scale
evidence, not a full-size capacity prediction.

## Prerequisites

- Apple-silicon Docker Desktop capable of running native `linux/arm64` images.
- Python 3.12 and `uv`.
- At least 32 GiB for the Stage 1 ClickHouse container. The validation host is
  normally configured with 16 CPUs and 48 GiB in Docker Desktop. The 50-GiB
  container experiments temporarily used a 56-GiB Docker VM, which exposed
  about 54.8 GiB to containers; the normal allocation is restored after them.
- At least 3 GiB of download space plus ClickHouse working space for Stage 1.
  The pinned Stage 2 input is exactly 98,301,763,421 bytes and its conservative
  preflight reserves another two input-size equivalents plus 50 GiB before
  starting the transfer or build.

Raw Parquet, pinned manifests, local ClickHouse state, and raw logs live below
`.data/` and are not committed. Alliance de recherche numérique du Canada VM
performance remains unvalidated; that environmental spike follows only after
the local Stage 1 and Stage 2 evidence gates pass.

## Exact Stage 1 commands

```bash
uv sync --extra dev
uv run openalex-spike pin-manifests
uv run openalex-spike select
uv run openalex-spike download --tier stage1 --include-small-dimensions
uv run openalex-spike clickhouse-up --memory-gb 32 --cpus 16
uv run openalex-spike stage1 --include-small-dimensions --run-id stage1
uv run openalex-spike report --run stage1
uv run openalex-spike clickhouse-down
```

`stage1` builds the same real input twice in isolated databases, runs blocking
correctness gates, compares normalized result hashes, and executes the fixed
seven-query bibliometric smoke suite. Any malformed-ID, row-reconciliation,
blocking internal-reference, rebuild-hash, architecture, or query failure stops
the run. External snapshot coverage gaps are measured and disclosed without
dropping their bridge rows.

Stage 1 deliberately guarantees update-period coverage by seeding each of four
cumulative-byte strata with a file no larger than one quarter of the target.
That size conditioning favors smaller files, so Stage 1 timings validate query
execution but are not representative performance or capacity measurements.

## Exact Stage 2 commands

Stage 2 downloads the immutable maximum input once, materializes nested tier
views with hard links, loads complete Authors and dimensions once, then rebuilds
the Work-derived tables for the 3.254, 15.118, and 45.233 GB Works tiers.

```bash
uv run openalex-spike download --tier stage2_large \
  --include-complete-authors \
  --include-small-dimensions
uv run openalex-spike stage2 --memory-gb 32 --run-id stage2-v2
uv run openalex-spike report --run stage2-v2
```

After a completed run, the Stage 2 verdict can be regenerated from its pinned
artifacts without starting Docker:

```bash
uv run openalex-spike stage2 --run-id stage2-v2 --report-only
```

The compatibility flag `--memory-gb` is interpreted as GiB. Under the normal
48-GiB Docker Desktop allocation, a 50-GiB container is deliberately
unreachable and refused before Compose changes anything. The local 32-GiB
result is capped at Conditional even if every gate passes. The observed run is
a Fail because the large tier exceeds the configured latency ceilings, not
because of that cap. The CLI never falls back to a smaller envelope.

## Stage 2 result

The pinned [`stage2-v2` report](results/stage2-v2/report.md) covers 98.302 GB of
raw Parquet, including 31,885,241 Works in the largest tier. All blocking
correctness gates passed, all three query classes reached their minimum sample
count, and ClickHouse recorded no query error or server restart. Small and
medium received Pass verdicts. The large tier received Fail: under three
concurrent workers, routine-query p95 was 16.874 seconds against the 15-second
Pass ceiling, while join-query p95 was 140.781 seconds against the 120-second
Conditional ceiling. One-hop citation p95 was 0.476 seconds.

This validates the raw-Parquet-to-ClickHouse path, normalized bibliometric
tables, SQL joins, and citation traversal at the tested volume. It does not yet
validate the unoptimized large tier for interactive concurrent joins. The next
technical experiment should target physical layout or pre-aggregation for the
slow join queries and compare against this immutable baseline.

## Single-user resource result

Two follow-up runs used the same pinned inputs, 50-GiB ClickHouse limit, and
one closed-loop worker. One worker means one workload query at a time; these
are single-stream interactive-latency measurements, not multi-user concurrency
tests.

| Run | Docker / query envelope | Small | Medium | Large | Aggregate |
|---|---|---|---|---|---|
| [`stage2-single-memory50`](results/stage2-single-memory50/report.md) | 16 CPU, 8 query threads | Pass | Pass | Fail | Fail |
| [`stage2-single-memory50-cpu18`](results/stage2-single-memory50-cpu18/report.md) | 18 CPU, 18 query threads | Pass | Fail | Conditional | Fail |

Both runs saw the same approximately 54.8-GiB Docker-visible memory and the
same 50-GiB container limit. The second run therefore changes a joint compute
envelope—CPU allocation and per-query threads—not memory and not CPU alone.
All correctness gates passed, every class reached its sample minimum, and
there were no workload errors, unexpected server replacements, or spills.

At the 31,885,241-Work large tier, the 18-CPU/18-thread run improved join p95
from 306.858 to 60.518 seconds and routine p95 from 169.067 to 4.876 seconds.
Its large q02 query nevertheless had a stable roughly 60-second floor. The
same run also produced severe intermittent medium-tier q03/q07 tails and
isolated small-tier maxima. Slow and fast executions read the same rows with
overlapping memory use, while measured peak query memory stayed about 6.2 GiB
and spill remained zero. The tested single-stream workload is therefore not
memory-capacity-bound at 50 GiB.

The tier-to-tier instability means one run per envelope cannot prove that the
larger compute envelope caused the large-tier improvement. See the
[`single-user resource result`](docs/superpowers/2026-08-05-single-user-resource-benchmark-results.md)
for the per-class evidence and interpretation boundary.

The medium-tier anomaly was then instrumented and repeated three times with
the fixed 50-GiB / 18-CPU / 18-thread / one-worker envelope. Every repeat
passed the predeclared repeatability rule with wide margin. Observed maxima
across the repeats were routine p95 1.716 seconds, join p95 10.881 seconds, and
q03/q07 maximum-to-median ratio 1.191; there were no 20-second samples,
foreign-database merges, errors, restarts, or spills. The old medium tails are
therefore not an ongoing reproducible issue under this configuration. Their
historical cause remains unknown because the old run predates the new
per-query wait/I/O and merge telemetry.

The tracked follow-up work is in
[`Post-Stage 2 next steps`](docs/superpowers/plans/2026-08-05-post-stage2-next-steps.md):
the performance-repeatability item is complete; snapshot updates and
enrichment design remain.

## SQL access

After a passing run, start ClickHouse again with `clickhouse-up`. The retained
database is `openalex_stage1_b`. The native and HTTP ports are published only
on `127.0.0.1:9000` and `127.0.0.1:8123`. From the repository, an immediate
SQL shell is available with:

```bash
docker compose exec clickhouse clickhouse-client \
  --user openalex \
  --password openalex-local-only \
  --database openalex_stage1_b
```

The analytical schema contains Works, Authors, Institutions, Sources, Topics,
authorship and affiliation bridges, Work-topic links, and deduplicated citation
edges suitable for aggregations, entity joins, and one-/two-hop network queries.

DBeaver's ClickHouse JDBC driver uses the HTTP interface. Configure it with
host `127.0.0.1`, port `8123`, database `openalex_stage1_b`, user `openalex`, and
password `openalex-local-only`. Port `9000` is the native protocol used by
`clickhouse-client`, not the DBeaver connection. Both host ports are
loopback-only. These committed credentials are deliberately limited to this
local validation environment and must not be reused for a shared deployment.
