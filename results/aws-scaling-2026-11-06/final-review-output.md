**BLOCK, on one finding.** No rerun is needed: fix one phrase in the generator and re-render. I found no numeric errors in the supplied material, and this is the only finding I consider blocking.

## Blocking finding
The mechanism paragraph misstates the experiment. It says latency was unchanged "when only query memory increases" (`analyze_tuning.py:94`, also in the final report; line numbers are counted from the supplied text). No arm changed only query memory: `memory24` also raised both spill thresholds, as `analyze_tuning.py:65` and the effective settings confirm.

That second change had a measured effect. External aggregation fell from about 0.47 GB in both controls to 0 in all three `memory24` runs, while external join stayed near 2.20 GB. The conclusion survives, but the sentence claims an isolation the report itself disclaims, in the paragraph carrying the causal reasoning.

**Replacement:** "the unchanged automatic-join latency when query memory and the spill thresholds are raised together".

## Verified
- **Tuning:** I recomputed all five table rows from the per-run data, plus the 1.0075 control ratio, 11.5× speedup and join/aggregation split.
- **Cost:** row sums, the $3.515988 total, $47/month and $9.60/month all reconcile, and tier scan fees sum to the $1.10746 total within rounding.
- **Report math:** I checked the 99 comparisons (11 cases × 3 tiers × 3 repeats), Works and byte fractions, scaling multipliers, storage sums and CPU percentages. The 60 GB estimate also holds (3.526 GB × 16.007 + 3.364 GB = 59.8 GB), and cold read rates fit their monitoring windows.
- **Cleanup:** all 7 compute runs show verified termination, `vol-039919b5eb12aeb46` is the only volume left and is detached, and all 11 buckets show 7-day expiry.
- **Code:** I found no defect in `analyze_tuning.py` or `costs.py` that affects the current outputs.
- **Disclosure:** the 1.08 rule's timestamp falls after the 21:38:56 launch, the report does not call it preregistered, and the ratio passes both rules.

**Not independently checked:**
- Raw baseline JSON and telemetry weren't supplied, so the baseline tables were checked for internal consistency only.
- I did not open the ClickHouse source or AWS pricing pages. Your source findings and the rates match what I know.
- The claim that no variant results had been seen when the 1.08 rule was recorded rests on the policy record.

## Non-blocking
Items 2–4 can't be confirmed from the supplied evidence, but all three can be checked locally.

1. **Summary:** the 5.640 s sentence omits forced `parallel_hash` and the 24/8 GiB bundle. Name those and the 9.258 s rewrite under 12/4 GiB, since the tested configuration is a stated goal.
2. **Commit scope:** "The code commit deployed to guests" is unqualified, yet the adjudication records a tuning payload hash (`2981b06a…`) and post-review changes. Unless the commit is shared, say "baseline guests" and cite the tuning payload.
3. **Same OCI image:** the report claims this for tuning, but `analyze_tuning.py` guards only the AMI and the supplied tuning JSON has no image digest. Confirm it from the raw summary and copy the digest in.
4. **Record totals:** 630,105,216 minus Works and the four dimension counts leaves 187,148 records, while bytes reconcile within rounding (53.069 GB). Either the totals have different scopes or normalization drops rows, so check "complete" against the manifest.
5. **Full-corpus condition:** the text is accurate but leaves out the key condition. Proportional scaling needs at most 3.75 s at 31.89m to reach 60 s at 16×.
   - q03 (17.630 s), q04 (24.270 s), q07 (4.947 s) and both q02 fixes (5.640 s, 9.258 s) exceed that.
   - Proportional `parallel_hash` memory would be about 213 GiB, above this 128 GiB host.
   - Labelled as arithmetic rather than prediction, this shows "candidate" depends on more hardware or further tuning.
6. **Root occupancy:** this column depends on run order. Identical controls show 27.84 and 14.56 GB, and `memory24` drops from 25.80 to 15.45 GB between its first two runs. Add a sentence saying arms can't be compared on it.
7. **"Equivalent SQL rewrite":** the evidence is identical output on this cohort plus the three-Work fixture. Say "output-identical on this cohort" unless equivalence is argued from key constraints.
8. **Cost and cleanup evidence:**
   - The $1 allowance has no metered request counts behind it, so the total is an estimate rather than a proven upper bound. The under-$15 conclusion still has an $11.48 margin.
   - `cleanup.json` has no instance-profile field, although the report says profiles were removed.
   - Source deletion rests on a flag and one HEAD 404, not a listing.
9. **R&D draft:** it otherwise matches the report and claims no hours.
   - "environ 6,5 cœurs" should be 6,6 (6.57).
   - "copiés côté AWS puis téléchargés" reads as one chain, but `input-proof.json` shows two paths: a server-side copy for Athena and a direct OpenAlex download to EBS.
