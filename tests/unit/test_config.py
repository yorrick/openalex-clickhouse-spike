from pathlib import Path

from openalex_spike.config import ExperimentConfig


def test_loads_fixed_tiers_and_resource_envelopes(tmp_path: Path) -> None:
    path = tmp_path / "experiment.toml"
    path.write_text(
        """
seed = "openalex-clickhouse-v1"
works_manifest_url = "https://openalex.s3.amazonaws.com/data/parquet/works/manifest.json"
combined_manifest_url = "https://openalex.s3.amazonaws.com/data/parquet/manifest.json"
[tiers]
stage1 = 1073741824
stage2_small = 3000000000
stage2_medium = 15000000000
stage2_large = 45000000000
[resources]
cpus = 16
memory_gb = [32, 50]
[envelopes.memory32]
container_gb = 32
max_memory_usage_gib = 7
spill_gib = 2
[envelopes.memory50]
container_gb = 50
max_memory_usage_gib = 12
spill_gib = 4
[thresholds]
minimum_ordinary_author_reference_coverage = 0.999
minimum_samples = 50
maximum_seconds = 3600
pass_routine_p95_seconds = 15
pass_join_p95_seconds = 45
conditional_routine_p95_seconds = 30
conditional_join_p95_seconds = 120
"""
    )
    cfg = ExperimentConfig.load(path)
    assert cfg.seed == "openalex-clickhouse-v1"
    assert cfg.tiers["stage2_large"] == 45_000_000_000
    assert cfg.memory_gb == (32, 50)
    assert cfg.envelopes[32].max_memory_usage_gib == 7
    assert cfg.thresholds.minimum_samples == 50
    assert cfg.thresholds.minimum_ordinary_author_reference_coverage == 0.999
