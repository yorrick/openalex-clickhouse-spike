import json

import pytest

from openalex_spike.clickhouse import ClickHouseService


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
