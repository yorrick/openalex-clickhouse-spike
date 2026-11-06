# Cross-AI review adjudication, current series

Reviewer in every invocation: Claude Code, `claude-opus-5-5`, explicit effort as recorded. Reviewers were leaf reviewers with tools and MCP disabled. Outputs and payloads are retained in the study directory.

## Tuning plan and implementation (max)

`tuning-review-result.txt`: BLOCK, process exit0. Accepted: getSetting instead of system.settings.value, exact native three-Work case-loop preflight, explicit inconclusive outcome, build and parts evidence, AMI identity guard, case-setting EXPLAIN, decision rules, preserved engine failure metrics, merged-scope/oracle checks. Local witness showed max_threads value `'auto(4)'` with changed0 while getSetting returned4. The deployed native fixture subsequently passed all five arms and exact output checks with max_threads18 and full telemetry before the 31.9m load.

`tuning-followup-result.txt`: BLOCK, process exit0. The reviewer explicitly resolved nine initial findings. Its two remaining claims were checked:

1. Accepted concern that20% drift exceeds the roughly8% baseline-to-target margin. The launched guest's original1.20 policy is preserved. A stricter1.08 secondary report rule was recorded at the timestamp in tuning-adoption-policy.json, before observing any large-cohort variant or closing-control result. All report adoption claims apply the stricter rule; there is no claim that it was the original preregistration.
2. Missing structured status for a preflight exception is a diagnostic limitation. The alleged100-minute idle cost is rejected: deployed bootstrap uses `set -Eeuo pipefail` and `trap 'shutdown -P now' EXIT` before the Python guest. A local shell witness confirms an immediate EXIT trap on a nonzero child result (bootstrap-exit-trap-proof.json). Job.wait also detects instance exit, captures console output, and fails when no complete primary summary exists. The actual native fixture passed, so no preflight failure affected these results. No rerun is justified by this hypothetical failure path.

The current deployed payload is extracted from archived user data and verified byte-identical, SHA2562981b06a0a9333227505f16edd602409634d486b64dbf0ec0f8cd02adde6ae9a. Do not describe the follow-up reviewer as having emitted PASS.

## Resource aggregation and report (high)

`resource-review-result.txt`: BLOCK, process exit0. Accepted and fixed: all-case99-comparison gate before publication, exact multiset mismatchFalse, conservative missing-value handling, operation-weighted await, explicit18-CPU denominator, external join/aggregation split, cold-versus-cold comparisons and limits on minimum-resource claims. The purported two-sample memory trace was an intentionally shortened reviewer excerpt: original31.9m q02 warm1 has132samples, including the reported peaks. Full traces are published as deterministic gzip.

`resource-followup-result.txt`: BLOCK, process exit0. The reviewer withdrew its missing-samples claim, verified the gates/math/folds, and left two text/assertion issues. Both are fixed: the summary names external join AND aggregation, and narrative assertions now check cold q03 versus cold q02 at all tiers, warm q03 reads below1MiB, the zero2m/0.785GB10m join values, zero10m aggregation, warm1 spill split and the maximum CPU usage. Eleven focused tests pass; narrative assertions also pass against all three real cohorts.

Additional accepted improvements: exporter no longer edits report prose, EBS readback proof is derived from completed preparation records, final rendering requires cost/tuning sections, sampling wording is nominal, throttle column shows maxima, and unsupported causal bottleneck labels are null. The full final results receive a final external review after tuning, costs and cleanup are complete.
