# OpenAlex ClickHouse Validation Design

Date: 2026-08-04  
Status: reviewed design

## 1. Decision to validate

Test whether a single self-managed ClickHouse server is a credible shared SQL
platform for OpenAlex bibliometrics on a Digital Research Alliance of Canada
persistent VM. The target workload is aggregation, joins across OpenAlex
entities, and bounded one- and two-hop citation traversal for a team of about
ten researchers, with three concurrent users as the benchmark load.

This spike validates the data model, transformation correctness, query
expressibility, and sample-scale behaviour before an Alliance resource request.
It produces a sizing model and a resource request; it does not claim that local
sample timings predict full-scale Alliance latency, volume IOPS, network
performance, or object-store compatibility. Those performance claims require
an Alliance VM with the full intended corpus.

## 2. Evidence and fixed inputs

- OpenAlex publishes the public snapshot in native Snappy Parquet under
  `s3://openalex/data/parquet/`, partitioned by `updated_date` and described by
  manifests.
- The manifest dated 2026-06-26 reports 783,555,949,110 bytes across all
  Parquet entities.
- Works account for 724,970,323,127 bytes and 510,372,821 records in 2,446
  files.
- Authors account for 52,769,910,496 bytes and 119,129,660 records.
- All selected non-Works/non-Authors entities total exactly 298,706,581 bytes:
  Institutions, Sources, Publishers, Funders, Topics, Subfields, Fields,
  Domains, Concepts, Keywords, Continents, Countries, and the small type,
  language, licence, and SDG lookups. Awards account for 5,517,008,906 bytes
  and 18,991,361 records; they are not needed for the target workload and are
  excluded. Works, Authors, Awards, and the selected 298,706,581 bytes
  reconcile exactly to the 783,555,949,110-byte combined manifest.
- The local host has 128 GB RAM, 18 logical CPUs, about 1 TiB of free storage,
  and an ARM64 processor. Docker is installed but its daemon is not currently
  running.

The implementation will pin the OpenAlex manifests, their HTTP ETags, and the
exact file URLs and byte counts recorded in them. It will pin the official
ClickHouse LTS image `clickhouse/clickhouse-server:26.3.12.3`, rather than using
`latest`. The tag was verified to publish native `linux/arm64` and
`linux/amd64` manifests.

## 3. Options considered

### 3.1 Stratified real Parquet sample — selected

Use genuine OpenAlex files selected deterministically from the manifest. This
tests the real nested schema, compression, data skew, and citation arrays with
minimal collection machinery. A partial Works sample produces an incomplete
citation graph, so citation benchmarks must be bounded and interpreted as
engine tests rather than bibliometric findings.

### 3.2 Coherent topical citation corpus — rejected for this spike

Collect one field or institution and recursively fetch cited neighbours. This
would produce a more connected graph, but it introduces API collection logic
and is less representative of the full global dataset.

### 3.3 Real seed plus synthetic scaling — rejected for this spike

Generate a large graph from observed distributions. This is useful for stress
testing but weaker evidence for OpenAlex schema handling and real-world skew.

## 4. Architecture

```text
OpenAlex public S3
    |
    v
pinned manifests + selected Parquet files
    |
    +--> direct schema-on-read checks with ClickHouse file()/s3()
    |
    v
ClickHouse native MergeTree tables
    |
    +--> dimensions and work table
    +--> authorship/institution/topic bridges
    +--> citation edge table
    |
    v
correctness checks + sequential benchmark + 3-client benchmark
    |
    v
machine-readable results and a human-readable verdict
```

ClickHouse runs locally in Docker with its data directory bind-mounted outside
the container. Ports bind only to loopback. The benchmark uses
`clickhouse-client`; DBeaver receives a separate connection smoke test so GUI
behaviour does not affect timing.

Container startup is ready only after a native-protocol `SELECT 1` healthcheck
passes. Compose waits for that health status with a 40-second hard timeout;
container "running" state alone is not sufficient because ClickHouse binds its
native port after the entrypoint starts.

