# PostgreSQL local benchmark evidence

The [report](../../docs/postgres-local-benchmark.md) describes the methods and limits. `summary.json` holds baseline family/case summaries; `cases.json.gz` contains all plans, settings, SQL, timings, resources and QA for the measured cases, including the q03 rewrite and original-SQL control. `telemetry.json.gz` holds the complete cgroup traces. Loading, indexing/storage and synthetic update probes are archived separately.

The harness expects the historical cached files and local study directory recorded in provenance, not a public reproducible service. Credentials, PGDATA, intermediate temp files, and large canonical-result exports stay in the local study. No benchmark is added to CI. No Claude Code validation was requested or performed for PostgreSQL.
