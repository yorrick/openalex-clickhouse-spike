# Verdict: BLOCK

The core unit math is correct, and `REAL31M_Q02` cross-checks well. The blockers are in peak-memory evidence, final-state gates, missing-value handling, and three report claims. None of the fixes needs a rerun.

## Blocking issues

1. **Memory peaks are not shown to be 0.5-second peaks.**
   - `REAL31M_Q02` has only 2 telemetry samples, 65.315 s apart, not about 131. `resources()` therefore takes the larger of the two endpoints.
   - That gives 6.03 GB anon, while start anon (3.52 GB) plus query peak (4.38 GB) could reach about 7.90 GB if additive. The true peak is unknown.
   - Disk, CPU and pressure deltas are valid from endpoints, but the `container_sampled_peak_*` fields and the report's "sampled every 0.5 seconds" text are not.
   - **Fix:** Count samples per record. If the intermediate samples weren't persisted, label these values as window-endpoint maxima and report true peaks as unknown. If this excerpt was trimmed, restore the samples and add a sample-count gate.

2. **The report gate can publish a false 99/99.**
   - `finalize_report.py` checks `qa_matched` only for `q02`. A mismatch in `q05` still has Athena durations, so it passes the gate and the hard-coded "99 of 99" is published.
   - `matching` also collapses a real mismatch to `None`, which makes it look pending rather than failed.
   - The gate ignores `athena_all_matched`, `status`, `merges_quiescent` and `state`. It also doesn't require 11 cases per tier or 3 completed warm runs per case.
   - `export()` runs before the gate, so a failed gate may still leave exported output.
   - **Fix:** Gate before export on exactly 33 matched comparisons per tier and 99 overall, with all status and state checks. Use `False` for a mismatch and `None` only for pending.

3. **The prose findings are hard-coded, not generated from evidence.**
   - This covers the q02 range and growth, CPU and memory figures, spill, cold q03, the 60 GB extrapolation and "every other case below 25 seconds."
   - For example, warm1 q02 writes 27.37 MiB/s, so "roughly 24" holds only if the other two runs are lower.
   - **Fix:** Compute these values or assert each against the evidence before writing the report.

4. **The await fold breaks the stated aggregation rule.**
   - `wait_values` pools every device, run and seed, and gives a window with one stray I/O the same weight as one with 7,844. That contradicts "maximum seed median for graph families."
   - **Fix:** Compute I/O-weighted await per run across devices, take the median per case, then the maximum across seeds. Show `n/a` if a run has no I/O.

5. **Missing metrics do not always stay unknown.**
   - `.get('anon',0)` and `.get('file',0)` turn missing values into zero.
   - One missing CPU key undercounts CPU, because the other is still summed.
   - A device missing from the last sample is dropped, which understates the totals.
   - `max_threads` defaults to 18 when absent.
   - `max_med` can silently take the median of 1 or 2 runs under a "median of three" label.
   - All-missing metrics crash with `StatisticsError`, `KeyError` or `TypeError` instead of rendering as unknown. A crash fails closed, but the requested output is still `unknown`.

6. **The external-processing claim is mislabeled.**
   - In this run, 2.67 GB is **join 2.203 GB plus aggregation 0.471 GB**, yet the report calls it external join processing.
   - The summary also omits that aggregation spilled. Split the 10m value the same way.

7. **The cold comparison is invalid.**
   - "More dependent on disk reads than warm q02" and the following "by contrast" compare cold q03 with warm q02.
   - **Fix:** Compare cold q03 with cold q02, or with warm q03.

8. **"Sufficient… except q02" implies an unproven resource limit.**
   - The evidence shows q02 missed 60 s at about 4.8 of 18 cores, 4.1 GiB and negligible I/O stall. It doesn't show that the container was the cause.
   - **Suggested wording:** "All baseline warm cases except q02 at 31.89m met the single-user target under the tested settings; the q02 miss is not attributed to the container limit."

## Non-blocking corrections

- **File-cache dependence:** q02 made 103.98 GB of file-descriptor reads with almost no physical reads, while file cache stayed near 34.9 GB. Low stall therefore applies only with this cache state, so "reclaimable" shouldn't suggest the cache is unimportant.
- **Per-query container memory:** Anon and file peaks include state inherited from earlier queries. Say so under the table.
- **Bottleneck label:** `classify` receives NVMe utilization and uses `max_threads` as the CPU denominator. Check that utilization isn't treated as capacity, and use 18 for allocated-CPU percentages.
- **I/O stall label:** This is PSI `some`, so 11.5% doesn't mean 11.5% of the work was blocked.
- **Throttling:** The windowed value is retained but not shown. It was 0 here, but it matters for the 16-17 core queries.
- **Storage extrapolation:** Scaling linearly from a non-random cohort, with peak occupancy unknown, doesn't fully support "Storage alone does not force a multi-node design." Soften it to the arithmetic result.

## Tests

The existing assertions are correct, but they leave these gaps:
- The fixture has zero read and write op deltas, and pressure doesn't change. IOPS, await, utilization, stall and throttling are therefore never meaningfully tested.
- The missing-value test doesn't cover anon/file, stall, rates, one CPU key, a dropped device, or one sample.
- `finalize_report.py` has no tests for its folds, gates or rendering of unknowns.

Add a golden test using `REAL31M_Q02`:

| Metric | Expected |
|---|---|
| Query CPU | 310.679 s, 4.768 cores, 26.5% of 18 |
| Container CPU | 4.898 cores, 0 s throttled |
| Query peak | 4.080 GiB |
| Endpoint anon / file maxima | 5.617 / 32.494 GiB |
| Host read / write | 12,288 / 1,874,493,440 bytes |
| Write rate | 27.37 MiB/s |
| Summed IOPS | 120.14 |
| `nvme0n1` await / utilization | 3.933 ms / 2.687% |
| I/O stall | 0.0001% |

## Verified

- **Metrics:** `/proc/diskstats` indices, 512-byte sectors, await, IOPS, PSI and cgroup conversions are correct.
- **Cross-checks:** Query CPU (310.7 s) is consistent with cgroup CPU (319.9 s). Host writes (1.874 GB) match the cgroup write delta (1.872 GB).
- **Report math:** The 99-comparison count, q02 growth multipliers, cohort percentages, table column counts and the limits on minimum-resource claims are all correct.

**Not reviewed:** `controls.py` and `export_report.py` weren't included, so `classify`, `outcome`, field renames, cost, cold fields and any gates there remain unchecked. Also confirm the primer's `block` value doesn't start with `warm`.