Raw Parquet remains canonical. Transformations occur in version-controlled SQL
inside ClickHouse using `INSERT ... SELECT`, `ARRAY JOIN`, and explicit casts.
No Python row-by-row ETL is part of the design.

## 5. Sampling design

### 5.1 Deterministic selection

The selector records its algorithm version and a fixed seed. It parses
`updated_date` from every Works URL, divides the manifest into four
cumulative-byte strata ordered by update date, hashes each URL with the fixed
seed inside its stratum, and selects equal byte budgets from all four strata.
This makes the selection reproducible while preventing one update period from
dominating the sample.

Algorithm `cumulative-bytes-four-strata-v2` constructs Stage 1 coverage before
the greedy fill: in each stratum it selects the lowest stable-ranked file whose
size is no greater than one quarter of the Stage 1 target, then resumes the
normal furthest-below-quarter selection. The selection document records that
cap, the eligible and total file counts per stratum, and the four seed files.
This constraint is necessary because the manifest can contain a single file
large enough to consume the remaining 1 GiB target before every stratum is
visited. It is unconditional algorithm behavior, not a runtime fallback.

"Within one selected file of the target" defines only the allowed byte-budget
overshoot. Given the pinned manifest, algorithm version, and seed, every tier's
file list is exact and deterministic.

Every selected file must match the manifest byte length and have a readable
Parquet footer. Loaded entity row counts must match the sum of the selected
manifest record counts. The manifest does not publish cryptographic checksums,
so the spike must not claim checksum verification.

### 5.2 Stage 1: correctness sample

- Target approximately 1 GiB of Works data with all four strata represented.
  The allowed one-file overshoot means the actual sample may be materially
  larger. Across 60 seeds on the pinned manifest, Stage 1 ranges from
  1,074,513,600 to 2,227,436,005 bytes (1.00 to 2.07 GiB); the configured seed
  selects 1,259,100,971 bytes (1.17 GiB). The per-file Stage 1 coverage cap is
  268,435,456 bytes; eligible/total file counts are 666/966, 479/712, 113/464,
  and 32/304 across strata 0 through 3.
- The coverage cap conditions the four seed choices on file size and therefore
  favors smaller files, especially in recent strata. Stage 1 is a smoke and
  correctness sample; its latency results are not a representative Works
  performance sample. Stage 2 does not apply this cap.
- Include the complete, explicitly enumerated 298,706,581-byte entity set from
  section 2.
- Derive the Stage 1 Authors dimension from distinct authors embedded in the
  selected Works authorships.
- Expected purpose: validate download, schema inference, nested-array
  expansion, numeric ID parsing, table construction, invariants, joins, and
  bounded citation traversal.

### 5.3 Stage 2: performance sample

- Produce nested 3 GB, 15 GB, and 45 GB decimal Works selections, each a strict
  superset of the previous selection and each within one selected file of its
  target. This measures the sample-scale curve and exposes nonlinear/cache
  changes without downloading more than the 45 GB selection.
- Include the complete Authors entity, currently about 52.8 GB.
- Include the exact 298,706,581-byte entity set used in Stage 1.
- For the pinned 2026-06-26 manifests and selected files, maximum input is
  exactly 98,301,763,421 bytes (98.302 GB decimal): 45,233,146,344 bytes of
  Works, 52,769,910,496 bytes of Authors, and 298,706,581 bytes of dimensions.
  Generated ClickHouse data, merge scratch, logs, and results are additional
  and must be measured.
- Stage 2 begins only after Stage 1 correctness gates pass.

At the largest tier, Works represent about 6.2% of current Works bytes while
Authors are complete. Therefore authorship fan-out is understated and many
Authors will have no matching sampled Work. Queries over authorship and
institutions are sample-scale engine measurements, not full-scale capacity
claims. The report must publish authorships per sampled Work and the fraction
of loaded Authors matched by at least one sampled Work at every tier.
If implementation pins a newer manifest, it recomputes all byte targets,
percentages, and reported input totals rather than reusing the 2026-06-26
figures.

## 6. Analytical model

