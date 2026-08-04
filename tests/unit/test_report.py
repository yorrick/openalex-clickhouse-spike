import json

from openalex_spike.report import render_report


def test_report_keeps_engine_and_capacity_verdicts_separate(tmp_path):
    evidence = {
        "run_id": "stage1-test",
        "inputs": {"manifest_sha256": "abc"},
        "environment": {"container_architecture": "aarch64"},
        "correctness": {"normalized_sha256": "def"},
        "sequential": [],
        "concurrent": {},
        "storage": {"observed_peak_bytes": 100},
        "local_engine_verdict": "pass",
        "capacity_verdict": "uncertain",
        "limitations": ["Stage 1 is validation evidence, not a full-size prediction."],
    }
    report_json, report_md = render_report(tmp_path, evidence)
    assert json.loads(report_json.read_text())["capacity_verdict"] == "uncertain"
    text = report_md.read_text()
    assert "Local engine verdict: pass" in text
    assert "Capacity verdict: uncertain" in text
    assert "not a full-size prediction" in text
