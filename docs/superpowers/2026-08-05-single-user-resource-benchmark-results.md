# Single-user resource benchmark results

## Outcome

The 50-GiB ClickHouse configuration is viable for the tested 98.302-GB raw
sample and 31,885,241-Work largest tier, but neither completed run meets every
predeclared latency gate. More importantly, the workload used only about
6.2 GiB peak query memory and never spilled, so memory capacity was not the
performance constraint in this single-stream experiment.

Run B made the large tier dramatically faster and more consistent than Run A,
but it also suffered severe intermittent tails at medium and isolated outliers
at small. One observation per configuration is not enough to attribute the
large-tier improvement causally to the larger CPU/thread envelope.

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

- The experiment does not isolate CPU count from query threads: both changed
  between A and B.
- One run per arm provides no run-to-run error bar. The severe tails moved
  between tiers across runs, so the entire large-tier improvement cannot yet be
  assigned causally to the resource change.
- Identical row counts and overlapping memory do not prove that ClickHouse's
  runtime plan, background merges, cache state, host contention, or thermal
  state remained identical. The existing artifacts lack per-query wall-clock
  timestamps and merge/event telemetry needed to distinguish them.
- Single-stream peak memory does not establish the memory requirement under
  multiple simultaneous users.

## Next experiment

1. Repeat 18 CPU / 18 threads at least three times to measure the noise floor.
2. Add an 18 CPU / 8-thread arm, then repeat all three arms at least three times
   while holding memory, workers, input, and SQL fixed.
3. Counterbalance tier order and record per-query wall-clock timestamps,
   `system.merges`, and relevant ClickHouse/system events.
4. Profile and optimize large q02 separately; its stable roughly 60-second
   floor is a query-design problem even in the more consistent run.
5. If multi-user capacity is required, run a separately labeled worker-count
   experiment after the single-stream variance is understood.

The immutable reports are
[`Run A`](../../results/stage2-single-memory50/report.md) and
[`Run B`](../../results/stage2-single-memory50-cpu18/report.md).
