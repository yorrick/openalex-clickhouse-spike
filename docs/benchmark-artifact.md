# Interactive OpenAlex benchmark evidence

[Open the existing Claude artifact](https://claude.ai/artifact/12VD4Wi6EzKtA2mdABXp6H). The November 2026 update brings the original 2m/10m/32m results, local PostgreSQL and 100m comparisons, and paired EC2 200m results into one technical interface. It preserves the existing private sharing state; the owner controls sharing in Claude.

Select a cohort, query family, engine, seed and recorded tuning profile. The inspector shows exact SQL, SHA-256, requested/effective settings, individual observations, warm medians, available query plans, result fingerprints, and observed CPU, memory and I/O. Failure, timeout, not-run and historical timing-only observations have separate labels. The dataflow nodes expose the fourteen PostgreSQL index names, the ClickHouse reverse projection and Athena DDL; full table schemas and index DDL are in the dataset section.

The evidence favors ClickHouse for the tested broad analytical workload; PostgreSQL wins the indexed citation lookups. At 200,313,862 Works, ClickHouse meets the warm-median 60-second target for six of seven families and PostgreSQL for three. ClickHouse author aggregation has a memory failure and no valid median. Athena uses raw Parquet views, not an optimized CTAS layout; timing scopes and earlier hardware differ. The approximately 76 GB full-corpus estimate covers the selected 42-column schema and fixed complete dimensions only. It establishes neither query RAM nor full-corpus latency, and the richer final schema remains unvalidated.

The [200m report](ec2-200m-benchmark.md) remains the numerical reference. The historical full-experiment external review remains incomplete as stated there; reviewing this presentation does not resolve it. The later [scoped citation timing review](citation-timing-interpretation.md) explains the tiny cached PostgreSQL figures, request-latency limits, raw-Parquet ingestion and separately supplied memory settings. [Future data retention](benchmark-data-retention.md) now requires retaining the largest verified corpus and prepared database snapshots. The historical 200m volumes were deleted without snapshots, and the artifact states that explicitly.

## Reproducible presentation and verification

[Versioned artifact source and evidence](../results/benchmark-artifact-2026-11-13/) contain the self-contained HTML, immutable payload, assembly and extraction scripts, real Chrome QA, exact 200m Athena execution receipts, and review results. No new database or AWS experiment was performed for this update. `build_artifact.py` rebuilds HTML from the adjacent payload/template using Python standard libraries; `build_payload.py` records extraction from the original local study paths and requires those original archives.

Claude Code authored the interface with `claude --model claude-opus-5-5 --effort high` and publishes through its native Artifact tool to the existing URL. Codex CLI independently reviewed the presentation, first at max effort, then at high effort for the bounded corrections. Initial focus/mobile/footer findings were reproduced and corrected. The exact successful review commands were:

```sh
codex exec --model gpt-6-sol -c model_reasoning_effort=max --sandbox read-only --skip-git-repo-check --output-last-message review-output.txt - < review-prompt.md > review-cli.log 2>&1
codex exec --model gpt-6-sol -c model_reasoning_effort=high --sandbox read-only --skip-git-repo-check --output-last-message correction-review-output.txt - < correction-review-prompt.md > correction-review-cli.log 2>&1
```

Both commands exited zero; the second verdict is PASS. Real headless Chrome exercised all 205 profiles at widths 1440, 1000 and 390 (615 profile/viewport checks, including 552 exact-SQL checks), keyboard focus, copy success/denial, mobile layout, all 36 tuning links, five historical tuning arms, schemas and Athena DDL. No JavaScript errors were observed. Clipboard tests use a controlled browser stub, not the user's operating-system clipboard. Local browser QA does not establish anonymous hosted access. Publication receipts and a post-publication source-integrity check record the hosted version separately.
