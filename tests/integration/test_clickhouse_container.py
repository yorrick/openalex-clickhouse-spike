import json
from base64 import b64encode
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from openalex_spike.clickhouse import (
    CLICKHOUSE_PASSWORD,
    CLICKHOUSE_USER,
    ClickHouseService,
)


@pytest.mark.integration
def test_compose_has_bounded_native_protocol_readiness_gate():
    service = ClickHouseService()
    config = json.loads(service._compose(["config", "--format", "json"]))
    healthcheck = config["services"]["clickhouse"]["healthcheck"]
    assert healthcheck["test"] == [
        "CMD",
        "clickhouse-client",
        "--host",
        "127.0.0.1",
        "--user",
        "openalex",
        "--password",
        "openalex-local-only",
        "--query",
        "SELECT 1",
    ]
    assert healthcheck["start_period"] == "2s"
    assert healthcheck["interval"] == "1s"
    assert healthcheck["timeout"] == "1s"
    assert healthcheck["retries"] == 45


@pytest.mark.integration
def test_clickhouse_is_native_arm64_and_loopback_only():
    service = ClickHouseService()
    service.up(memory_gb=32, cpus=16)
    try:
        assert service.container_architecture() in {"aarch64", "arm64"}
        assert service.docker_server_architecture() in {"aarch64", "arm64"}
        assert service.emulation_detected() is False
        assert service.raw_mount_read_only() is True
        assert service.query_value("SELECT version()").startswith("26.3.12.3")
        assert service.published_hosts() == {
            "8123": "127.0.0.1",
            "9000": "127.0.0.1",
        }
    finally:
        service.down()


@pytest.mark.integration
def test_clickhouse_http_is_queryable_from_the_host():
    service = ClickHouseService()
    service.up(memory_gb=32, cpus=16)
    try:
        request = Request(
            "http://127.0.0.1:8123/",
            data=b"SELECT 1 FORMAT TabSeparatedRaw",
            headers={
                "Authorization": "Basic "
                + b64encode(
                    f"{CLICKHOUSE_USER}:{CLICKHOUSE_PASSWORD}".encode()
                ).decode()
            },
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            assert response.status == 200
            assert response.read() == b"1\n"
    finally:
        service.down()


@pytest.mark.integration
def test_clickhouse_http_rejects_unauthenticated_host_queries():
    service = ClickHouseService()
    service.up(memory_gb=32, cpus=16)
    try:
        request = Request(
            "http://127.0.0.1:8123/",
            data=b"SELECT 1 FORMAT TabSeparatedRaw",
            method="POST",
        )
        with pytest.raises(HTTPError) as error:
            urlopen(request, timeout=5)
        assert error.value.code in {401, 403}
    finally:
        service.down()