The curated layer uses compact numeric identifiers for joins and retains the
canonical OpenAlex URL identifier for display and traceability.

| Table | Required columns | Purpose |
|---|---|---|
| `works` | `work_id UInt64`, `canonical_id String`, `publication_year Nullable(UInt16)`, `work_type LowCardinality(String)`, `source_id Nullable(UInt64)`, `is_oa Bool`, `is_xpac Bool`, `cited_by_count UInt32`, `primary_topic_id Nullable(UInt64)` | Work facts and common filters |
| `authors` | `author_id UInt64`, `canonical_id String`, `display_name String`, `orcid Nullable(String)` | Author dimension |
| `institutions` | `institution_id UInt64`, `canonical_id String`, `display_name String`, `country_code Nullable(String)`, `institution_type LowCardinality(String)` | Institution dimension |
| `sources` | `source_id UInt64`, `canonical_id String`, `display_name String`, `issn_l Nullable(String)`, `source_type LowCardinality(String)` | Source dimension |
| `topics` | `topic_id UInt64`, `display_name String`, `subfield_id UInt64`, `field_id UInt64`, `domain_id UInt64` | Topic hierarchy |
| `work_author` | `work_id UInt64`, `author_id UInt64`, `author_position LowCardinality(String)`, `is_corresponding Bool` | Authorship joins |
| `work_institution` | `work_id UInt64`, `author_id UInt64`, `institution_id UInt64` | Affiliation and collaboration joins |
| `work_topic` | `work_id UInt64`, `topic_id UInt64`, `score Float32`, `is_primary Bool` | Topical aggregation |
| `citation_edge` | `citing_work_id UInt64`, `cited_work_id UInt64`, `citing_year Nullable(UInt16)` | Citation traversal and aggregation |

`is_xpac` is the OpenAlex snapshot field identifying records from the expanded
XPAC corpus. It remains explicit so benchmark reports can show XPAC and
non-XPAC distributions rather than silently mixing them.

Numeric IDs are produced by stripping the entity prefix from canonical IDs
(for example, `https://openalex.org/W2741809807` becomes `2741809807`) and
parsing the remainder as `UInt64`.

`citation_edge` is deduplicated on `(citing_work_id, cited_work_id)` and ordered
by that pair. The benchmark measures this baseline plus a predefined reverse
projection ordered by `(cited_work_id, citing_work_id)`. Projection build time,
peak disk, final disk, and the before/after timings for incoming-citation
queries are reported. This is a planned experimental variant, not an automatic
runtime fallback.

All tables use explicit schemas. Parquet schema inference is used for
inspection, not as the production table definition.

## 7. Correctness gates

Stage 1 must satisfy all gates before Stage 2:

1. The resolved container platform is native `linux/arm64`; `uname -m` inside
   the container reports `aarch64`, and the recorded image digest is not using
   Rosetta/QEMU emulation. Emulation stops the benchmark because its timings
   would not be usable.
2. Re-running the selector from its recorded algorithm version and seed
   produces a byte-identical selected-file list.
3. Every selected Parquet file is present at the manifest byte length and has a
   readable footer.
4. Raw Works rows equal the selected manifest record total.
5. A null or empty `referenced_works` array emits zero edges, and a null or
   malformed referenced ID is counted as a rejection. Report the raw reference
   entry count, distinct valid `(citing, cited)` pair count, duplicate-pair
   delta, and rejected-ID count. Deduplicated `citation_edge` rows must equal
   the distinct valid-pair count.
6. Bridge-table counts equal independent raw-array expansion counts.
7. Numeric ID parsing is lossless for all non-null OpenAlex entity IDs. Any
   rejected entity ID blocks Stage 2 unless the user explicitly approves a
   documented waiver.
