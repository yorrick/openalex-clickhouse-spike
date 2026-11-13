#!/usr/bin/env python3
"""Assemble artifact.html from artifact-template.html and the immutable artifact-payload.json.

The payload text is inserted verbatim except that every '<' is written as the JSON escape \\u003c,
so no '</script' or '<!--' sequence can appear inside the inline JSON. After JSON parsing, every
value (including every SQL string) is identical to the payload file. The script checks that.
"""
from pathlib import Path
import hashlib, json, re, sys

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "artifact-template.html"
PAYLOAD = HERE / "artifact-payload.json"
INTEGRITY = HERE / "payload-integrity.json"
OUT = HERE / "artifact.html"


def fail(msg):
    print("BUILD FAILED: " + msg, file=sys.stderr)
    sys.exit(1)


def main():
    tpl = TEMPLATE.read_text(encoding="utf-8")
    raw = PAYLOAD.read_bytes()
    text = raw.decode("utf-8")
    payload_sha = hashlib.sha256(raw).hexdigest()
    integ = json.loads(INTEGRITY.read_text(encoding="utf-8"))
    if integ.get("payload_sha256") != payload_sha or integ.get("payload_bytes") != len(raw):
        fail("payload does not match payload-integrity.json (%s, %d bytes)" % (payload_sha, len(raw)))

    for ch, name in (("—", "em dash"), ("–", "en dash")):
        if ch in tpl:
            fail("template contains an %s" % name)
    # Standards mode and explicit UTF-8 before any content (a raw file opened locally must not
    # fall back to quirks mode or windows-1252). The template itself is kept ASCII-only.
    head = tpl[:400].lower()
    if not head.startswith("<!doctype html>") or '<meta charset="utf-8">' not in head or 'name="viewport"' not in head:
        fail("template must start with <!doctype html>, <meta charset=\"utf-8\"> and a viewport meta")
    if any(ord(c) > 127 for c in tpl):
        fail("template must be ASCII-only (use HTML entities or JS \\u escapes)")
    for ph in ("__PAYLOAD__", "__BUILD__"):
        if tpl.count(ph) != 1:
            fail("placeholder %s must occur exactly once" % ph)

    original = json.loads(text)
    embedded = text.rstrip("\n").replace("<", "\\u003c")
    if json.loads(embedded) != original:
        fail("escaped payload does not parse to the same value")

    build = {
        "payload_file": PAYLOAD.name,
        "payload_sha256": payload_sha,
        "payload_bytes": len(raw),
        "records": len(original["records"]),
        "exact_sql_records": sum(1 for r in original["records"] if r.get("sql")),
        "sql_status_counts": {k: sum(1 for r in original["records"] if r.get("sql_status") == k) for k in ("exact_executed", "not_executed", "not_recorded")},
        "template_sha256": hashlib.sha256(tpl.encode("utf-8")).hexdigest(),
    }
    build_json = json.dumps(build, separators=(",", ":")).replace("<", "\\u003c")
    html = tpl.replace("__PAYLOAD__", embedded).replace("__BUILD__", build_json)
    OUT.write_text(html, encoding="utf-8")

    # Re-read the output and verify the inline payload round-trips.
    out = OUT.read_text(encoding="utf-8")
    m = re.search(r'<script type="application/json" id="payload">(.*?)</script>', out, re.S)
    if not m:
        fail("payload script element not found in output")
    seg = m.group(1)
    if "<" in seg:
        fail("unescaped '<' inside inline payload")
    parsed = json.loads(seg)
    if parsed != original:
        fail("inline payload differs from payload file")
    for a, b in zip(parsed["records"], original["records"]):
        if a.get("sql") != b.get("sql"):
            fail("SQL mismatch for " + str(b.get("profile_id")))
        if b.get("sql") and hashlib.sha256(a["sql"].encode("utf-8")).hexdigest() != b["sql_sha256"]:
            fail("SQL SHA-256 mismatch for " + str(b.get("profile_id")))
    if "—" in out.replace(seg, ""):
        fail("em dash in page copy")
    print(json.dumps(dict(build, output=OUT.name, output_bytes=len(out.encode("utf-8"))), indent=2))


if __name__ == "__main__":
    main()
