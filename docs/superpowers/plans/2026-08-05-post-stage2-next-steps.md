# Post-Stage 2 next steps

These items are intentionally deferred from the completed 98 GB Stage 2
validation. Keep the Stage 2 input selection, SQL, and report as the immutable
baseline so later results remain comparable.

## 1. Repeat the performance experiment

- Measure the effect of concurrency separately from the effect of hardware.
- Complete the remaining cells in this comparison matrix:

| Concurrent workers | 16 CPU / 32 GiB | Larger CPU/RAM envelope |
|---:|---:|---:|
| 1 | Run | Run |
| 3 | Existing Stage 2 baseline | Run |

- Choose and record the larger envelope before execution; it must be genuinely
  larger than 16 CPU / 32 GiB and have enough host memory for the container.
- Reuse the exact `stage2-v2` manifests, selected Parquet objects, query catalog,
  query envelopes, seed IDs, sample minimums, and verdict thresholds.
- Record query-class median, p95, maximum, errors, restarts, peak memory, spills,
  and storage. Compare each new result directly with the committed Stage 2
  report rather than changing the baseline thresholds after seeing results.
- Pay particular attention to the large-tier join tail: its current median is
  19.165 seconds and p95 is 140.781 seconds.

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
