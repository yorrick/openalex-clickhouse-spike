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
- At least 32 GiB for the Stage 1 ClickHouse container. On the validation host,
  Docker Desktop is configured with 16 CPUs and 48 GiB; its 64-GiB VM setting
  did not boot. A later 50-GiB container run needs at least 54 GiB assigned to
  Docker Desktop and must be validated separately.
- At least 3 GiB of download space plus ClickHouse working space for Stage 1.

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
