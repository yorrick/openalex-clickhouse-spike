import pytest

from openalex_spike.clickhouse import ClickHouseService


@pytest.mark.integration
def test_clickhouse_is_native_arm64_and_loopback_only():
    service = ClickHouseService()
    service.up(memory_gb=32, cpus=16)
    try:
        assert service.container_architecture() in {"aarch64", "arm64"}
        assert service.docker_server_architecture() in {"aarch64", "arm64"}
        assert service.emulation_detected() is False
        assert service.query_value("SELECT version()").startswith("26.3.12.3")
        assert service.published_hosts() == {
            "8123": "127.0.0.1",
            "9000": "127.0.0.1",
        }
    finally:
        service.down()