8. Referential coverage is reported for every bridge. Missing cited Works are
   expected in a partial Works sample and are not silently discarded.
   Report citation-edge retention as the fraction whose cited ID is present in
   the sampled `works` table. `work_author` links to sampled Works and derived
   Authors are closed by construction and therefore remain blocking zero-gap
   checks. Topics cross an independent snapshot and its loader additionally
   rejects incomplete hierarchy rows; a Topic gap can therefore indicate a
   fixable transformation loss and remains blocking until its cause is
   classified. Institution links also cross independent Works and Institutions
   snapshots, but that loader has no extra exclusion predicate: preserve and
   report unmatched raw links, distinct IDs, affected Works/Authors, coverage
   ratio, and a capped ID/name sample, but do not invent placeholders or
   silently discard them. Record both manifest dates and digests.
9. At each nested Works tier, report authorships per Work, matched-Author
   fraction, and distributions over publication year, work type, primary
   topic, and `is_xpac`. Report whether these distributions converge as sample
   size grows; do not claim population representativeness from
   `updated_date` stratification alone.
10. Every benchmark query returns a result whose row count and basic invariants
   are checked.
11. Recreating the database from the same pinned input produces the same table
   counts and result hashes for order-normalized correctness queries.

Any failed gate stops progression. The failure is diagnosed and the design is
revisited; the implementation must not silently switch formats, engines, or
sampling methods.

## 8. Benchmark workload

The fixed query suite contains:

1. Work and open-access counts by publication year and work type.
2. Publication and citation totals by topic and year.
3. Author output joined through `work_author` to the Authors dimension.
4. Institution output and cross-country collaboration by year.
5. Incoming and outgoing one-hop citations for selected seed works, with
   incoming queries measured before and after the reverse projection.
6. Deduplicated outgoing two-hop traversal for ordinary and high-degree seeds,
   reported as a diagnostic rather than a latency gate.
7. Citation totals grouped by citing year and cited work.

Seeds are selected deterministically after load from median, 95th-percentile,
and maximum observed reference counts. Citation queries are bounded by explicit
seeds and, where needed, years. An unbounded global two-hop expansion is outside
the SQL-service acceptance test and must not be used to declare the design a
failure. Because only about 6.2% of Works bytes are loaded at the largest tier,
the graph is sparse and the two-hop frontier is not representative of the full
network. Edge retention is displayed beside every citation result, and no
full-scale two-hop capacity claim is made locally.

Queries 1–5 and 7 run at the nested 3 GB, 15 GB, and 45 GB Works tiers. The
current local Docker VM exposes 46.964 GiB and therefore cannot run the planned
50 GiB container. The local scaling curve explicitly uses the 32 GiB envelope
and its verdict is capped at Conditional before execution. The 50 GiB arm is
retained for a different environment configured with at least 54 GiB of Docker
memory; the CLI refuses it here before Compose mutation and never downgrades it.
The report plots measured latency and bytes read at all three tiers and reports
a descriptive log-log slope. The slope may expose nonlinear/cache behaviour,
but it is not used to predict a production latency or declare full-scale
success.

## 9. Resource envelope and measurement

The source Alliance allocation table states a persistent-project ceiling of 25
vCPU and 50 GB RAM. The local host can expose only 16 benchmark CPUs, so the
CPU test is deliberately below that stated ceiling. This local Stage 2 run
measures all three Works tiers at 32 GiB with 16 CPUs. The 50 GiB comparison is
not executed on the current host and remains an environmental-spike task. Note
that the CLI and Compose limit are GiB despite the compatibility spelling
`--memory-gb`.

The benchmark pins these per-query settings:

| Setting | 32 GB run | 50 GB run |
|---|---:|---:|
| `max_threads` | 16 sequential; 8 per concurrent query | 16 sequential; 8 per concurrent query |
| `max_memory_usage` | 7 GiB | 12 GiB |
| `max_bytes_before_external_group_by` | 2 GiB | 4 GiB |
| `max_bytes_before_external_sort` | 2 GiB | 4 GiB |
| `join_algorithm` | `auto` | `auto` |

Sequential runs use all 16 exposed CPUs. Concurrent runs permit up to eight
threads per query, intentionally allowing three clients to contend for the 16
CPUs as they would on a shared server. The 32 GB/50 GB comparison changes both
the container envelope and its documented per-query/spill limits; it is a
bundled operating-envelope comparison, not an isolated causal test of RAM.

