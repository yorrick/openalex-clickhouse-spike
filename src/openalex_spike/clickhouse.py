from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import os
import platform
import re
import subprocess


IMAGE = "clickhouse/clickhouse-server:26.3.12.3"
ARM_ARCHITECTURES = {"aarch64", "arm64"}


def _normalized_architecture(value: str) -> str:
    value = value.strip().lower()
    if value == "aarch64":
        return "arm64"
    return value


class ClickHouseService:
    def __init__(self, project_dir: Path | None = None) -> None:
        self.project_dir = project_dir or Path(__file__).resolve().parents[2]
        self._environment: dict[str, Any] | None = None

    def _run(
        self,
        command: list[str],
        *,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> str:
        completed = subprocess.run(
            command,
            cwd=self.project_dir,
            env=env,
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip()
            raise RuntimeError(f"command failed ({completed.returncode}): {detail}")
        return completed.stdout.strip()

    def _compose(self, arguments: list[str], **kwargs: Any) -> str:
        return self._run(["docker", "compose", *arguments], **kwargs)

    def up(self, memory_gb: int, cpus: int) -> None:
        raw_dir = self.project_dir / ".data" / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        environment = os.environ.copy()
        environment["CLICKHOUSE_MEMORY_GB"] = str(memory_gb)
        environment["CLICKHOUSE_CPUS"] = str(cpus)
        self._compose(
            ["up", "-d", "--wait", "--wait-timeout", "40"], env=environment
        )
        self._environment = self.environment_evidence()
        architectures = {
            _normalized_architecture(self._environment["host_architecture"]),
            _normalized_architecture(self._environment["docker_server_architecture"]),
            _normalized_architecture(self._environment["image_architecture"]),
            _normalized_architecture(self._environment["container_architecture"]),
        }
        if architectures != {"arm64"}:
            raise RuntimeError(f"native ARM64 architecture gate failed: {architectures}")
        if self.emulation_detected():
            raise RuntimeError("QEMU/Rosetta emulation signal detected")
        expected_hosts = {"8123": "127.0.0.1", "9000": "127.0.0.1"}
        if self.published_hosts() != expected_hosts:
            raise RuntimeError("ClickHouse ports are not loopback-only")

    def down(self) -> None:
        self._compose(["down"])

    def container_id(self) -> str:
        container_id = self._compose(["ps", "-q", "clickhouse"])
        if not container_id:
            raise RuntimeError("ClickHouse container is not running")
        return container_id

    def docker_server_architecture(self) -> str:
        return self._run(["docker", "info", "--format", "{{.Architecture}}"])

    def container_architecture(self) -> str:
        return self._compose(["exec", "-T", "clickhouse", "uname", "-m"])

    def image_evidence(self) -> dict[str, Any]:
        raw = self._run(
            [
                "docker",
                "image",
                "inspect",
                IMAGE,
                "--format",
                "{{json .RepoDigests}}|{{.Architecture}}|{{.Id}}",
            ]
        )
        repo_digests, architecture, image_id = raw.split("|", 2)
        return {
            "image": IMAGE,
            "repo_digests": json.loads(repo_digests),
            "image_architecture": architecture,
            "image_id": image_id,
        }

    def _container_text(self, arguments: list[str]) -> str:
        return self._compose(["exec", "-T", "clickhouse", *arguments])

    def environment_evidence(self) -> dict[str, Any]:
        image = self.image_evidence()
        container_id = self.container_id()
        inspect_raw = self._run(["docker", "inspect", container_id])
        inspect = json.loads(inspect_raw)[0]
        cpuinfo = self._container_text(["cat", "/proc/cpuinfo"])
        binfmt = self._container_text(
            [
                "sh",
                "-c",
                "if [ -d /proc/sys/fs/binfmt_misc ]; then "
                "for f in /proc/sys/fs/binfmt_misc/*; do "
                "if [ -f \"$f\" ]; then echo ===$f; cat \"$f\" || exit 1; fi; "
                "done; fi; exit 0",
            ]
        )
        return {
            "host_architecture": platform.machine(),
            "docker_server_architecture": self.docker_server_architecture(),
            **image,
            "container_architecture": self.container_architecture(),
            "container_cpuinfo": cpuinfo,
            "binfmt_registrations": binfmt,
            "published_hosts": self.published_hosts(inspect=inspect),
            "raw_mount_read_only": self.raw_mount_read_only(inspect=inspect),
            "resource_limits": {
                "memory_bytes": inspect["HostConfig"]["Memory"],
                "nano_cpus": inspect["HostConfig"]["NanoCpus"],
            },
        }

    def write_environment_evidence(self, destination: Path) -> dict[str, Any]:
        evidence = self._environment or self.environment_evidence()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
        return evidence

    def emulation_detected(self) -> bool:
        evidence = self._environment or self.environment_evidence()
        signals = "\n".join(
            [
                str(evidence["container_cpuinfo"]),
                str(evidence["binfmt_registrations"]),
            ]
        ).lower()
        architecture_mismatch = len(
            {
                _normalized_architecture(evidence["docker_server_architecture"]),
                _normalized_architecture(evidence["image_architecture"]),
                _normalized_architecture(evidence["container_architecture"]),
            }
        ) != 1
        return architecture_mismatch or "qemu" in signals or "rosetta" in signals

    def raw_mount_read_only(self, *, inspect: dict[str, Any] | None = None) -> bool:
        if inspect is None:
            inspect = json.loads(
                self._run(["docker", "inspect", self.container_id()])
            )[0]
        raw_mounts = [
            mount for mount in inspect["Mounts"] if mount["Destination"] == "/raw"
        ]
        return (
            len(raw_mounts) == 1
            and raw_mounts[0]["Type"] == "bind"
            and raw_mounts[0]["RW"] is False
        )

    def published_hosts(self, *, inspect: dict[str, Any] | None = None) -> dict[str, str]:
        if inspect is None:
            inspect = json.loads(
                self._run(["docker", "inspect", self.container_id()])
            )[0]
        result = {}
        for container_port, bindings in inspect["NetworkSettings"]["Ports"].items():
            if not bindings:
                raise RuntimeError(f"unexpected port bindings for {container_port}")
            host_ips = {binding["HostIp"] for binding in bindings}
            if not host_ips <= {"127.0.0.1", "::1"}:
                raise RuntimeError(f"non-loopback binding for {container_port}: {host_ips}")
            result[container_port.split("/", 1)[0]] = (
                "127.0.0.1" if "127.0.0.1" in host_ips else "::1"
            )
        return result

    def execute_script(self, sql: str) -> str:
        return self._compose(
            ["exec", "-T", "clickhouse", "clickhouse-client", "--multiquery"],
            input_text=sql,
        )

    def query_value(self, sql: str) -> str:
        if not re.match(r"^\s*SELECT\b", sql, flags=re.IGNORECASE):
            raise ValueError("query_value accepts SELECT statements only")
        return self._compose(
            [
                "exec",
                "-T",
                "clickhouse",
                "clickhouse-client",
                "--format",
                "TabSeparatedRaw",
                "--query",
                sql,
            ]
        )

    def query_json(self, sql: str) -> list[dict[str, object]]:
        if not re.match(r"^\s*(SELECT|WITH)\b", sql, flags=re.IGNORECASE):
            raise ValueError("query_json accepts SELECT/WITH statements only")
        output = self._compose(
            [
                "exec",
                "-T",
                "clickhouse",
                "clickhouse-client",
                "--format",
                "JSONEachRow",
                "--query",
                sql,
            ]
        )
        return [json.loads(line) for line in output.splitlines() if line]

    def execute_benchmark_query(
        self,
        sql: str,
        *,
        parameters: dict[str, int],
        settings: dict[str, int | str],
        query_id: str,
    ) -> dict[str, object]:
        if not re.fullmatch(r"[0-9a-f-]{36}", query_id):
            raise ValueError(f"invalid benchmark query ID: {query_id}")
        command = [
            "exec",
            "-T",
            "clickhouse",
            "clickhouse-client",
            f"--query_id={query_id}",
            "--format=Null",
        ]
        for name, value in sorted(settings.items()):
            if not re.fullmatch(r"[a-z_]+", name):
                raise ValueError(f"invalid ClickHouse setting name: {name}")
            command.append(f"--{name}={value}")
        for name, value in sorted(parameters.items()):
            if not re.fullmatch(r"[a-z_]+", name):
                raise ValueError(f"invalid ClickHouse parameter name: {name}")
            command.append(f"--param_{name}={value}")
        self._compose(command, input_text=sql)
        self.execute_script("SYSTEM FLUSH LOGS")
        telemetry = self.query_json(
            "SELECT "
            "query_duration_ms / 1000.0 AS elapsed_seconds, read_rows, read_bytes, "
            "result_rows, memory_usage AS peak_memory_bytes, "
            "ProfileEvents['ExternalAggregationWriteBytes'] + "
            "ProfileEvents['ExternalSortWriteBytes'] AS spill_bytes "
            "FROM system.query_log "
            f"WHERE query_id = '{query_id}' AND type = 'QueryFinish' "
            "ORDER BY event_time_microseconds DESC LIMIT 1"
        )
        if len(telemetry) != 1:
            raise RuntimeError(f"missing query_log telemetry for {query_id}")
        return telemetry[0]
