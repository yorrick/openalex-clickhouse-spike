# Author notes: OpenAlex query benchmark artifact update

Target: existing artifact https://claude.ai/artifact/12VD4Wi6EzKtA2mdABXp6H (same URL, same title "OpenAlex query benchmark"). **Not published.** Waiting for root QA and an explicit publish instruction.

## Files (author-owned)
- `artifact-template.html`: the UI (CSS, HTML skeleton, vanilla JS), with `__PAYLOAD__` and `__BUILD__` placeholders. It uses no frameworks, remote data or external fonts.
- `build_artifact.py`: checks the payload against `payload-integrity.json`, writes every `<` as `<`, confirms the escaped JSON parses back identical, then writes `artifact.html`. After writing, it re-reads the inline payload and confirms that every SQL string and its SHA-256 match. It fails on an em dash or en dash in the template.
- `artifact.html`: the built page. Last build (after qa-corrections.md): payload `0a267717d9acc1108ea1b38e2e975c31aa7c9b84ffcd29b504616f98cf023705`, 1,193,397 bytes, 205 records; template `7539a714e47c...` (after review-corrections.md). SQL status: 177 exact_executed, 7 not_executed, 21 not_recorded.
- `qa-author.json`: the checks I actually ran.

## UI summary
1. Query explorer. The default cohort is 200.31m (`#cohort-select`). The table only shows engine columns that have records at that cohort, and it says which setups were not run. Hardware and setup for each column appear in the header and in callouts: original EC2 18 CPU / 50 GiB vs 200m 16 CPU / 32 GiB, 100m is local, and local ClickHouse history is timing-only with no SQL. Each cell is a `<button class="cell">` with `id="cell-<fam>-<engine>"` and data attributes `data-state` and `data-value` (complete or historical cells only). Arrow keys move between cells. The footer counts warm medians below 60 s.
2. Inspector (`#inspector`). It has selects for engine, profile and seed (`#engine-select`, `#profile-select`, `#seed-select`). The state bar `#ins-state` carries the data attributes. It shows the selected-seed median next to the family max-of-three value, and a failure banner `#ins-failure`. SQL goes in `#sql-body` via `textContent`, so it is byte-identical. The page shows the evidence SHA-256 and also recomputes it in the browser with Web Crypto (`#sql-sha-check[data-match]`). Copy (`#copy-sql`) uses the Clipboard API only. If the API is denied or unavailable, it shows an explicit failure in `#copy-status`, with no fallback and no auto-select. The inspector also shows requested vs effective settings, per-run query_log settings, every run with its kind, every metric with its measurement scope, failure telemetry, QA, compact PostgreSQL plan excerpts, a cross-cohort table and the source link.
3. Tuning history. Cards are generated for every cohort, engine and case that has more than one profile. Each card shows settings diffs against the baseline and same or different SQL by SHA prefix, with short notes on what each tuning attempt changed. The legacy q02 five-arm table keeps original_a and original_b as separate controls and lists the 31.89m cohort q02 (65.512 s) as its own series.
4. Dataflow. Clickable nodes for the native path and the Athena path, showing bytes, rows, method and current retention.
5. Rationale. 6 of 7 vs 3 of 7 is computed from the payload. Also covers PostgreSQL's graph-lookup wins and the unresolved q03.
6. Feasibility. Separate MEASURED, CONDITIONAL PROJECTION and UNVALIDATED columns, plus a storage-only slider for fixed + variable × N/200m.
7. Dataset, cost, methods and sources sections.

QA hook: `window.OA` exposes `{P, M, S, BUILD, setCohort, openCell, openProfile, select({cohort,engine,family,seed,profile}), currentRecord, currentCase}`. `buildModel(P)` is pure and works without a DOM.

## How amendments were handled
- `separate_cold_observation_as_archived` runs (33 of them, original 2/10/32m ClickHouse EC2) are shown as their own labelled row. They are not counted as warm repeats or included in medians. Medians use only runs whose kind starts with `warm`, and the payload median equals the median of those three for every complete record. The 31.89m q02 baseline row in the tuning table lists warm runs only.
- `qa.recorded_fingerprint_matches_raw_athena` is shown as a presentation-time join of stored hashes: "not a rerun and not an external validation". When the key is missing, the page shows "not recorded", never false.
- Methods now states the SQL coverage, computed from the payload: 184 SQL bodies, of which 177 were executed and 7 were prepared but not executed. 21 historical records have no SQL. The page never says all 184 were executed.

## Scoped input-contract review of build_payload.py
This covers UI and data integration only. It is not a review of the experiments. I did not edit the script or the payload. Root to verify:
1. **Dedupe keeps the first file's evidence.** `record()` drops a later record with the same (cohort, engine, case_key, profile_id) and only ORs `selected`. For 200m, `*-cases.json` is processed before `*-selected.json`. So the selected 200m native records with unsuffixed labels (PG q01, q04, the q05 and q06 seeds; CH q01, q07, the q05 and q06 seeds) carry runs and QA from the baseline-cases file. If the selected file holds a separate re-execution, those observations are dropped silently. The displayed medians match the brief's critical facts, so the impact may be nil. Please confirm the two files hold identical evidence for these profiles.
2. **Run kind default.** `'primer' if i==0 else 'warm'+str(i)` labels the first run as primer when a source run has no `kind`. The UI trusts `kind` for first-observation wording. Medians are unaffected: every complete record has exactly three warm runs.
3. **Seed parsing on `'-s' in name`.** Labels such as `q03-shm32-work512` contain `-s`. This is only safe because non-q05/q06 keys are reset. A future tuned q05 or q06 label with a suffix would produce a wrong seed and case_key. No such label exists now.
4. **Fingerprint join.** It asserts equality, so a mismatch would abort the build rather than record false. When the key is absent, it means no comparison was made, and the UI renders that.