All changed and relevant default settings are exported with the results. The
host and container architecture, resolved image digest/platform, emulation
status, ClickHouse version, Docker limits, raw bytes, loaded rows, native table
bytes, and total build time are recorded with every run.

For each query:

- restart ClickHouse before that query's first measured execution and report it
  as `post_restart_run`. Because the host OS cache is not flushed, this is a
  lower bound on a true cold read and is not compared to Alliance cold reads;
- run five measured sequential repetitions and report median and maximum;
- record ClickHouse elapsed time, rows and bytes read, peak memory, and any
  external aggregation/sort/join spill metrics available in `system.query_log`.

The concurrent test launches three closed-loop clients with a deterministic
mixture of routine aggregation, join, and one-hop citation queries. Two-hop is
run separately as a diagnostic. The gated test runs until every query class has
at least 50 completed samples or 60 minutes elapse, whichever happens first.
Report per-query count, errors, median, p95, maximum, peak server memory, CPU
saturation, and whether the server restarted. If a gated class has fewer than
50 completions, report that fact and cap the verdict at Conditional.

The report also estimates full-scale native storage as a low/expected/high
range with one row per table. Each row records sample input rows, sample output
rows, measured native bytes, and its explicit scaling driver:

- `works` scales from measured bytes per selected Work and the full manifest
  Work count;
- each bridge scales from measured bridge rows per selected Work, full Work
  count, and measured native bytes per bridge row;
- `citation_edge` scales from measured distinct edges per selected Work, full
  Work count, and measured native bytes per edge;
- complete dimensions use their measured native sizes without scaling;
- the reverse projection uses its measured projection-to-edge size ratio.

Low and high cases use the minimum and maximum rates observed across the four
sampling strata; the expected case uses the combined sample. These are rough
capacity estimates, not latency extrapolations. Record peak on-disk bytes during
every load and projection build. Compare these cases against the 10 TB
persistent-volume envelope for one active generation and for two generations
used in an atomic cutover. Show both observed peak headroom and a conservative
100% load/merge headroom case. Raw Parquet is modeled separately in object
storage and is never charged to the block-volume calculation.

Local Apple Silicon and local SSD performance must not be linearly extrapolated
to an Alliance x86 VM with network-backed storage.

## 10. Verdict thresholds

The verdict is explicitly local and sample-scale: it applies to the 45 GB Works
tier, about 6.2% of current Works bytes, on the recorded Apple Silicon host. It
does not assert full-corpus or Alliance latency. Use three local-engine outcomes
rather than forcing an uncertain latency preference into a binary result.

### Pass

- All correctness gates pass.
- No out-of-memory failure, server restart, or query error.
- Every gated class has at least 50 completions.
- At the 45 GB Works tier under three-client, 50 GB RAM load: routine-query p95
  is at most 15 seconds, and join/one-hop-query p95 is at most 45 seconds.

### Conditional

- All correctness gates pass and the server remains stable.
- At least one Pass latency is missed, but routine-query p95 is at most 30
  seconds and join/one-hop-query p95 is at most 120 seconds.
- Or at least one gated class has fewer than 50 completions before the 60-minute
  limit, so its p95 cannot support a Pass.
- The conclusion is that ClickHouse is viable but the tested 50 GB envelope or
  table layout does not yet meet the preferred sample-scale experience.

### Fail

- A correctness gate fails, the server runs out of memory or restarts, queries
  error under the fixed workload, or the Conditional latency ceilings are
  exceeded.
- A failure does not automatically authorize a different engine, data format,
  or fallback architecture. The evidence is reviewed before another design is
  proposed.

An under-sampled class cannot trigger Fail from latency alone because its p95
is not meaningful; it caps the latency verdict at Conditional. Correctness
failures, query errors, out-of-memory events, or server restarts still trigger
Fail regardless of sample count.

Two-hop latency never changes the local-engine verdict because the partial
Works sample fragments the graph. It is reported with edge retention as a
diagnostic.

