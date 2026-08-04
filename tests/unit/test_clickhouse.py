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

    service.up(memory_gb=32, cpus=16)

    arguments, kwargs = compose_calls[0]
    assert arguments == ["up", "-d", "--wait", "--wait-timeout", "40"]
    assert kwargs["env"]["CLICKHOUSE_MEMORY_GB"] == "32"
    assert kwargs["env"]["CLICKHOUSE_CPUS"] == "16"
