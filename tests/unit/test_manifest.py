import json

import httpx
import pytest

from openalex_spike.manifest import EntityManifest, pin_url, reconcile_entities


def test_entity_manifest_preserves_file_metadata(fixture_dir):
    manifest = EntityManifest.from_path(fixture_dir / "works-manifest.json")
    assert manifest.entity == "works"
    assert manifest.files[0].updated_date == "2022-01-01"
    assert manifest.files[0].record_count == 1


def test_combined_entities_reconcile_to_total(fixture_dir):
    total = reconcile_entities(fixture_dir / "combined-manifest.json")
    assert total == 783_555_949_110


def test_pin_url_records_transport_and_content_identity(tmp_path):
    content = b'{"date":"2026-06-26"}'

    def handler(request):
        return httpx.Response(
            200,
            content=content,
            headers={
                "ETag": '"fixture-etag"',
                "Last-Modified": "Fri, 26 Jun 2026 00:00:00 GMT",
                "Content-Length": str(len(content)),
            },
            request=request,
        )

    destination = tmp_path / "manifest.json"
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        metadata = pin_url(client, "https://example.test/manifest.json", destination)

    assert destination.read_bytes() == content
    assert metadata["etag"] == '"fixture-etag"'
    assert json.loads((tmp_path / "manifest.json.metadata.json").read_text())[
        "sha256"
    ] == metadata["sha256"]


def test_pin_url_rejects_missing_etag(tmp_path):
    def handler(request):
        return httpx.Response(200, content=b"{}", request=request)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(ValueError, match="no ETag"):
            pin_url(client, "https://example.test/manifest.json", tmp_path / "x.json")
