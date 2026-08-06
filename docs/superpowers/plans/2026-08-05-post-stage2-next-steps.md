# Post-Stage 2 next steps

These items are intentionally deferred from the completed 98 GB Stage 2
validation. Keep the Stage 2 input selection, SQL, and report as the immutable
baseline so later results remain comparable.

## 1. Establish repeatability — completed

- Added server-side query start/end timestamps, CPU-wait and read-wait profile
  events, page-cache and read-byte counters, and phase-scoped merge evidence.
- Added a hard guard against any in-flight or completed merge from a foreign
  database during newly instrumented benchmark phases.
- Ran three independent medium-only repeats at 50 GiB, 18 CPUs, 18 query
  threads, and one worker against the same 10,109,733-Work input.
- Every repeat passed the predeclared stricter rule: routine p95 below 5
  seconds, join p95 below 15 seconds, q03/q07 maximum-to-median below 2.0, and
  zero 20-second tails, foreign merges, errors, restarts, or spills.
- The old long tails are not an ongoing reproducible problem at this fixed
  configuration. Their historical cause is not recoverable because the old
  matched run predates the new timestamp and wait/I/O telemetry.

Stop this repeatability series. Run an 18-CPU/8-thread arm only if that envelope
becomes a deployment candidate. Treat any future multi-worker run as a separate
capacity experiment, not as a correction to this single-stream evidence. See
[`Single-user resource benchmark results`](../2026-08-05-single-user-resource-benchmark-results.md).

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

The performance-repeatability item is complete. The remaining program is
complete only when the update design is proven against consecutive snapshots
and each accepted enrichment has explicit provenance and measured join
quality.