Checked with no issue found: exactly one selected record per cohort, engine and case; no duplicate profile ids; family equals the case_key prefix; every SQL string hashes to its sql_sha256; non-complete records have a null median; every Athena record has three runs whose median equals `median_seconds`.

## Pre-publication corrections (qa-corrections.md)
- **Encoding and quirks mode (blocker).** The template now starts with `<!doctype html>`, `<meta charset="utf-8">` and `<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">`, the same as the prior published version. The template is now ASCII-only: the nine non-ASCII glyphs (curly apostrophe, ellipsis, arrows, multiplication and approximately-equal signs) are JS `\u` escapes inside the script. They render as the same glyphs. `build_artifact.py` now fails if the prefix is missing or the template has non-ASCII characters. The built page has no non-ASCII bytes outside the payload, and none inside it either.
  - Note for publishing: the Artifact tool wraps the page in its own skeleton (doctype, charset, viewport). The duplicate doctype and meta tags that end up inside the body are ignored by HTML parsers. I kept them because root asked for them and because they fix raw-file previews.
- **390 px page-wide overflow.** My diagnosis from reading the CSS (I did not measure in a browser): long unbroken strings sat in grid items whose minimum width defaults to their content. These were the inspector source URL, the payload SHA in Sources, and possibly the profile select's long option text. `overflow-wrap: break-word` does not reduce that minimum. Fixes:
  - `overflow-wrap: anywhere` on the body.
  - `overflow-wrap: normal` on tables, which keep scrolling locally inside `.tw`. Code, hashes and links in table cells still wrap anywhere.
  - `min-width: 0` on the children of grid and flex containers.
  - Inspector selects are now `width: 100%` of a flexible control (`flex: 1 1 14rem`), with `text-overflow: ellipsis`. The full option text stays visible in the open list, and the active profile is repeated in the state bar.
  - Nothing is hidden with `overflow: hidden`. Root needs to re-measure `scrollWidth` at 390 px.

## Cache wording correction (cache-wording-correction.md)
- The First observation caption for a primer now reads "first observation of this profile; not a controlled cold-cache measurement" for every setup. It no longer claims "after OS cache clear". The runs-table primer label uses the same wording.
- Archived separate cold observations (original ClickHouse EC2 series) keep their own label and stay out of medians.
- The Methods "Caches" entry is now scoped to 200.31m: the OS cache was cleared at each main engine phase boundary, not before each query. The grace-hash trial cleared it once before q02 and then ran q02, q03 and q04 in sequence. No deliberate cache clearing is claimed for the local PostgreSQL 2.00m/10.11m/31.89m runs or other earlier runs.
- No SQL, timings or runs were changed. The payload is unchanged (`0a267717...`).

## Independent review corrections (review-corrections.md, review-output.txt)
- **Keyboard focus (blocker).** The engine, profile and seed `change` handlers rebuild the inspector and then put focus back on the same select (`focus({preventScroll: true})`). Opening the inspector from a query-cell button does not move focus to a select.
- **Dataflow arrows at 390 px.** The base `.arrow .v { display: none }` rule came after the mobile media query and overrode it, so no arrows showed on mobile. It now comes before the query. On narrow screens each connection shows a centred vertical arrow on its own line, and the horizontal arrow shows on desktop. No arrow is hidden at either width.
- **Below-60 s footer.** A column made up entirely of historical timing-only records (local ClickHouse at 2.00m, 10.11m and 31.89m) now reads "not assessed (historical timing-only)" with `data-assessed="false"`, instead of 0 / 7. 200.31m stays ClickHouse 6 / 7 and PostgreSQL 3 / 7; this is not presented as six wins.
- The earlier corrections are kept: the doctype, UTF-8 and viewport prefix, the ASCII-only template, and the first-observation caption. No SQL, data or measured figures changed. The payload is still `0a267717...`.

## Verdict on root's exporter corrections (presentation-exporter scope only)
I accept all three as correct fail-closed fixes. Data meanings are unchanged, and the regenerated payload is byte-identical (`0a267717...`), which I confirmed.
1. The dedupe now asserts that a repeated profile identity has identical normalized evidence (everything except `selected` and `source`) before merging. This resolves my finding 1. One nuance: `source` is excluded from the equality check, so a merged record keeps the first file's link. At 200m both files link the same frozen-evidence tarball, so there is no visible effect.
2. `run.kind` is now required (`r['kind']`), and a missing kind raises an error. This resolves finding 2.
3. q05 and q06 identities must fully match `q0[56]-s<digits>`, and other families map to the bare family. This resolves finding 3.
4. A fingerprint mismatch still deliberately aborts the export. An absent comparison is never turned into false, and the UI renders it as "not recorded".

## Not done
- No browser or visual QA, screenshot, real 390 px render or screen-reader test. Tests ran in node against a DOM stub (string and structure level).
- The live artifact was not read, because the previous template was provided as its source.
- Nothing was published, watched or commented on.
