# Author notes: OpenAlex query benchmark, version 5

Artifact: https://claude.ai/artifact/12VD4Wi6EzKtA2mdABXp6H (same URL, private). Version 4, id 1794173636-dad9.

## Changes in this revision (qa-corrections.txt)
1. Mobile overflow: `section, .calc, header.top, .inspector, .ins-head, .ins-sec, details.box > .in, .node-detail` get `grid-template-columns: minmax(0, 1fr)`; `.calc, .tw` get `min-width: 0; max-width: 100%`. Tables still scroll inside `.tw`. No global overflow hiding.
2. Follow-up: inline `code` inside `.note`, `.lead`, `.callout`, `.facts-list`, `.warnline`, `dl.kv`, `.sqlnote` wraps (`overflow-wrap: anywhere; word-break: break-word`), and so do the cohort-facts spans. `pre.code` is unchanged (`white-space: pre`, horizontal scroll).
3. `<meta charset="utf-8">` and a standard viewport meta now come first in the file.
4. Copy button: Clipboard API only. On failure or when the API is unavailable it shows "Copy failed: clipboard unavailable here". It no longer auto-selects text.
5. Sources: the payload bytes and SHA-256 are now labelled as the source file before HTML-safe escaping. The inline script JSON bytes and SHA-256 are shown separately (225,391 bytes, `7a277793dcb37b1e2f388e01b155486ecd8ecf8550cd5320b2540ae62cc401c5`). The escaping itself is kept.
6. Schema note: states that `render_sql_template` (src/openalex_spike/cli.py lines 267 to 271) applies `.replace('openalex_spike', database)` with `database` set to openalex_benchmark. The archived SQL text is unchanged.
7. HTML title and publish label: "OpenAlex query benchmark".

Measured data and exact SQL are unchanged: the embedded payload is the same JSON.

## Checks actually run (local, no browser)
- The built file's embedded JSON parses equal to technical-payload.json, and the inline JSON SHA-256 matches the displayed value.
- The charset and viewport metas are first. No createRange, getSelection or addRange remain. No em or en dashes.
- `node --check` passes. A stub-DOM render of all 33 cases, 6 arm views and 8 dataflow nodes contains the exact SQL and no NaN or undefined values.

## Not checked by me
- The 390px overflow fix has not been verified in a real viewport. Do not treat it as fixed until Playwright confirms it.
- No visual, accessibility or in-browser copy-button check was done.

## Version 5 (1794174385-00c6): mobile-final-correction.txt
- Added `<!doctype html>` at the top of the file. It gives standards mode when the file is opened standalone. The artifact host wraps the page in its own doctype, so this one is ignored there.
- Added `#qtable { overflow: visible; }` and `.tw { contain: inline-size layout paint; }`. `.tw` is still the local horizontal scroller for each table.
- Added `.tw :focus-visible { outline-offset: -2px; }` so that paint containment doesn't clip focus rings inside the scrollers.
- A line diff against version 4 shows only these 4 added lines. The payload, numbers, SQL, clipboard logic and hash metadata are unchanged.
- Checks: line diff, `node --check`, and the stub-DOM render of all cases. I have not checked responsiveness, the 390px overflow or focus visibility in a browser.
