# Post-Stage 2 next steps

These items are intentionally deferred from the completed 98 GB Stage 2
validation. Keep the Stage 2 input selection, SQL, and report as the immutable
baseline so later results remain comparable.

## 1. Establish repeatability and isolate compute variables

- The two one-worker, 50-GiB runs are complete. Treat them as single-stream
  latency evidence: one worker issues one blocking query at a time. They do not
  measure multi-user concurrency.
- Run at least three independent repeats of one fixed configuration, starting
  with 18 CPU / 18 query threads, to measure the p95 and maximum noise floor.
  Recreate the container between repeats while retaining the same pinned input.
- Then isolate one variable per arm, with at least three repeats per arm:

| Arm | CPU | Query threads | ClickHouse memory | Workers |
|---|---:|---:|---:|---:|
| A, completed | 16 | 8 | 50 GiB | 1 |
| CPU isolation | 18 | 8 | 50 GiB | 1 |
| B, completed | 18 | 18 | 50 GiB | 1 |

- Reuse the exact `stage2-v2` manifests, selected Parquet objects, query catalog,
  query envelopes, seed IDs, sample minimums, and verdict thresholds.
- Record query-class median, p95, maximum, errors, restarts, peak memory, spills,
  and storage. Compare each new result directly with the committed Stage 2
  report rather than changing the baseline thresholds after seeing results.
- Add per-query wall-clock timestamps and sample `system.merges` and relevant
  system events. Slow and fast executions currently read identical row counts
  with overlapping memory use and zero spill, but the recurring tail mechanism
  is not instrumented.
- Counterbalance or randomize tier order across repeats. Run A was stable at
  medium and unstable at large; Run B showed intermittent outliers in every
  tier, with its most severe non-q02 tails at medium.
- Treat a three-worker 50-GiB run as a separate multi-user capacity experiment,
  not as a correction to these intentionally single-user measurements.

## 2. Design the update path

- Establish the required refresh cadence and acceptable data staleness.
- Inspect how OpenAlex publishes additions, modifications, deletions, merged
  entities, and manifest changes across snapshots.
- Compare full snapshot rebuilds with an incremental design based on
  `updated_date`, including how each approach handles late corrections and
  deletions.
- Define stable versioning and atomic activation so readers see one internally
  consistent snapshot across Works, dimensions, bridges, and citation edges.
- Specify idempotency, restartability, audit metadata, reconciliation gates,
  storage overlap during refresh, and recovery from an interrupted update.
- Validate the chosen design by applying at least two consecutive pinned
  snapshots and proving that the refreshed database matches a clean rebuild.

## 3. Design enrichments

- Identify the bibliometric questions that OpenAlex alone cannot answer before
  selecting enrichment sources.
- Evaluate each candidate on join-key coverage, licensing, provenance, refresh
  cadence, correction/deletion behavior, expected size, and analytical value.
- Consider both derived enrichments (for example field-normalized citation
  indicators or collaboration classifications) and external enrichments (for
  example organization, funder, retraction, or publication metadata).
- Keep canonical OpenAlex fields unchanged. Store enrichment source, source
  version, retrieval time, join method, and confidence or match status in
  separate typed tables.
- Measure match coverage, ambiguity, duplicates, unmatched records, and query
  cost before treating an enrichment as production-ready.

## Completion criteria

These next steps are complete only when the performance comparison is
reproducible, the update design is proven against consecutive snapshots, and
each accepted enrichment has explicit provenance and measured join quality.
