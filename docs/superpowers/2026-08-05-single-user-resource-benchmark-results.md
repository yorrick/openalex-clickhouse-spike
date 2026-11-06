# Single-user resource benchmark results

## AWS sample and Athena cross-check (2026-11-06)

**Coverage:** the EC2 sample contains **1,557,222 of 464,765,485 Works
(0.335%, about 1 in 298)** in the 2026-10-14 OpenAlex snapshot. Its **2.759 GB**
of compressed input is **0.345% of the 800.893-GB full Parquet snapshot**. The byte
fraction includes all snapshot entity types, while this test used sampled Works
and complete institution/source/topic dimensions; it is not uniform coverage.

### Summary: resources, data, performance and cost

| Run | Works | Compressed input GB | CPUs / ClickHouse RAM | Disk | Query-median range | Cost |
|---|---:|---:|---|---|---:|---|
| Local small | 2,002,982 | 56.323 | 18 / 50 GiB | Bandwidth not recorded | 0.011–33.630 s | Not metered |
| Local medium | 10,109,733 | 68.187 | 18 / 50 GiB | Bandwidth not recorded | 0.007–10.780 s | Not metered |
| Local large | 31,885,241 | 98.302 | 18 / 50 GiB | Bandwidth not recorded | 0.011–65.285 s | Not metered |
| EC2 small cross-check | 1,557,222 | 2.759 | 4 / 8 GiB (16-GiB host) | 50-GiB gp3, requested defaults | 0.005–1.048 s | Included in US$0.081 all-attempts total |
| Athena small cross-check | 1,557,222 | 2.759 | AWS-managed | Original S3 Parquet | 3.170–6.055 s | US$0.040 all-attempt scan fees, included above |

The seven queries cover publication counts, topic statistics, author output,
international collaboration, one-hop and two-hop citation traversal, and cited
work/year-pair counts. Local rows use five warm sequential observations per query;
EC2/Athena rows use three repeated executions, not a controlled warm/cold-cache
test. The local input totals include a complete **52.770-GB
Authors snapshot** plus other dimensions, whereas the small EC2 test derived
Authors from its selected Works. The source snapshots and graph seeds also differ.
These rows describe the existing experiments, not an equal-input local/EC2 race.
The local small-tier q03 median of 33.630 s comes from the historical unstable run.
At 31.89m Works, local q02 already misses the 60-second target: warm median
65.285 s and maximum 239.892 s, despite 18 CPUs and 50 GiB. The newer small EC2
test had a 180-second query ceiling; the larger-run limit is not yet selected.

ClickHouse was faster than Athena on all seven queries in the small cross-check,
with every output matching in all three executions. ClickHouse queried preloaded,
normalized EBS tables; Athena read raw Parquet through normalization views each
time. Download and build time are excluded. ClickHouse query-log durations can include
server result streaming; Athena timings exclude SDK result fetching. These are
not end-to-end client latencies. This validates the two paths at this volume, not full-corpus capacity.

### Dataset and execution

The input was **2.759 GB (2.570 GiB) of Snappy-compressed Parquet**, comprising
**1,973,822 entity records** across 231 original OpenAlex objects:

| Entity | Records | Files | Compressed GB |
|---|---:|---:|---:|
| Works (publications) | 1,557,222 | 6 | 2.504 |
| Institutions | 143,455 | 83 | 0.094 |
| Publication sources | 268,629 | 136 | 0.156 |
| Topics | 4,516 | 6 | 0.0056 |
| Total | 1,973,822 | 231 | 2.759 |

Works came from six whole files, SHA-ranked across four update-date strata; this
is not a representative random sample of individual publications. The institution,
source and topic dimensions were complete.
Authors, author/work affiliations and citation edges were derived from the selected
Works, so they are not additional independent input records in this table.

