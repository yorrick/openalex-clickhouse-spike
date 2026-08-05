# Single-user resource benchmark design

## Objective

Repeat the completed Stage 2 benchmark with one concurrent user under two
predeclared local resource envelopes:

1. more memory while preserving the existing concurrent-query CPU ceiling;
2. the same larger memory envelope with all locally available CPUs exposed to
   the query.

The existing `stage2-v2` artifacts remain the immutable three-user baseline.
No run may silently reduce a requested resource.

## Resource hierarchy and prerequisite

The host has 128 GiB RAM and 18 CPUs. Docker Desktop is currently configured
for a 48 GiB / 16 CPU Linux VM and exposes 46.963905 GiB to containers.
ClickHouse ran inside that VM with a 32 GiB cgroup limit. Concurrent queries
were separately limited to 7 GiB and eight threads.

A 50 GiB ClickHouse container requires 54 GiB of VM-visible RAM because the
preflight reserves 4 GiB for the VM and Docker services. Before either new run,
configure Docker Desktop for 56 GiB, restart it, and verify `docker info`
reports at least 54 GiB. Stop on failure; do not downgrade the container.

## Fixed comparison inputs

Both runs reuse the exact `stage2-v2` manifests, selected Parquet objects,
rendered SQL, seed IDs, three Works tiers, minimum 50 samples per query class,
and latency thresholds. The maximum closed-loop duration is predeclared as
18,000 seconds. The completed three-worker evidence contains about 9,494
seconds of aggregate large-tier query time; five hours supplies explicit
headroom for serial execution and telemetry round trips. Undersampling is a
hard experiment failure for these resource-comparison runs rather than a
Conditional verdict cap.

| Setting | Run A: memory | Run B: memory + CPU |
|---|---:|---:|
| Concurrent workers | 1 | 1 |
| ClickHouse memory | 50 GiB | 50 GiB |
| ClickHouse CPU limit | 16 | 18 |
| Concurrent query `max_threads` | 8 | 18 |
| Per-query memory ceiling | 12 GiB | 12 GiB |
| Maximum duration | 18,000 s | 18,000 s |

Run A intentionally retains eight query threads, matching the previous
per-query CPU ceiling while changing concurrency and memory as requested. Run
B changes only the CPU allocation and concurrent query thread ceiling relative
to Run A. The 16-to-18 CPU increase is only 12.5%; results must not be
generalized to a materially larger external VM.

The prior sequential evidence suggests the slow join is neither spilling nor
using enough memory to prove it is memory-bound, so little or no improvement is
an expected and reportable result rather than an execution failure.

## CLI and execution identity

Extend `stage2` with explicit options:

- `--cpus`
- `--workers`
- `--query-threads`
- `--maximum-seconds`

New checkpoints use execution identity version 2 and pin all four values in
addition to the existing memory, tier, input, configuration, and rendered-SQL
identity. Resume and report-only operations reject any changed value.

The approved backward-compatibility rule is narrow:

- a checkpoint without `identity_version` is a legacy version-1 checkpoint;
- detect the version from the recorded checkpoint before constructing the
  current identity document; the legacy branch calls the original version-1
  identity builder;
- legacy checkpoints are validated with the original identity document and
  retain their original defaults of 16 CPUs, three workers, eight concurrent
  query threads, and 3,600 seconds;
- supplying any new execution option while resuming or regenerating a legacy
  checkpoint is rejected;
- every newly created checkpoint is version 2, including runs that use the old
  default resource values.

This compatibility reader never changes or downgrades requested runtime
resources.

## Runtime changes

- Parameterize worker schedule construction and the closed-loop executor.
- `build_worker_schedules(catalog, workers)` returns exactly the requested
  number of rotations. One worker receives the complete unrotated six-query
  gated catalog in catalog order, including one one-hop query per cycle.
- Thread the worker count through schedule creation, the executor size, and
  worker submission. Thread `--query-threads` into `envelope_settings` instead
  of the current hardcoded value of eight.
- Use the requested CPU limit for the initial ClickHouse start, every per-tier
  restart, and `_run_projection_experiment`; Stage 1 retains its existing
  configuration-derived CPU behavior.
