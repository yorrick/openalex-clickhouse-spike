import pytest

from openalex_spike.clickhouse import ClickHouseService


def _inspect(host_ips):
    return {
        "NetworkSettings": {
            "Ports": {
                "8123/tcp": [{"HostIp": host_ip} for host_ip in host_ips],
                "9000/tcp": [{"HostIp": host_ip} for host_ip in host_ips],
            }
        }
    }


def test_published_hosts_accepts_ipv4_and_ipv6_loopback_bindings():
    service = ClickHouseService()
    assert service.published_hosts(inspect=_inspect(["127.0.0.1", "::1"])) == {
        "8123": "127.0.0.1",
        "9000": "127.0.0.1",
    }


def test_published_hosts_rejects_any_public_binding():
    service = ClickHouseService()
    with pytest.raises(RuntimeError, match="non-loopback"):
        service.published_hosts(inspect=_inspect(["127.0.0.1", "0.0.0.0"]))
