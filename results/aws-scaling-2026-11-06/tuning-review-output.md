# BLOCK

Cost, termination, cleanup and raw-volume safety hold in the supplied code. The block is about results: the settings check will very likely fail all five cases after the full load is paid for, and `tune_guest.py` has never run. I reviewed the supplied evidence only and ran nothing.

## Must fix before launch

1. **The settings check will very likely reject all five cases.**
   - **Cause:** `main()` compares `system.settings.value` with `str(SETTINGS[key])`. Your fixture showed that an explicit `max_threads` equal to the default is dropped. In the 18-CPU container, `value` should therefore read `auto(18)`, possibly with literal quotes, rather than `18`.
   - **Impact:** each case raises `Effective setting mismatch`, is recorded as `failed_exception`, and the loop moves on. You would get no timings and add up to $2.75 to the prior compute a rerun must fit under $15.
   - **Confirm:** this is inferred from your fixture and my memory of ClickHouse discarding no-op changes. In the 4-CPU fixture container, run `SELECT value, changed FROM system.settings WHERE name='max_threads'` with `--max_threads=4`.
   - **Fix:** the `getSetting` fix exists only in `local_fixture.py`. Use it in the guest for all five keys, comparing as strings because `threads` came back as an int. Keep the `system.settings` rows as raw evidence.

2. **`tune_guest.py` has never executed.** `local_fixture.py` imports `benchmark_guest` and stubs `query`. The real `query()`, case loop, `q02_signature`, EXPLAIN capture and summary would first run on the paid one-shot run. Move the case loop out of `main()` and run it on the tiny fixture with `max_threads=4` and `cpus=4`, which reproduces the equal-to-default condition.

3. **Inconclusive runs are labelled complete.** `summary.json` always says `state: complete`, and the driver writes `state='complete'` even when `all_cases_validated` is false. That contradicts "never claim complete if absent". Keep `status.json` as the lifecycle signal because `wait()` needs it, but set the summary and driver state to `inconclusive` unless every case validated.

4. **Load and layout evidence is lost.**
   - Only the hash from `correctness` survives; `profile` and `storage` are never saved.
   - `OUT/'dimensions'` and `OUT/'tier'` never reach S3, and the root volume is deleted at termination.
   - `system.parts` isn't captured, and `system.merges` reading 0 can be a gap between merges rather than a settled layout.
   - `launch()` takes the current Ubuntu AMI without comparing it to the baseline's.

   Without these, a gap between `original_a` and the 65–66s baseline can't be explained. Save `build.json`, snapshot `parts.json` before the first case and after the last, and record both AMIs. Use flat names, because `fetch()` rejects subpaths.

5. **EXPLAIN doesn't reflect the treatment.** `entry['plan']` calls the client without `SETTINGS`, so `parallel_hash24` records a plan under default settings. Plain `EXPLAIN PLAN` doesn't show the join algorithm either. Pass the case flags and use `EXPLAIN PLAN actions=1`.

6. **There is no pre-registered decision rule.** Going from 65s to 60s is only an 8% gap with three samples per arm, and nothing evaluates `original_a` against `original_b`. Before launch, fix:
   - the clock, matching how 65–66s was measured
   - the pass rule, for example all three warm runs under 60s with QA matched
   - the control drift that makes a comparison inconclusive

## Check before launch

7. **Join limits:** a 2.67GB external join at a 4.1GiB peak suggests `auto` switches on a fixed limit such as `max_bytes_in_join`, not `max_memory_usage`. If so, `memory24` won't change the join. Forced `parallel_hash` may also throw `SET_SIZE_LIMIT_EXCEEDED`, which `query()` raises, losing that arm's metrics. Check the baseline config, capture `WHERE changed OR name IN (...)`, and add `join_overflow_mode` and `default_max_bytes_in_join`.

8. **Driver preflight:** the guest evaluates the merged config, and `scope.py` wasn't supplied.
   - Run `validate_scope(config)` and assert `manifest_identity(config)==manifest_identity(remote)`.
   - Pin `oracle` to `49bfb17b…` and `len(rows)` to 838464.
   - I read "agrees exactly" as covering `q02_signature`. If it only covered `canonical_rows`, test `q02_signature` too, because a format mismatch aborts the run at the first QA.

9. **Time:** the cases need about 30 minutes (5 cases × 5 executions × ~70s). Confirm that this plus the baseline load fits in 100 minutes, and that baseline merges settled within the 10-minute abort limit.

10. **Legacy cost:** the glob skips the legacy directory, so the $1 allowance for the older trial is assumed, not computed.

## Claim limits

- **Oracle:** Athena is still running, so claim only "matches baseline" until its q02 hash equals `49bfb17b…`.
- **No arm under 60s:** that result covers these five arms only. The rewrite plus `parallel_hash` is untested, so it wouldn't by itself justify bigger hardware.
- **Timing scope:** these are `FORMAT Null` runs, not delivery of 838,464 rows to a client.

## Passed

- **Budget:** $2.75 is correct (2 × ($1.3056 + $47/730 + $0.005)). The full $5 Athena envelope is reserved, and the $15 stop runs before any resource is created.
- **Termination:** the 100, 110 and 120-minute layers are independent, and the schedule stays until termination is proven.
- **Raw volume:** it is block read-only, mounted `ro,noload`, write-probed and bind-mounted read-only. `DeleteOnTermination=False` is verified, and cleanup never deletes it.
- **Scope:** there are no Athena scans, and only aggregate results reach the laptop.
- **Rewrite:** it is equivalent given `topic_id` uniqueness, which the guest checks, and full-row QA tests the result.
- **Arms:** they match the plan, settings are replaced per case, deadline skips are explicit, and `memory24` is correctly treated as a bundle.

**Not supplied, so not reviewed:** `scope.py`, `controls.py`, `tier_sql.py`, `source_copy.py`, `Experiment.__init__`, `create_role` and `record` (including any account check), `ClickHouseService`, and the `cli` loaders.