The experiment ran in the certification test account in **us-east-1** on an
Ubuntu 24.04 ARM64 **m7g.xlarge (4 vCPU, 16 GiB RAM)** with 50 GiB of encrypted
gp3 storage. ClickHouse **26.3.12.3** ran inside Docker, limited to **4 CPUs and
8 GiB RAM**, with four query threads, a 6-GiB per-query memory ceiling and
1-GiB external aggregation/sort thresholds. No Docker-specific disk-I/O throttle
was configured. The gp3 volume was requested with default performance, documented
as 3,000 IOPS and 125 MiB/s; actual disk bandwidth was not benchmarked. See
[AWS gp3 performance](https://docs.aws.amazon.com/ebs/latest/userguide/general-purpose.html).

Athena engine 3 read the original public OpenAlex S3 objects in the same region.
Small symlink manifests listed the exact 231 objects; the ClickHouse downloader
used that same object list and conditional ETag checks. The source paths, row
counts, sizes and ETags were validated, including unchanged ETags before and after
the final Athena comparison. No raw-data S3 mirror was created. The source uses
update-date directories, which do not provide publication-year partition pruning;
Parquet column pruning still reduced measured scan sizes.

### Bibliometric query results

Timing cells below are medians of three executions. ClickHouse times are server
query durations; Athena times are total service execution durations, including
planning, queuing and service processing. ClickHouse server duration can include result streaming; Athena total duration
excludes SDK result fetching. Client end-to-end latency was not measured.
Athena result reuse was disabled; repeated executions were not a controlled
cold-cache experiment. Three samples do not justify a p95 claim.

| Query | Workload | ClickHouse median | Athena median | Athena scan/run | Matched output rows |
|---|---|---:|---:|---:|---:|
| q01 | Works by year/type/open access/XPAC | 0.023 s | 3.170 s | 16.01 MB | 6,928 |
| q02 | Topics by year, works and citations | 0.939 s | 4.526 s | 72.86 MB | 289,215 |
| q03 | Top authors by works, with citations reported | 0.773 s | 4.741 s | 696.96 MB | 1,000 |
| q04 | International collaborations by year/country pair | 0.378 s | 6.055 s | 713.79 MB | 37,019 |
| q05 | Incoming/outgoing citation neighbours | 0.005 s | 3.681 s | 139.53 MB | 95 |
| q06 | Distinct two-hop citation targets | 0.025 s | 4.357 s | 139.53 MB | 1 |
| q07 | Top 1,000 cited year/work pairs overall | 1.048 s | 5.032 s | 121.14 MB | 1,000 |

All returned rows were compared as typed multisets, preserving duplicates and
NULL values, rather than comparing only counts or checksums. A label-only harness
correction mapped ClickHouse's `t.topic_id` and `a.author_id` to Athena's column
labels; values were unchanged. The citation seed had both incoming and outgoing
edges (94 outgoing, 1 incoming) and 4 distinct two-hop targets, so graph agreement
was not vacuous. These are within-sample graph checks, not corpus-level
bibliometrics. None of q01-q07 exercises the normalized sources table; its raw
files were validated separately.

### Load, storage and memory

The 2.759-GB download took **42.45 seconds**. Two independent database builds took
**25.97 and 26.02 seconds**, with identical normalized correctness hashes. Active
normalized table parts occupied **270,957,492 bytes (0.271 GB)**; these retain the
fields used by this workload, rather than every field in the source objects.

Peak measured query memory was **1.581 GB**. The verified
`ExternalProcessingCompressedBytesTotal` counter was nonzero for q03
(about 60 MB/execution) and q07 (about 74 MB/execution), with the explicit 1-GiB
external-processing thresholds. The other five queries reported zero for this
counter. No memory or machine-size increase was made.

**Instrumentation correction for the older local results below:** their spill
checks used counters absent from the pinned ClickHouse image; missing counter
lookups returned zero. Historical claims of no spills, and memory conclusions
that depend on those claims, remain unverified. This correction does not change
the recorded historical latency measurements.

### Costs, cleanup and limits

Across all attempts, including startup and comparison-harness retries, Athena
reported **7.934 GB scanned**, approximately **US$0.040 in scan fees** after the
per-query minimum and rounding estimate. The conservative total estimate is
**US$0.081**, including EC2, EBS, public IPv4, seven-day S3 result storage,
shutdown padding and a US$0.01 allowance for small request/catalog/scheduler
charges. The published 21 Athena executions scanned 5.699 GB (about US$0.029 in scan fees);
other attempts and prechecks account for the remaining 2.234 GB. These are
estimates from live AWS list prices; the AWS bill was not yet
available, and credits and tax are excluded. Athena pricing is
[US$5/TB scanned](https://aws.amazon.com/athena/pricing/).

All three launched EC2 instances were terminated and their EBS volumes removed.
The experiment's termination schedules, Athena workgroups and Glue databases were
also deleted. Private manifest/result objects were intentionally retained in S3 with seven-day
object expiry, plus the persistent local study evidence. Published ClickHouse timings came from the third and final small-test EC2
instance; the first two instances failed before any benchmark timings were
produced. No ClickHouse timing samples were discarded. Published Athena timings
came from the final Athena-only comparison; earlier Athena attempts are excluded
from those latency samples but included in the all-attempt cost. One other attempt failed before EC2 launch. The final comparison
reused the completed EC2 measurements and ran only Athena; no additional EC2
instance was launched for the column-label correction.

The test stopped at these first figures. It validates this small sample and one
query stream, with no full-corpus load, multi-user test or tuning experiment.

### Committed evidence

The [measurement summary](../../results/aws-small-2026-11-06/summary.json) contains
all three timing samples, scan volumes, memory/spill counters, correctness hashes,
and the cost breakdown. The [source manifest](../../results/aws-small-2026-11-06/sample.json)
pins the exact public object paths, byte/row counts, ETags and downloaded SHA-256
values. The [query catalog](../../results/aws-small-2026-11-06/queries.json) contains
the executed ClickHouse SQL, equivalent Athena SQL and Athena normalization views.
The [local baseline](../../results/aws-small-2026-11-06/local-baseline.json)
records the five archived warm observations, their median/min/max summaries,
and input/resource sizes used in the
comparison below. Large output rows and machine-specific account/resource
identifiers are omitted. The pinned commit supplied SQL, schema and build helpers
from a fresh EC2 clone; the separate throwaway experiment harness is not included.
Its deployed guest-runner hash is recorded in the measurement summary.

Design, code and debugging findings were reviewed with Claude Code,
`claude-opus-5-5`, explicit `max` effort. Initial findings were verified and either
addressed or rejected with evidence; the relevant fixes passed follow-up review.

### Matched-volume comparison to complete

The requested follow-up runs target the local 2.00m, 10.11m and 31.89m Work tiers,
one ephemeral EC2 instance at a time, with an Athena comparison on identical
inputs and teardown after each tier. They have not run yet. The June 26 public objects behind these local tiers are now missing or changed;
this does not affect the verified October 14 sample above. The cached local copy
is verified at 98.302 GB.
Using a temporary private S3 copy is awaiting the user's data-path decision.

The historical local figures below are warm sequential medians, not p95 values.
The small-run q03 anomaly and other historical tails mean these numbers cannot by
themselves establish linear or nonlinear scaling. The new controlled EC2 series
will measure that question and the resources needed to keep each query under
60 seconds; full-corpus projections will remain estimates until tested.

| Works | Query | Local warm median (5 observations) | EC2 median | Athena median | Output agreement |
|---:|---|---:|---|---|---|
| 2,002,982 | q01 | 0.060 s | Not run | Not run | Not tested |
| 2,002,982 | q02 | 1.363 s | Not run | Not run | Not tested |
| 2,002,982 | q03 | 33.630 s | Not run | Not run | Not tested |
| 2,002,982 | q04 | 1.109 s | Not run | Not run | Not tested |
| 2,002,982 | q05 | 0.011 s | Not run | Not run | Not tested |
| 2,002,982 | q06 | 0.200 s | Not run | Not run | Not tested |
| 2,002,982 | q07 | 2.502 s | Not run | Not run | Not tested |
| 10,109,733 | q01 | 0.027 s | Not run | Not run | Not tested |
| 10,109,733 | q02 | 10.780 s | Not run | Not run | Not tested |
| 10,109,733 | q03 | 2.978 s | Not run | Not run | Not tested |
| 10,109,733 | q04 | 2.512 s | Not run | Not run | Not tested |
| 10,109,733 | q05 | 0.007 s | Not run | Not run | Not tested |
| 10,109,733 | q06 | 0.103 s | Not run | Not run | Not tested |
| 10,109,733 | q07 | 1.250 s | Not run | Not run | Not tested |
| 31,885,241 | q01 | 1.538 s | Not run | Not run | Not tested |
| 31,885,241 | q02 | 65.285 s | Not run | Not run | Not tested |
| 31,885,241 | q03 | 9.896 s | Not run | Not run | Not tested |
| 31,885,241 | q04 | 11.465 s | Not run | Not run | Not tested |
| 31,885,241 | q05 | 0.011 s | Not run | Not run | Not tested |
| 31,885,241 | q06 | 0.322 s | Not run | Not run | Not tested |
| 31,885,241 | q07 | 3.781 s | Not run | Not run | Not tested |

## Outcome

*Local 50-GiB results (2026-08-05). Historical no-spill claims and dependent memory
conclusions below are unverified; see the instrumentation correction above.*

The 50-GiB ClickHouse configuration is viable for the tested 98.302-GB raw
sample and 31,885,241-Work largest tier. The current medium-tier workload is
repeatably fast under 18 CPUs, 18 query threads, and one worker: three clean
repeats all met the stricter repeatability rule, with no 20-second tail, spill,
query error, server restart, or foreign-database merge activity.

The older matched 18-CPU/18-thread run had 25 medium-tier samples of at least
20 seconds and maxima above 200 seconds. Those tails did not recur in the
instrumented baseline or any repeat. The operational issue is therefore not
currently reproducible at this fixed configuration and byte-identical work
volume. Its historical cause remains unknown and cannot be recovered from the
old artifacts because they predate per-query timestamps and wait/I/O telemetry.

This does not turn the overall capacity verdict into a full pass. Large q02
still has a stable roughly 60-second floor, and the storage model has not been
validated at full OpenAlex corpus scale. Peak single-query memory remained
about 6.3 GiB of the 50-GiB container limit and no query spilled, so additional
memory was not the binding resource in these single-stream measurements.

## Medium-tier repeatability result

The fixed experiment used 10,109,733 Works, 50 GiB of ClickHouse container
memory, 18 CPUs, 18 query threads, and one closed-loop worker. Each repeat
captured 299 concurrent-phase samples. The predeclared rule required every
repeat to satisfy all of the following:

- routine p95 below 5 seconds and join p95 below 15 seconds;
- q03 and q07 maximum/median ratios below 2.0;
- no sample of at least 20 seconds;
- no in-flight or completed merge from a foreign database;
- no error, server restart, or spill.

| Run | Routine p95 | Join p95 | q03 max/median | q07 max/median | >=20 s | Foreign merges |
|---|---:|---:|---:|---:|---:|---:|
| Instrumented baseline | 1.571 s | 10.367 s | 1.059 | 1.129 | 0 | not gated yet |
| Repeat 1 | 1.566 s | 10.583 s | 1.047 | 1.050 | 0 | 0 |
| Repeat 2 | 1.716 s | 10.881 s | 1.077 | 1.191 | 0 | 0 |
| Repeat 3 | 1.574 s | 10.456 s | 1.094 | 1.094 | 0 | 0 |

Across the three gated repeats, join p95 ranged from 10.456 to 10.881 seconds,
q03 p95 from 3.008 to 3.132 seconds, and q07 p95 from 1.583 to 1.737 seconds.
All three repeats passed with wide margin. The instrumented baseline is useful
corroborating performance evidence, but it predates the strict foreign-merge
guard and is not counted toward that gate.

## Scope and controlled inputs

Both runs used identical manifests, selected Parquet objects, seed work IDs,
query SQL, tier sizes, class sample minimums, correctness gates, and latency
thresholds. Run-specific database names produce different rendered-SQL hashes
where those names are substituted; recomputation reproduces both recorded
identity documents and the repository SQL itself did not change between runs.

One worker issues a query and waits for it to finish before issuing the next.
The `concurrent` artifact name is inherited from the closed-loop harness, but
with `workers=1` these results measure one interactive stream, not simultaneous
multi-user load.

| Resource | Run A | Run B |
|---|---:|---:|
| Docker-visible memory | 54.823 GiB | 54.822 GiB |
| ClickHouse container memory | 50 GiB | 50 GiB |
| ClickHouse CPU limit | 16 | 18 |
| Query `max_threads` | 8 | 18 |
| Closed-loop workers | 1 | 1 |
| Per-query memory ceiling | 12 GiB | 12 GiB |

Run B is a joint CPU-and-thread experiment. It is not an isolated CPU test and
it does not change memory relative to Run A.

## Verdicts and correctness

| Run | Small | Medium | Large | Aggregate |
|---|---|---|---|---|
| A: 16 CPU / 8 threads | Pass | Pass | Fail | Fail |
| B: 18 CPU / 18 threads | Pass | Fail | Conditional | Fail |

For both runs and every tier:

- all blocking correctness gates passed;
- the normalized correctness hash matches across runs;
- 299 single-stream records were captured: 150 join, 99 routine, and 50
  one-hop records;
- no workload query error or unexpected server replacement occurred;
- no query spilled to disk and no class was undersampled.

The 299-record shape is intentional. Each six-query cycle includes two routine
queries, three joins, and one one-hop query. On the final cycle q05 reaches the
50-sample one-hop minimum, after which the harness stops before the final q07;
q07 therefore has 49 records while its routine class is already oversampled.

## Class performance

### Large tier

| Run / class | Median | p95 | Maximum | Peak memory |
|---|---:|---:|---:|---:|
| A join | 39.557 s | 306.858 s | 408.016 s | 4.34 GiB |
| B join | 12.464 s | 60.518 s | 63.981 s | 4.52 GiB |
| A routine | 5.144 s | 169.067 s | 217.084 s | 5.30 GiB |
| B routine | 0.085 s | 4.876 s | 5.062 s | 5.99 GiB |
| A one-hop | 0.017 s | 0.139 s | 0.665 s | 0.005 GiB |
| B one-hop | 0.014 s | 0.020 s | 0.254 s | 0.005 GiB |

Run B large q02 remained systematically expensive: median 59.705 seconds,
p95 61.170 seconds, and maximum 63.981 seconds. Other large queries were much
more stable: q03 p95 10.593 seconds, q04 p95 12.812 seconds, and q07 p95
4.968 seconds.

### Medium tier

| Run / class | Median | p95 | Maximum | Peak memory |
|---|---:|---:|---:|---:|
| A join | 3.398 s | 14.532 s | 33.556 s | 4.18 GiB |
| B join | 3.208 s | 53.270 s | 233.528 s | 4.19 GiB |
| A routine | 0.073 s | 1.984 s | 4.085 s | 4.14 GiB |
| B routine | 1.088 s | 99.010 s | 201.899 s | 6.20 GiB |

Run B's typical medium queries remained close to Run A, but q03 and q07 had
recurring extreme executions. For example, q03 had a 3.066-second median and a
233.528-second maximum; q07 had a 1.602-second median and a 201.899-second
maximum. The outliers are distributed across the run, sometimes in adjacent
q03/q07 bursts, rather than forming one continuous slow window.

Run B small passed its p95 gates but was not outlier-free: join maximum was
43.770 seconds, routine maximum 7.352 seconds, and one-hop maximum 1.659
seconds. The instability is therefore not exclusively a medium-tier property.

## What the evidence proves

- The ELT path is correct at the tested volume: raw Parquet is transformed into
  normalized ClickHouse tables that support bibliometric joins, aggregations,
  and citation traversal.
- The 50-GiB container has substantial single-stream headroom for this sample.
  Slow and fast executions of the same query read identical row counts, used
  overlapping memory envelopes, and did not spill. Data-volume differences and
  the container memory ceiling do not explain the latency excursions.
- Run B's large tier was faster and more consistent than Run A's large tier.
  This is a measured association under the joint 18-CPU/18-thread envelope.
- The reverse-citation projection cost 18.94 seconds to build in Run B. Warm
  median incoming-lookup latency fell from 0.009 to 0.004 seconds.
  Before-projection incoming samples were bimodal: two were zero, one was
  0.009 seconds, and three were approximately 0.26 seconds. After-projection
  samples were consistently near 0.004 seconds. Outgoing lookup and
  citations-by-year performance were essentially unchanged.

## What remains uncertain

- The original Run A/Run B experiment does not isolate CPU count from query
  threads: both changed. The new repeats establish stability only for the
  selected 18-CPU/18-thread configuration.
- The severe old medium-tier tails are not reproducible now, but their cause is
  not established. The matched historical run lacks the telemetry needed to
  distinguish host scheduling, cache/I/O stalls, or another environmental
  cause, so re-analysis cannot recover a definitive root cause.
- The repeatability result is scoped to medium. The large tier remains
  Conditional because q02 is consistently expensive, and neither the local
  sample nor its projection proves full-corpus capacity on an Alliance VM.
- Single-stream peak memory does not establish the memory requirement under
  multiple simultaneous users.

## Decision and future experiments

Stop the current repeatability series and ship the evidence. More same-config
repeats are unlikely to change the operational decision. An 18-CPU/8-thread
arm is worthwhile only if eight query threads becomes a real deployment
candidate. A `SYSTEM FLUSH LOGS` A/B is not justified: flushes occur after the
server-reported query duration and were present in both the old and new code.

The next performance work with a concrete decision attached is:

1. profile and optimize large q02 separately;
2. run a separately labeled worker-count experiment if multi-user capacity is
   required;
3. validate the storage/capacity model on the intended Alliance VM before a
   full-corpus commitment.

The immutable reports are
[`Run A`](../../results/stage2-single-memory50/report.md),
[`Run B`](../../results/stage2-single-memory50-cpu18/report.md),
[`instrumented baseline`](../../results/stage2-instrumented-18c18t-baseline/report.md),
[`repeat 1`](../../results/stage2-repeat-medium-18c18t-r1/report.md),
[`repeat 2`](../../results/stage2-repeat-medium-18c18t-r2/report.md), and
[`repeat 3`](../../results/stage2-repeat-medium-18c18t-r3/report.md).
