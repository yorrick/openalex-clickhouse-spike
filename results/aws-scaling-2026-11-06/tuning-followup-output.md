# BLOCK

Two small edits remain before launch, and neither touches the Job lifecycle. Nine of the ten prior blockers are resolved, and #6 is only partly resolved. With both edits in and `test_tuning_cases.py` rerun, this is a PASS on the supplied evidence. I reviewed that evidence only and ran nothing.

## Must fix before launch

1. **The 20% control limit is too loose for an 8% target (prior #6).**
   - **Problem:** `controls_max_median_ratio=1.20` allows more drift than the 65s to 60s gap under test. Controls at 66s and 57s give a ratio of 1.16, so a no-effect arm that runs late at 58s gets `PASS` and the run reads `complete`. `original_b` might also show `PASS`, but nothing downgrades the arm.
   - **Fix:** set the limit to `1.08`, the size of the gap, which makes that example `INCONCLUSIVE_COMPARISON`. Baseline runs only spread 65–66s, so this should trip only on real drift. Change it now because `decision-policy.json` is the pre-registration. The existing tests still hold.

2. **A fixture failure never reports `failed`.**
   - **Problem:** `mount_raw()`, `fixture()` and `start_service()` all run before the `try` in `main()`. If the fixture raises, the full load is skipped as intended, but `status.json` is left at its last phase or absent, and no traceback is uploaded. Case errors survive in `fixture-tuning.json`, but a failure in the tiny load, query catalog or spill check leaves no reason from the guest.
   - **Impact:** this code doesn't show an immediate abort. The prior review recorded that `wait()` needs `status.json`, and the bootstrap isn't in this packet. If it doesn't catch the non-zero exit, the VM idles to the 100-minute limit, costing about $2.29. That is within budget.
   - **Fix:** open the `try` at the top of `main()`, set `service=None` first, and use `if service:service.down()` in the `finally`.

## Worth adding, not blocking

Some new `main()` lines still first run after the load:
- `save('build.json')`, because `fixture()` never serializes `profile` or either storage object
- the `openalex_benchmark.topics` check; I can't see the schema, and `seeds()` reads a singular `citation_edge`, so that table name is unproven
- `parts()`

These fail closed, so the cost is about 15 minutes of VM time (about $0.35) plus a rerun. To cover them, save those objects in `fixture.json`, and run the topic check and a database-parameterized `parts()` against `openalex_fixture`.

## Prior blockers

| # | Status | Basis |
|---|---|---|
| 1 | Resolved | All five controls use `getSetting`; your proof confirms `'auto(4)'` with `changed=0`. |
| 2 | Resolved | The real case loop runs all five arms on the VM before the load. |
| 3 | Resolved | Summary and driver use the experiment outcome; `status.json` is lifecycle only. |
| 4 | Resolved | Build and parts evidence use flat names, and the AMI guard runs before launch. |
| 5 | Resolved | EXPLAIN uses each case's flags and `actions=1`. |
| 6 | Partly | The clock, pass rule and saved policy are fine; the drift limit is not. |
| 7 | Resolved | Join limits are captured, and engine errors return a failed metric with telemetry. |
| 8 | Resolved | Scope, identity, oracle hash and row count are checked before launch. |
| 9 | Resolved as stated | Deadline checks hold; the 4-minute load and zero-merge figures are yours. |
| 10 | Resolved as stated | $0.081 fits the $1 allowance, but the cost report wasn't in what I received. |

For #8, your full-row match is the only evidence that `q02_signature` agrees with the canonical hash. The fixture can't test this because its expected hash comes from `q02_signature` itself.

## Also holds

- **Arms:** all five match the plan, including the closing control.
- **Fixture gate:** it uses only `all_cases_validated`, so tiny timings can't abort it, and a zero median can't divide by zero.
- **Raw data:** `copytree` skips `.data`, so fixture writes stay out of the raw mount.
- **Telemetry:** timeouts keep their samples, and `spill_bytes` stays `None` until the counter check passes.
- **Budget:** the formula still reserves the full $5 Athena envelope.
- **Claim limits:** those from the prior review still apply.

**Not supplied, so not reviewed:** `cloud_job.py` apart from the AMI guard, `scope.py`, `controls.py`, `tier_sql.py`, `source_copy.py`, `ClickHouseService`, the `cli` loaders, and the q02 and rewrite SQL.
