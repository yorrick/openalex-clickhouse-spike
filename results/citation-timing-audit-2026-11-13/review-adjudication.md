# Scoped timing review adjudication

Claude Code (claude-opus-5-5, max effort) completed a read-only review of six archived graph cases. Root verified the findings against run_engines.py, helpers.py and raw PostgreSQL/ClickHouse logs. No database, AWS or concurrency experiment was rerun. This review is scoped to citation timing interpretation and does not complete the historical full-experiment review.

Accepted: raw milliseconds-to-seconds conversions, medians, actual plan cardinalities and fingerprints match; the engines have different server timing scopes; client_seconds includes monitoring and telemetry serialization/write overhead; QA fetch timing includes canonicalization/hashing; q05 rows are not necessarily distinct neighbors; seeds have sparse incoming citations; family-max pairing is only a minor numerical issue. These amendments are explicit in the amended audit and documentation.

Accepted with limits: ClickHouse q06 reads roughly 1.25 billion rows / 10 GB logical bytes and consumes about 5.1–5.4 CPU-seconds per run according to query-log counters. Those are not physical EBS reads or measured multi-user capacity. No requests-per-second prediction is adopted.

Rejected as a demonstrated claim: the review's assertion that a 17.2 GB compressed citation table therefore fits in query memory. Compressed storage is not a measured working-set or peak-RAM bound. Also retain the review's earlier qualification that primer runs are not controlled cold-cache tests, despite its later shorthand calling them uncached.

The user explicitly authorized Claude Code for this review after earlier excluding it for PostgreSQL. Earlier DeepSeek/GLM attempts failed with the personal OpenRouter key's hard total-quota limit; no company credentials were used. Those failures remain recorded in the local study. Server timing values are unchanged; application-level speedups remain unmeasured.
