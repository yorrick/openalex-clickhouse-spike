# Single-user resource benchmark results

## Outcome

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