- Add a CPU preflight against Docker's visible CPU count before Compose
  mutation, analogous to the existing memory preflight. It runs inside
  `ClickHouseService.up` before the Compose call, so an 18-CPU request is
  refused until Docker Desktop exposes 18 CPUs and cannot silently become 16.
- Retain query telemetry needed to compare memory pressure: peak memory, spill
  bytes, rows, and bytes read. Add all four fields to `ConcurrentRecord` rather
  than discarding telemetry already returned by ClickHouse.
- Persist the execution envelope in tier summaries, the final report, and the
  checkpoint identity.
- Render all three memory-specific limitations conditionally. A completed 50
  GiB run must not say it used 32 GiB, must not say 50 GiB was unreachable or
  requires a different Docker environment, and must drop only the unvalidated
  50 GiB clause while retaining the separate Alliance limitation.
- Pass the CLI maximum duration directly to `run_closed_loop`; do not alter
  `config/experiment.toml`, whose hash is part of legacy checkpoint identity.
- After writing concurrent evidence, abort the resource-comparison run if any
  class has fewer than 50 successful samples. Do not finalize a comparison
  report from under-sampled evidence.

## Commands

Run A:

```bash
uv run openalex-spike stage2 \
  --memory-gb 50 \
  --cpus 16 \
  --workers 1 \
  --query-threads 8 \
  --maximum-seconds 18000 \
  --run-id stage2-single-memory50
```

Run B, after changing Docker Desktop from 16 to 18 CPUs and verifying the
visible CPU count:

```bash
uv run openalex-spike stage2 \
  --memory-gb 50 \
  --cpus 18 \
  --workers 1 \
  --query-threads 18 \
  --maximum-seconds 18000 \
  --run-id stage2-single-memory50-cpu18
```

## Acceptance gates

- Existing `stage2-v2 --report-only` remains Docker-free and reproducible.
- New checkpoints reject CPU, worker, thread, duration, memory, tier, input,
  configuration, or SQL drift before service mutation.
- Docker CPU and memory preflights pass before each run with no fallback.
- Every query class reaches 50 successful samples. Undersampling, errors, and
  server restarts are hard failures for these resource-comparison runs.
- All existing correctness gates pass at every tier.
- Reports disclose the exact resource envelope and compare medians, p95s,
  maximums, memory, spills, errors, and restarts with `stage2-v2`.

## Run A storage-sampling incident and resume design

The first Run A attempt completed its dimension load and the small-tier SQL
load, then failed in the storage monitor's exact final host-filesystem scan.
`os.walk` had listed a ClickHouse part file that a background merge removed
before `Path.stat` reached it. The resulting `FileNotFoundError` was a
time-of-check/time-of-use race in benchmark telemetry, not a ClickHouse query
or load failure. The checkpoint remains `in_progress`, has complete dimensions,
and records no completed tier. Exact-command resume therefore reuses the
dimensions and restarts the small tier after the existing work-table reset.

The user approved one narrowly scoped concurrency rule for allocated-size
sampling:

- represent a scan as both `allocated_bytes` and `vanished_files`;
- after a child file has been returned by `os.walk`, catch only
  `FileNotFoundError` from that child's `stat`, exclude the now-absent file from
  the instantaneous total, and increment `vanished_files`;
- make `os.walk` traversal errors explicit, and continue propagating
  `PermissionError` and every other I/O error;
- add `filesystem_vanished_files` as the last `StorageSample` field with a
  default of zero, preserving existing positional construction;
- cache the complete scan result in the decimated sampler so cached byte and
  vanished-file values always come from the same scan;
- for every storage-sample population reaching a version-2 report, normalize
  persisted pre-change samples by adding a zero value when the field is absent;
  this explicitly includes `checkpoint["dimension_storage_samples"]`, which
  Run A retains across resume, as well as tier and projection samples; preserve
  legacy version-1 report bytes and leave Stage 1 report shaping untouched;
- test vanished-child accounting, non-suppression of permission and traversal
  errors, positional compatibility, final-sample behavior, decimated-cache
  coherence, and a version-2 mixed-provenance report whose dimension, tier,
  and projection sample populations all expose the same telemetry keys.

This is not a general retry or filesystem-error fallback. It gives a precise
meaning to one expected race while retaining visible telemetry about it and
failing on all errors outside that definition.
