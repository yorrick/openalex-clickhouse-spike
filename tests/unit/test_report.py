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


def test_report_provenance_mode_changes_only_json_and_is_byte_stable(tmp_path):
    base_evidence = {
        "run_id": "stage2-test",
        "inputs": {"selection_sha256": "abc"},
        "environment": {"container_architecture": "aarch64"},
        "correctness": {"stage2_medium": {"normalized_sha256": "def"}},
        "sequential": {"stage2_medium": []},
        "concurrent": {"stage2_medium": {"classes": {}}},
        "storage": {"observed_peak_bytes": 100},
        "local_engine_verdict": "pass",
        "capacity_verdict": "uncertain",
        "limitations": ["test limitation"],
    }
    source = "SHA-256-pinned completed tier summaries"
    in_run = {
        **base_evidence,
        "verdict_evaluation": {"mode": "in_run", "source": source},
    }
    postprocessed = {
        **base_evidence,
        "verdict_evaluation": {
            "mode": "postprocessed_from_sha256_pinned_tier_artifacts",
            "source": source,
        },
    }

    in_run_json, in_run_md = render_report(tmp_path / "in-run", in_run)
    post_json, post_md = render_report(tmp_path / "postprocessed", postprocessed)

    assert in_run_md.read_bytes() == post_md.read_bytes()
    in_run_payload = json.loads(in_run_json.read_text())
    post_payload = json.loads(post_json.read_text())
    assert in_run_payload.pop("verdict_evaluation") == in_run["verdict_evaluation"]
    assert post_payload.pop("verdict_evaluation") == postprocessed[
        "verdict_evaluation"
    ]
    assert in_run_payload == post_payload

    first_json = post_json.read_bytes()
    first_md = post_md.read_bytes()
    render_report(tmp_path / "postprocessed", postprocessed)
    assert post_json.read_bytes() == first_json
    assert post_md.read_bytes() == first_md
