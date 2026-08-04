from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class QueryEnvelope:
    container_gb: int
    max_memory_usage_gib: int
    spill_gib: int


@dataclass(frozen=True)
class VerdictThresholds:
    minimum_samples: int
    maximum_seconds: int
    pass_routine_p95_seconds: int
    pass_join_p95_seconds: int
    conditional_routine_p95_seconds: int
    conditional_join_p95_seconds: int


@dataclass(frozen=True)
class ExperimentConfig:
    seed: str
    works_manifest_url: str
    combined_manifest_url: str
    tiers: dict[str, int]
    cpus: int
    memory_gb: tuple[int, ...]
    envelopes: dict[int, QueryEnvelope]
    thresholds: VerdictThresholds

    @classmethod
    def load(cls, path: Path) -> "ExperimentConfig":
        raw = tomllib.loads(path.read_text())
        tiers = {name: int(value) for name, value in raw["tiers"].items()}
        expected_names = {
            "stage1",
            "stage2_small",
            "stage2_medium",
            "stage2_large",
        }
        if set(tiers) != expected_names:
            raise ValueError(f"tier names must be {sorted(expected_names)}")
        if list(tiers.values()) != sorted(tiers.values()):
            raise ValueError("tier byte targets must be increasing")
        envelopes = {
            int(name.removeprefix("memory")): QueryEnvelope(**values)
            for name, values in raw["envelopes"].items()
        }
        return cls(
            seed=raw["seed"],
            works_manifest_url=raw["works_manifest_url"],
            combined_manifest_url=raw["combined_manifest_url"],
            tiers=tiers,
            cpus=int(raw["resources"]["cpus"]),
            memory_gb=tuple(int(v) for v in raw["resources"]["memory_gb"]),
            envelopes=envelopes,
            thresholds=VerdictThresholds(**raw["thresholds"]),
        )
