# Verdict: BLOCK

The gates, folds and unit math pass, and no reruns are needed. Two narrow report issues remain, both text or assertion edits. Prior #1 is withdrawn: 132 samples over 65.315 s is about one every 0.499 s, and the 7,649,484,800-byte anon and 37,041,070,080-byte file peaks are real full-trace peaks.

## Blocking issues

### 1. Some narrative claims still have no golden assertion
The rewritten cold claim is the main gap, and its direction can't be verified. The report says "Cold q03 has more physical reads and I/O pressure than cold q02", but only the q03 values are asserted, and no cold q02 values were supplied. The sentence also has no tier scope, although the table below it covers three tiers.

| Claim | Current state | Fix |
|---|---|---|
| Cold q03 exceeds cold q02 | Not asserted | Assert reads and stall at all three tiers, or scope the sentence to 31.89m |
| Warm q03 has "essentially no physical reads" | Not asserted | Assert a stated threshold |
| 10m external join is 0.785 GB, and 2m is zero | Not asserted | Assert from `resources`; also assert 10m aggregation is zero |
| 2.67 GB "per run" | Only warm1 is tested | Assert all three runs, or say "in warm1" |
| "Up to about 16-17 cores" | Only q07 is bounded, at 15.5-16.5 | Assert the maximum across families, or say "about 16" |

For the cold claim:

```python
for d in datasets.values():
    c2 = d['cases']['q02']['cold_resources']
    c3 = d['cases']['q03']['cold_resources']
    assert c3['physical_read_bytes'] > c2['physical_read_bytes']
    assert c3['io_stall_fraction'] > c2['io_stall_fraction']
```

If this fails at any tier, the sentence has to change. These assertions only run in `finalize_report.main()`, so include that run's output with the fix. The focused tests don't execute them.

### 2. The summary still omits aggregation spill
Prior #6 was fixed in the sizing section, but the summary still says q02 "performs external join work". Warm1 also spilled 0.471 GB of external aggregation. Change it to "external join and aggregation work".

## Non-blocking
- **Status gate:** `validate_analysis` still ignores `status`, so a primer timeout, a primer memory failure or an extra failed warm record would pass. Add a check that `c['status']` is `PASS` or `FAIL_LATENCY`.
- **Failure after export:** the goldens run after `export()`, which has already rewritten `REPORT`. A golden failure would leave the report in an intermediate state, with the stale "2m tier" section and possibly the hard-coded `All matched, <60 s CH` label, which is false for q02 at 31.89m. Remove the `REPORT` edits from `export_report.py`.
- **Hard-coded proof field:** `every_ec2_filesystem_readback_sha256_and_footer_count_matches` is a literal `True` in `input-proof.json`. Derive it from the readback evidence.
- **Cost section:** the report promises a "cost section below", but `cost-report.md` is skipped silently if absent. Raise an error instead.
- **Possible string sizes:** `fixed=sum(r['bytes'] ...)` has no `int()`, unlike the other `table_bytes` reads. If the values are strings, finalize will crash, which at least fails closed.
- **Sampling wording:** the blanket "every 0.5 seconds" isn't checked against `telemetry_max_gap_seconds`. Say "nominally" and point to the per-run count and maximum gap.
- **Throttle column:** a median can hide throttling in a single run, so the maximum may be more useful.
- **Published `bottleneck` field:** `classify` still treats NVMe utilization of at least 0.8 as I/O-bound. The report doesn't use this field, but the JSON still publishes it.
- **Test coverage:** there are no direct tests for stall, utilization, one-sample input, a dropped device, or the `max_med`, `max_peak` and `num` folds. Reading the code, they behave correctly.

## Verified from the code
- **Gate:** it runs before export and requires 3 complete tiers, quiescent merges, 11 exact cases, and 3 warm, 3 resource and 3 Athena records per case. All must match, for exactly 99 comparisons. `False` is preserved, and the warm count also rules out a primer labeled `warm`.
- **Await and missing values:** await is operation-weighted per run, then folded as a per-case median and maximum seed. Missing CPU keys, anon/file values, dropped devices and per-run metrics stay unknown rather than becoming 0.
- **Spill split:** 2,202,536,825 + 470,815,333 = 2,673,352,158 bytes, matching the report's split for warm1.
- **Derived figures:** the growth multipliers, cohort percentages, 16× factor, download minutes and table column counts are correct. `m7g.8xlarge` EBS limits match the report.
- **Report limits:** PSI semantics, the 18-CPU denominator, the throttle column, and the limits on cache state, NVMe percentage, minimum resources, SLA and the 60 GB arithmetic are all present.
- **Traces:** archives are deterministic, using `mtime=0` and sorted keys.

## Not verified
- **Tests:** only 5 of the 9 passing tests were supplied.
- **Finalize run:** no `finalize_report.main()` output was supplied, so I can't confirm the goldens pass.
- **Raw evidence:** I relied on your statement and the test for the raw trace. Cold q02 values were not supplied.
- **Unsupplied or hard-coded content:** `tuning-report.md`, `cost-report.md`, the history report, and the hard-coded commit, image and settings prose.