### Separate capacity result

The storage model receives `Likely fits`, `Uncertain`, or `Likely exceeds` for
one-generation and two-generation layouts. `Likely fits` requires the high
estimate including conservative peak headroom to remain within 10 TB. `Likely
exceeds` means the low estimate crosses 10 TB. Anything between is `Uncertain`.
This result informs the Alliance resource request but is not presented as a
measured full-scale fact.

## 11. Outputs

The implementation will produce small, version-controlled artifacts only:

- pinned manifest metadata and selected-file lists;
- explicit ClickHouse DDL and transformation SQL;
- correctness queries and expected invariants;
- benchmark queries and concurrency harness;
- machine-readable run metadata and metrics;
- filtered `system.query_log` evidence for measured query IDs, including
  elapsed time, rows/bytes read, peak memory, and spill-related counters;
- a concise report with Pass, Conditional, or Fail and the evidence supporting
  it.

Raw Parquet, ClickHouse data directories, and unfiltered server/query logs are
excluded from Git.

## 12. Alliance follow-up gate

A local Pass or Conditional result de-risks the data model and supports an
Alliance resource request; it does not settle production performance. On an
actual Alliance VM, verify:

1. whether the allocated object store exposes an S3-compatible endpoint that
   ClickHouse can authenticate against;
2. direct reading of one pinned Parquet file through that endpoint;
3. persistent-volume sequential throughput and representative ClickHouse load
   throughput;
4. the effective persistent RAM/CPU quota and whether storage categories are
   independent;
5. secure DBeaver connectivity through the Alliance network path. The DBeaver
   client and SSH-tunnel configuration are rehearsed locally first.

The Alliance spike, using the full intended corpus or the largest allocation
practical, is the gate for absolute query latency, sustained load throughput,
network-backed I/O behaviour, realistic working-set fit, x86 performance, and
multi-user capacity. Local scaling slopes and storage ranges inform this test
but do not replace it.

No ClickHouse data port is exposed publicly. If Alliance Swift is not compatible
with ClickHouse `s3()`, implementation stops and presents the evidence and the
filesystem alternative for explicit approval; it does not install that
alternative automatically.

## 13. Review disposition

Claude CLI reviewed the complete design as a leaf reviewer. The review's
sample-scale, graph-sparsity, per-table storage, fan-out telemetry, native ARM,
benchmark sample-count, reverse-projection, selector-determinism, ID parsing,
settings, and evidence-retention findings were accepted and incorporated.

The claimed 5.8 GB arithmetic error was rejected after checking the live
manifest: 5,517,008,906 of those bytes are the explicitly excluded Awards
entity, and the selected small entities do total 298,706,581 bytes. The claim
that `is_xpac` was undefined as an OpenAlex field was also rejected; the design
now defines its purpose explicitly. Speculative full citation-edge row counts
from the review were not adopted; the experiment measures edges per Work and
derives a low/expected/high range instead.

## 14. References

- OpenAlex download overview (accessed 2026-08-04):
  <https://developers.openalex.org/download/overview>
- OpenAlex snapshot format (accessed 2026-08-04):
  <https://developers.openalex.org/download/snapshot-format>
- Current Parquet manifest (accessed 2026-08-04; ETag
  `83569df5a65f5741ed09823d94a06c7c`):
  <https://openalex.s3.amazonaws.com/data/parquet/manifest.json>
- Current Works manifest (accessed 2026-08-04; ETag
  `9edf1873de62a74e25ff3d41e0124bbd`):
  <https://openalex.s3.amazonaws.com/data/parquet/works/manifest.json>
- ClickHouse S3 integration (accessed 2026-08-04):
  <https://clickhouse.com/integrations/amazon_s3>
- OpenAlex XPAC description (accessed 2026-08-04):
  <https://developers.openalex.org/guides/key-concepts>
- DBeaver ClickHouse connection documentation (accessed 2026-08-04):
  <https://dbeaver.com/docs/dbeaver/Clickhouse/>
