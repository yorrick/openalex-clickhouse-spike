# Independent review and adjudication

Claude Code reviewed this study as a leaf reviewer, using claude-opus-5-5. The initial plan and full evidence review used max effort. The bounded correction review used high effort. All three CLI processes completed successfully with exit code 0 and empty stderr. A successful CLI exit is not itself a PASS verdict.

The initial plan verdict was not PASS. The full evidence review verified the recorded values and integrity, conditional on two interpretation corrections. The correction review returned PASS after those edits. This covers the local extraction study, not earlier PostgreSQL/ClickHouse experiments or a production export service.

## Initial plan findings

1. Independent correctness: compare exported values against a non-DuckDB reader, preserving nested values and duplicate counts. Implemented using raw PyArrow and canonical multiset hashes. Nested population checks were completed after the main runs, not before, and confirmed 15,595 matching records with nonempty authorships.
2. Layout and transfer interpretation: preserve Parquet format, selectivity, row groups, column sizes and page-index evidence. Every row group contains 2018 records. Row-group bytes are not claimed as a universal floor for page-aware readers.
3. Network counter: HTTP Content-Length sums were checked with continuous per-process observation. The one-shot post-query counter missed prior traffic and its check exited 1. Continuous observation matched body bytes plus plausible protocol overhead. Sampling per-flow peaks also misses some short flows.
4. Authentication: isolated config/credentials/secrets, explicit anonymous config, no credential fetching, runtime matched-secret inspection, unsigned baseline and absence of signing-related header names. Logger values are redacted, names remain. The archive contains 3,702 extraction requests plus four preliminary probe requests; all 3,706 have only host, user-agent, range and if-match request headers.
5. Resource scope: fresh-process RUSAGE_SELF, macOS byte units, separate 8 GB database and 12 GiB RSS limits, process CPU around COPY. Initial temp-space cap absent, but every profile reports zero spill; follow-ups set 4 GB. Physical disk bandwidth and IOPS were not measured.
6. Repeated/local comparison: three fresh processes per extraction arm, matching query settings, with local OS cache explicitly uncleared. The one unsigned full-download baseline is not a repeated throughput comparison. Arms were sequential, not interleaved.

## Final evidence-review findings

F1 accepted: default caching reduces overlapping range bytes, but changing network throughput prevents attributing the entire 94.2-to-66.9 s difference to caching. Report and R&D draft corrected.

F2 accepted: API request spacing creates a 36.96 s floor before the final response. The 37.3 s median is not maximum API throughput. API/S3 coverage, freshness, schema and output formats differ. Report, draft and protocol corrected.

F3 accepted: extra full/narrow observation 4 overlapped, as first-request timestamps confirm. They remain excluded from primary medians.

F4 accepted: header names, isolated empty credential paths, explicit config and runtime selection support anonymity; logger values are not unredacted proof. Report corrected.

F5 accepted: final source HEAD and extra QA establish consistency across all phases. Raw SHA-256 recheck is recorded in extra-qa.json, not final-qa.json. Report cites both.

F6 optional suggestion omitted: synthetic page-size simulations are not measurements of this file's physical page layout. No universal pruning floor is asserted.

F7 accepted: default_cache_variant.py did not enforce the follow-up 5 GiB guard live. Post-run reconciliation gives 4,063,697,670 bytes, within the guard. The late nested-population check and sequential-arm design are disclosed. The R&D draft removes the overstated repetitions_statistiques tag and retains hours:null.

## Failures and corrections retained

An initial extra-observation which_secret call used scalar syntax and failed before its query. It was corrected to table-function syntax. A subsequent full extraction succeeded, but its one-shot network assertion failed because the counter did not include earlier traffic. That observation is retained and excluded from latency medians. A continuous observation independently reconciled received bytes. These were measurement-harness issues, not source-data equality failures.

The cache-disabled arm is retained under its actual setting. Default-cache results are an additional measured arm, not a replacement of historical evidence. The publication QA initially counted 3,706 requests against the review's 3,702 extraction-only count; the four preliminary probe requests explain the difference. Both scopes are now explicit.
