from io import BytesIO
from urllib.error import HTTPError

import pytest

import openalex_spike.clickhouse as clickhouse_module
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


def test_up_uses_bounded_compose_wait(tmp_path, monkeypatch):
    service = ClickHouseService(tmp_path)
    compose_calls = []
    evidence = {
        "host_architecture": "arm64",
        "docker_server_architecture": "arm64",
        "image_architecture": "arm64",
        "container_architecture": "arm64",
        "container_cpuinfo": "Apple",
        "binfmt_registrations": "",
    }

    monkeypatch.setattr(
        service,
        "_compose",
        lambda arguments, **kwargs: compose_calls.append((arguments, kwargs)) or "",
    )
    monkeypatch.setattr(service, "environment_evidence", lambda: evidence)
    monkeypatch.setattr(service, "emulation_detected", lambda: False)
    monkeypatch.setattr(
        service,
        "published_hosts",
        lambda: {"8123": "127.0.0.1", "9000": "127.0.0.1"},
    )
    monkeypatch.setattr(service, "query_http_value", lambda sql: "1")

    service.up(memory_gb=32, cpus=16)

    arguments, kwargs = compose_calls[0]
    assert arguments == ["up", "-d", "--wait", "--wait-timeout", "40"]
    assert kwargs["env"]["CLICKHOUSE_MEMORY_GB"] == "32"
    assert kwargs["env"]["CLICKHOUSE_CPUS"] == "16"


def test_query_http_value_rejects_non_select_statements():
    service = ClickHouseService()
    with pytest.raises(ValueError, match="SELECT"):
        service.query_http_value("DROP DATABASE openalex_spike")


def test_query_http_value_wraps_http_errors(monkeypatch):
    service = ClickHouseService()

    def raise_http_error(*args, **kwargs):
        raise HTTPError(
            "http://127.0.0.1:8123/",
            401,
            "Unauthorized",
            {},
            BytesIO(b"authentication failed"),
        )

    monkeypatch.setattr(clickhouse_module, "urlopen", raise_http_error)

    with pytest.raises(RuntimeError, match="status 401: authentication failed"):
        service.query_http_value("SELECT 1")
