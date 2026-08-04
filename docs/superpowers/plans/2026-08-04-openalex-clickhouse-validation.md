# OpenAlex ClickHouse Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and run a reproducible two-stage experiment that proves OpenAlex Parquet can be transformed into a useful ClickHouse bibliometrics model and measures sample-scale behaviour under an Alliance-like resource envelope.

**Architecture:** A Python CLI pins OpenAlex manifests, deterministically selects nested Works samples, downloads and verifies Parquet, and orchestrates a loopback-only ClickHouse Docker container. Versioned SQL builds native dimensions, bridges, and citation edges; a benchmark harness records correctness, sequential, concurrent, and storage evidence without claiming that local sample latency predicts full-scale Alliance performance.

**Tech Stack:** Python 3.12, `uv`, pytest, httpx, PyArrow, clickhouse-connect, Docker Compose, ClickHouse 26.3.12.3 LTS, SQL, TOML, JSON.

---

## File map

- `pyproject.toml`: Python package, console script, and dependencies.
- `.gitignore`: excludes raw data, ClickHouse state, secrets, and unfiltered logs.
- `compose.yaml`: pinned, loopback-only ClickHouse service with configurable CPU/RAM limits.
- `clickhouse/config.d/benchmark.xml`: query-log and filesystem-cache configuration.
- `config/experiment.toml`: pinned URLs, byte targets, seed, resource envelopes, and thresholds.
- `src/openalex_spike/config.py`: typed configuration loader.
- `src/openalex_spike/manifest.py`: fetches, validates, and pins manifests and HTTP metadata.
- `src/openalex_spike/sampling.py`: deterministic four-stratum nested file selection.
- `src/openalex_spike/download.py`: anonymous S3 downloads, byte/footer checks, and hard-linked tier views.
- `src/openalex_spike/clickhouse.py`: Docker lifecycle, native-platform gate, SQL execution, and query telemetry.
- `src/openalex_spike/correctness.py`: invariant queries and blocking Stage 1 verdict.
- `src/openalex_spike/benchmark.py`: sequential and multi-scale benchmark runner.
- `src/openalex_spike/concurrency.py`: deterministic three-client load generator.
- `src/openalex_spike/storage.py`: per-table low/expected/high capacity model.
- `src/openalex_spike/report.py`: JSON evidence export and Markdown verdict.
- `src/openalex_spike/cli.py`: explicit pipeline commands; no automatic fallback path.
- `sql/00_schema.sql`: explicit native table schemas and ID parser.
- `sql/10_load_dimensions.sql`: complete small dimensions and Stage 2 Authors.
- `sql/20_load_works.sql`: Works and bridge/edge materialization.
- `sql/30_reverse_projection.sql`: measured incoming-citation projection variant.
- `sql/queries/q01_works_by_year.sql` through `q07_citations_by_year.sql`: fixed workload.
- `tests/fixtures/`: small manifests and generated nested Parquet fixtures.
- `tests/conftest.py`: shared fixture-directory, manifest, and selected-file fixtures.
- `tests/unit/`: deterministic, network-free unit tests.
- `tests/integration/`: Docker/ClickHouse and generated-Parquet integration tests.
- `README.md`: exact Stage 1 and Stage 2 operator commands and interpretation limits.

## Task 1: Bootstrap the package and typed experiment configuration

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `config/experiment.toml`
- Create: `src/openalex_spike/__init__.py`
- Create: `src/openalex_spike/config.py`
- Test: `tests/unit/test_config.py`

- [ ] **Step 1: Write the failing configuration test**

```python
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
```

- [ ] **Step 2: Run the test and verify the package is absent**

Run: `uv run pytest tests/unit/test_config.py -q`  
Expected: FAIL with `ModuleNotFoundError: No module named 'openalex_spike'`.

- [ ] **Step 3: Add package metadata and dependencies**

```toml
[project]
name = "openalex-clickhouse-spike"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
  "clickhouse-connect==0.8.18",
  "httpx==0.28.1",
  "pyarrow==21.0.0",
]

[project.optional-dependencies]
dev = ["pytest==8.4.1"]

[project.scripts]
openalex-spike = "openalex_spike.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = ["integration: requires a running Docker daemon"]
```

- [ ] **Step 4: Implement the immutable configuration loader**

```python
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
        expected_names = {"stage1", "stage2_small", "stage2_medium", "stage2_large"}
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
```

- [ ] **Step 5: Add the real configuration and data exclusions**

Use the URLs and byte targets in the test, `cpus = 16`, and `memory_gb = [32, 50]`. Add:

```gitignore
.data/
.env
results/raw-logs/
__pycache__/
.pytest_cache/
.venv/
*.pyc
```

- [ ] **Step 6: Run the test and commit**

Run: `uv lock && uv sync --extra dev && uv run pytest tests/unit/test_config.py -q`  
Expected: `1 passed`.

```bash
git add pyproject.toml uv.lock .gitignore config src tests
git commit -m "chore: bootstrap OpenAlex spike configuration"
```

## Task 2: Pin and reconcile OpenAlex manifests

**Files:**
- Create: `src/openalex_spike/manifest.py`
- Create: `tests/fixtures/works-manifest.json`
- Create: `tests/fixtures/combined-manifest.json`
- Create: `tests/conftest.py`
- Test: `tests/unit/test_manifest.py`

- [ ] **Step 1: Write tests for manifest parsing and exact reconciliation**

```python
from openalex_spike.manifest import EntityManifest, reconcile_entities


def test_entity_manifest_preserves_file_metadata(fixture_dir):
    manifest = EntityManifest.from_path(fixture_dir / "works-manifest.json")
    assert manifest.entity == "works"
    assert manifest.files[0].updated_date == "2022-07-31"
    assert manifest.files[0].record_count == 1


def test_combined_entities_reconcile_to_total(fixture_dir):
    total = reconcile_entities(fixture_dir / "combined-manifest.json")
    assert total == 783_555_949_110
```

`tests/conftest.py` defines `fixture_dir`, parses `works_manifest`, and provides
a `selected_file` whose URL, byte length, record count, date, stratum, and rank
are fixed. Keep all unit tests network-free.

- [ ] **Step 2: Run the tests and verify failure**

Run: `uv run pytest tests/unit/test_manifest.py -q`  
Expected: FAIL because `openalex_spike.manifest` does not exist.

- [ ] **Step 3: Implement strict manifest models**

```python
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
import json


@dataclass(frozen=True)
class ManifestFile:
    url: str
    content_length: int
    record_count: int

    @property
    def updated_date(self) -> str:
        marker = "updated_date="
        if marker not in self.url:
            raise ValueError(f"missing updated_date in {self.url}")
        return self.url.split(marker, 1)[1].split("/", 1)[0]


@dataclass(frozen=True)
class EntityManifest:
    date: str
    entity: str
    content_length: int
    record_count: int
    files: tuple[ManifestFile, ...]

    @classmethod
    def from_path(cls, path: Path) -> "EntityManifest":
        raw = json.loads(path.read_text())
        files = tuple(
            ManifestFile(
                url=item["url"],
                content_length=int(item["meta"]["content_length"]),
                record_count=int(item["meta"]["record_count"]),
            )
            for item in raw["files"]
        )
        if sum(f.content_length for f in files) != int(raw["content_length"]):
            raise ValueError("entity file bytes do not reconcile")
        if sum(f.record_count for f in files) != int(raw["record_count"]):
            raise ValueError("entity record counts do not reconcile")
        return cls(raw["date"], raw["entity"], int(raw["content_length"]), int(raw["record_count"]), files)


def reconcile_entities(path: Path) -> int:
    raw = json.loads(path.read_text())
    actual = sum(int(entity["content_length"]) for entity in raw["entities"])
    expected = int(raw["meta"]["content_length"])
    if actual != expected:
        raise ValueError(f"combined manifest mismatch: {actual} != {expected}")
    return actual
```

- [ ] **Step 4: Add HTTP pinning with ETag and atomic rename**

Implement `pin_url(client, url, destination)` to GET into `destination.with_suffix('.tmp')`, write an adjacent metadata JSON containing URL, UTC retrieval time, `ETag`, `Last-Modified`, `Content-Length`, and SHA-256 of the downloaded manifest, then rename both into place. A missing ETag is an error; do not silently pin without it.

Pin the combined manifest plus per-entity manifests for Works, Authors, and
every explicitly selected small entity from design section 2. Assert that the
pinned per-entity totals reconcile to the matching entries in the pinned
combined manifest before selection or download.

- [ ] **Step 5: Run tests and commit**

Run: `uv run pytest tests/unit/test_manifest.py -q`  
Expected: all manifest tests PASS.

```bash
git add src/openalex_spike/manifest.py tests/fixtures tests/unit/test_manifest.py
git commit -m "feat: pin and reconcile OpenAlex manifests"
```

## Task 3: Select deterministic nested Works tiers

**Files:**
- Create: `src/openalex_spike/sampling.py`
- Test: `tests/unit/test_sampling.py`

- [ ] **Step 1: Write the determinism, stratum, and nesting tests**

```python
def test_selection_is_deterministic_and_nested(works_manifest):
    targets = {"stage1": 1_000, "stage2_small": 3_000, "stage2_medium": 6_000, "stage2_large": 9_000}
    first = select_nested(works_manifest.files, targets, "fixed-seed")
    second = select_nested(works_manifest.files, targets, "fixed-seed")
    assert first == second
    assert set(first["stage1"]) <= set(first["stage2_small"])
    assert set(first["stage2_small"]) <= set(first["stage2_medium"])
    assert set(first["stage2_medium"]) <= set(first["stage2_large"])
    assert {entry.stratum for entry in first["stage1"]} == {0, 1, 2, 3}
```

- [ ] **Step 2: Run the test and verify failure**

Run: `uv run pytest tests/unit/test_sampling.py -q`  
Expected: FAIL because `select_nested` is missing.

- [ ] **Step 3: Implement four cumulative-byte strata and stable ranking**

Create a `SelectedFile` dataclass containing URL, bytes, records, updated date, stratum, and stable rank. Sort all files by `(updated_date, url)`, assign stratum from cumulative-byte fraction, then rank within each stratum using:

```python
def stable_rank(seed: str, url: str) -> str:
    return hashlib.sha256(f"{seed}\0{url}".encode()).hexdigest()
```

For Stage 1, first seed every stratum with its lowest-ranked file no larger than one quarter of the Stage 1 target; fail if a stratum has no eligible file. Then, for each increasing target, start with the preceding tier and add the lowest-ranked unused file from the stratum furthest below one quarter of the target until total bytes meet or exceed the target. The overshoot may not exceed the largest selected file. Record the cap, eligibility counts, seed files, and Stage 1 small-file bias. Verify the algorithm over 60 seeds.

- [ ] **Step 4: Serialize an auditable selection document**

Write `selection.json` with algorithm name `cumulative-bytes-four-strata-v2`, seed, manifest ETag/SHA-256, Stage 1 coverage policy, target bytes, actual bytes, record totals, and the ordered `SelectedFile` list per tier. Re-serialize from the same inputs in the test and assert byte equality. Reject stale selection documents whose algorithm does not match the running code.

- [ ] **Step 5: Run tests and commit**

Run: `uv run pytest tests/unit/test_sampling.py -q`  
Expected: all sampling tests PASS.

```bash
git add src/openalex_spike/sampling.py tests/unit/test_sampling.py
git commit -m "feat: select reproducible nested Works samples"
```

## Task 4: Download and verify Parquet without duplicating tiers

**Files:**
- Create: `src/openalex_spike/download.py`
- Test: `tests/unit/test_download.py`

- [ ] **Step 1: Write tests for S3 URL conversion, byte validation, and hard links**

```python
def test_public_s3_url_conversion():
    assert public_https("s3://openalex/data/parquet/works/x.parquet") == \
        "https://openalex.s3.amazonaws.com/data/parquet/works/x.parquet"


def test_materialized_tiers_share_inode(tmp_path, selected_file):
    object_path = tmp_path / "objects" / "abc.parquet"
    object_path.parent.mkdir()
    object_path.write_bytes(b"PAR1fixturePAR1")
    links = materialize_tier_links(tmp_path, {"small": [selected_file]}, {selected_file.url: object_path})
    assert links[0].stat().st_ino == object_path.stat().st_ino
```

- [ ] **Step 2: Implement bounded concurrent streaming downloads**

Use `httpx.Client(follow_redirects=True, timeout=120)` and at most four worker threads. Write each response to `*.partial`, count bytes while streaming, `fsync`, compare with manifest length, then atomically rename. On network or length failure retain neither a final object nor a tier link; return a nonzero CLI status. Retries use exactly three attempts with 2, 8, and 30 second delays. No alternate URL or download tool is tried automatically.

- [ ] **Step 3: Verify Parquet metadata and selected row totals**

Use `pyarrow.parquet.ParquetFile(path).metadata.num_rows`. Require a readable footer and require the file row count to equal the manifest record count. Sum verified rows and bytes per tier and store them in `download-verification.json`.

The per-file record-count equality deliberately tightens the design's aggregate
gate: OpenAlex publishes an exact count for every file, so any mismatch stops
the experiment and is reported rather than relaxed automatically.

- [ ] **Step 4: Materialize nested tier directories with hard links**

Store every unique object once beneath `.data/raw/objects/<sha256-url>.parquet`. Build `.data/raw/tiers/<tier>/<entity>/` using `os.link`. If source and target filesystems differ, stop with an explicit error; do not copy as a fallback without user approval.

Works use the nested tier selection. Authors use the complete pinned Authors
manifest only when `include_complete_authors=True`. The selected small entities
always use every file in their pinned entity manifests. Add unit tests proving
that complete Authors and small dimensions have entity-specific directories,
verified totals, and no accidental inclusion of Awards.

- [ ] **Step 5: Run tests and commit**

Run: `uv run pytest tests/unit/test_download.py -q`  
Expected: all download tests PASS.

```bash
git add src/openalex_spike/download.py tests/unit/test_download.py
git commit -m "feat: download and verify selected Parquet files"
```

## Task 5: Start a pinned, loopback-only native ClickHouse container

**Files:**
- Create: `compose.yaml`
- Create: `clickhouse/config.d/benchmark.xml`
- Create: `src/openalex_spike/clickhouse.py`
- Test: `tests/integration/test_clickhouse_container.py`

- [ ] **Step 1: Add the Docker integration test**

```python
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
        assert service.published_hosts() == {"8123": "127.0.0.1", "9000": "127.0.0.1"}
    finally:
        service.down()
```

- [ ] **Step 2: Create the Compose service**

```yaml
services:
  clickhouse:
    image: clickhouse/clickhouse-server:26.3.12.3
    cpus: "${CLICKHOUSE_CPUS:-16}"
    mem_limit: "${CLICKHOUSE_MEMORY_GB:-32}g"
    ports:
      - "127.0.0.1:8123:8123"
      - "127.0.0.1:9000:9000"
    volumes:
      - ./.data/clickhouse:/var/lib/clickhouse
      - ./.data/raw:/var/lib/clickhouse/user_files/raw:ro
      - ./clickhouse/config.d:/etc/clickhouse-server/config.d:ro
```

Use this exact `benchmark.xml`:

```xml
<clickhouse>
  <query_log replace="1">
    <database>system</database>
    <table>query_log</table>
    <flush_interval_milliseconds>1000</flush_interval_milliseconds>
  </query_log>
  <asynchronous_metric_log>
    <flush_interval_milliseconds>1000</flush_interval_milliseconds>
  </asynchronous_metric_log>
</clickhouse>
```

- [ ] **Step 3: Implement lifecycle and architecture gates**

`ClickHouseService.up()` sets the two environment variables and runs `docker compose up -d --wait --wait-timeout 40`. Compose defines a native-protocol `SELECT 1` healthcheck so `--wait` does not return merely because the entrypoint process is running. Do not force `platform`; let the multi-architecture image resolve for the Docker server. Record the Docker server architecture, resolved image digest/architecture, `uname -m` inside the container, `/proc/cpuinfo`, binfmt/QEMU registrations visible to the Docker VM, port bindings, and resource limits. On this ARM host, fail unless server, image, and container all resolve to ARM64 and no QEMU/Rosetta signal is present. `execute_script()` passes SQL to `clickhouse-client --multiquery` through stdin; it never shell-interpolates file paths.

- [ ] **Step 4: Start Docker Desktop, run the integration test, and commit**

Run: `uv run pytest -m integration tests/integration/test_clickhouse_container.py -q`  
Expected: `1 passed`; if Docker is unavailable, stop and report that prerequisite rather than changing runtimes.

```bash
git add compose.yaml clickhouse src/openalex_spike/clickhouse.py tests/integration
git commit -m "feat: add reproducible ClickHouse container"
```

## Task 6: Define explicit analytical schemas and transformations

**Files:**
- Create: `sql/00_schema.sql`
- Create: `sql/05_raw_evidence.sql`
- Create: `sql/10_load_dimensions.sql`
- Create: `sql/20_load_works.sql`
- Create: `sql/30_reverse_projection.sql`
- Test: `tests/integration/test_transform_sql.py`

- [ ] **Step 1: Generate a nested Parquet fixture and write failing integration assertions**

The fixture contains two Works, two authorships, two institutions, two topics, three raw references with one duplicate, one null reference array, `is_xpac` values, and matching dimension rows. Assert exact counts: two Works, two work-author rows, two work-institution rows, two work-topic rows, and two distinct citation edges.

- [ ] **Step 2: Add the ID parser and explicit MergeTree tables**

Start `00_schema.sql` with:

```sql
CREATE DATABASE IF NOT EXISTS openalex_spike;
CREATE OR REPLACE FUNCTION openalex_numeric_id AS id ->
    toUInt64OrNull(extract(id, '[A-Z]([0-9]+)$'));

CREATE TABLE openalex_spike.works
(
    work_id UInt64,
    canonical_id String,
    publication_year Nullable(UInt16),
    work_type LowCardinality(String),
    source_id Nullable(UInt64),
    is_oa Bool,
    is_xpac Bool,
    cited_by_count UInt32,
    primary_topic_id Nullable(UInt64)
) ENGINE = MergeTree ORDER BY (publication_year, work_id);

CREATE TABLE openalex_spike.work_author
(
    work_id UInt64,
    author_id UInt64,
    author_position LowCardinality(String),
    is_corresponding Bool
) ENGINE = MergeTree ORDER BY (author_id, work_id);

CREATE TABLE openalex_spike.work_institution
(
    work_id UInt64,
    author_id UInt64,
    institution_id UInt64
) ENGINE = MergeTree ORDER BY (institution_id, work_id, author_id);

CREATE TABLE openalex_spike.work_topic
(
    work_id UInt64,
    topic_id UInt64,
    score Float32,
    is_primary Bool
) ENGINE = MergeTree ORDER BY (topic_id, work_id);

CREATE TABLE openalex_spike.citation_edge
(
    citing_work_id UInt64,
    cited_work_id UInt64,
    citing_year Nullable(UInt16)
) ENGINE = MergeTree ORDER BY (citing_work_id, cited_work_id);

CREATE TABLE openalex_spike.authors
(
    author_id UInt64,
    canonical_id String,
    display_name String,
    orcid Nullable(String)
) ENGINE = MergeTree ORDER BY author_id;

CREATE TABLE openalex_spike.institutions
(
    institution_id UInt64,
    canonical_id String,
    display_name String,
    country_code Nullable(String),
    institution_type LowCardinality(String)
) ENGINE = MergeTree ORDER BY institution_id;

CREATE TABLE openalex_spike.sources
(
    source_id UInt64,
    canonical_id String,
    display_name String,
    issn_l Nullable(String),
    source_type LowCardinality(String)
) ENGINE = MergeTree ORDER BY source_id;

CREATE TABLE openalex_spike.topics
(
    topic_id UInt64,
    display_name String,
    subfield_id UInt64,
    field_id UInt64,
    domain_id UInt64
) ENGINE = MergeTree ORDER BY topic_id;
```

- [ ] **Step 3: Record raw evidence, then load Works and deduplicated edges**

Use a validated `{{WORKS_GLOB}}` replacement supplied by the Python runner.
Before any filtered insert, run this single-scan evidence query and persist its
row as JSON:

```sql
WITH raw_edges AS
(
    SELECT
        id,
        referenced_id,
        openalex_numeric_id(id) AS citing_id,
        openalex_numeric_id(referenced_id) AS cited_id,
        citing_id IS NOT NULL AND cited_id IS NOT NULL AS valid
    FROM file('{{WORKS_GLOB}}', Parquet)
    ARRAY JOIN referenced_works AS referenced_id
)
SELECT
    count() AS raw_reference_entries,
    countIf(NOT valid) AS rejected_id_entries,
    uniqExactIf(tuple(citing_id, cited_id), valid) AS distinct_valid_pairs,
    countIf(valid) - distinct_valid_pairs AS duplicate_pair_delta
FROM raw_edges
FORMAT JSONEachRow;

SELECT countIf(topic.score IS NULL) AS null_topic_scores
FROM file('{{WORKS_GLOB}}', Parquet)
ARRAY JOIN topics AS topic
FORMAT JSONEachRow;
```

The load SQL is:

```sql
INSERT INTO openalex_spike.works
SELECT
    openalex_numeric_id(id),
    id,
    toUInt16OrNull(publication_year),
    type,
    openalex_numeric_id(primary_location.source.id),
    coalesce(open_access.is_oa, false),
    coalesce(is_xpac, false),
    toUInt32(cited_by_count),
    openalex_numeric_id(primary_topic.id)
FROM file('{{WORKS_GLOB}}', Parquet)
WHERE openalex_numeric_id(id) IS NOT NULL;

INSERT INTO openalex_spike.citation_edge
SELECT citing_work_id, cited_work_id, min(citing_year)
FROM
(
    SELECT
        openalex_numeric_id(id) AS citing_work_id,
        openalex_numeric_id(referenced_id) AS cited_work_id,
        toUInt16OrNull(publication_year) AS citing_year
    FROM file('{{WORKS_GLOB}}', Parquet)
    ARRAY JOIN referenced_works AS referenced_id
)
WHERE citing_work_id IS NOT NULL AND cited_work_id IS NOT NULL
GROUP BY citing_work_id, cited_work_id;
```

Load the other Works-derived tables with these explicit shapes:

```sql
INSERT INTO openalex_spike.work_author
SELECT
    openalex_numeric_id(id),
    openalex_numeric_id(authorship.author.id),
    authorship.author_position,
    coalesce(authorship.is_corresponding, false)
FROM file('{{WORKS_GLOB}}', Parquet)
ARRAY JOIN authorships AS authorship
WHERE openalex_numeric_id(id) IS NOT NULL
  AND openalex_numeric_id(authorship.author.id) IS NOT NULL;

INSERT INTO openalex_spike.work_institution
SELECT DISTINCT
    openalex_numeric_id(id),
    openalex_numeric_id(authorship.author.id),
    openalex_numeric_id(institution.id)
FROM file('{{WORKS_GLOB}}', Parquet)
ARRAY JOIN authorships AS authorship
ARRAY JOIN authorship.institutions AS institution
WHERE openalex_numeric_id(id) IS NOT NULL
  AND openalex_numeric_id(authorship.author.id) IS NOT NULL
  AND openalex_numeric_id(institution.id) IS NOT NULL;

INSERT INTO openalex_spike.work_topic
SELECT
    openalex_numeric_id(id),
    openalex_numeric_id(topic.id),
    toFloat32(topic.score),
    ifNull(
        openalex_numeric_id(topic.id) = openalex_numeric_id(primary_topic.id),
        false
    )
FROM file('{{WORKS_GLOB}}', Parquet)
ARRAY JOIN topics AS topic
WHERE openalex_numeric_id(id) IS NOT NULL
  AND openalex_numeric_id(topic.id) IS NOT NULL
  AND topic.score IS NOT NULL;
```

Null/empty arrays naturally emit zero rows; malformed IDs are counted before
filtered inserts and are correctness failures. The raw evidence step also
records `countIf(topic.score IS NULL)` after expanding topics; a nonzero count
is a blocking schema/data failure before the filtered `work_topic` insert.

- [ ] **Step 4: Load dimensions and the reverse projection**

Stage 1 Authors use deterministic aggregation over embedded author tuples:

```sql
INSERT INTO openalex_spike.authors
SELECT
    openalex_numeric_id(authorship.author.id) AS author_id,
    max(authorship.author.id),
    max(authorship.author.display_name),
    nullIf(max(authorship.author.orcid), '')
FROM file('{{WORKS_GLOB}}', Parquet)
ARRAY JOIN authorships AS authorship
WHERE author_id IS NOT NULL
GROUP BY author_id;
```

Stage 2 Authors come from the complete Authors Parquet directory with:

```sql
INSERT INTO openalex_spike.authors
SELECT
    openalex_numeric_id(id), id, display_name, nullIf(orcid, '')
FROM file('{{AUTHORS_GLOB}}', Parquet)
WHERE openalex_numeric_id(id) IS NOT NULL;
```

Load the other dimensions with:

```sql
INSERT INTO openalex_spike.institutions
SELECT openalex_numeric_id(id), id, display_name, nullIf(country_code, ''), type
FROM file('{{INSTITUTIONS_GLOB}}', Parquet)
WHERE openalex_numeric_id(id) IS NOT NULL;

INSERT INTO openalex_spike.sources
SELECT openalex_numeric_id(id), id, display_name, nullIf(issn_l, ''), type
FROM file('{{SOURCES_GLOB}}', Parquet)
WHERE openalex_numeric_id(id) IS NOT NULL;

INSERT INTO openalex_spike.topics
SELECT
    openalex_numeric_id(id), display_name,
    openalex_numeric_id(subfield.id),
    openalex_numeric_id(field.id),
    openalex_numeric_id(domain.id)
FROM file('{{TOPICS_GLOB}}', Parquet)
WHERE openalex_numeric_id(id) IS NOT NULL
  AND openalex_numeric_id(subfield.id) IS NOT NULL
  AND openalex_numeric_id(field.id) IS NOT NULL
  AND openalex_numeric_id(domain.id) IS NOT NULL;
```

Create the planned variant:

```sql
ALTER TABLE openalex_spike.citation_edge ADD PROJECTION by_cited
(
    SELECT citing_work_id, cited_work_id, citing_year
    ORDER BY (cited_work_id, citing_work_id)
);
ALTER TABLE openalex_spike.citation_edge MATERIALIZE PROJECTION by_cited;
```

Do not execute `30_reverse_projection.sql` in the normal Task 6 or Stage 2 load
path. The integration test may create and drop it solely to verify syntax. The
real projection is first materialized in Task 13 Step 4, after baseline q05/q07
metrics have been captured.

- [ ] **Step 5: Run integration assertions and commit**

Run: `uv run pytest -m integration tests/integration/test_transform_sql.py -q`  
Expected: all transformation counts and ID assertions PASS.

```bash
git add sql tests/integration/test_transform_sql.py tests/fixtures
git commit -m "feat: materialize OpenAlex analytical tables"
```

## Task 7: Implement blocking correctness gates

**Files:**
- Create: `src/openalex_spike/correctness.py`
- Test: `tests/unit/test_correctness.py`
- Test: `tests/integration/test_correctness_queries.py`

- [ ] **Step 1: Define a structured gate result and failing unit tests**

```python
@dataclass(frozen=True)
class GateResult:
    name: str
    passed: bool
    expected: int | str
    actual: int | str
    evidence: dict[str, object]


def require_all(results: list[GateResult]) -> None:
    failed = [r for r in results if not r.passed]
    if failed:
        raise CorrectnessFailure(failed)
```

Test that one failure raises and that the serialized exception names the gate and expected/actual values.

- [ ] **Step 2: Implement all design gates as explicit queries**

Define one named `GateSpec` per design gate. Include these exact checks:

- verified manifest rows equal `SELECT count() FROM file('{{WORKS_GLOB}}', Parquet)`;
- raw Work rows equal `uniqExact(id)`; a duplicate Work ID is a blocking
  manifest/input failure because current OpenAlex manifests move changed Works
  rather than retaining old copies;
- the persisted `05_raw_evidence.sql` reject count is zero, its distinct-pair
  count equals `citation_edge` rows, and its duplicate delta is reported;
- independent raw array counts reconcile to each bridge table;
- `uniqExactIf(openalex_numeric_id(id), id IS NOT NULL)` equals the count of
  non-null canonical IDs for every loaded entity;
- left anti-join counts and percentages report bridge referential coverage and
  retained citation edges; closed Work/Author gaps are blocking, Topic gaps
  remain blocking because the Topics transformation has hierarchy exclusion
  predicates that must be ruled out, while independently pinned Institution
  gaps are explicit non-blocking observations with a capped raw ID/name sample
  and both manifest identities;
- authorships per Work, matched-Author fraction, and year/type/topic/XPAC
  distributions are emitted per tier;
- selector file-list bytes and order reproduce exactly;
- normalized correctness result hashes match after a rebuild.

Store every query text/hash and output in
`results/<run-id>/correctness.json` before calling `require_all`.

- [ ] **Step 3: Prove recreation determinism in integration tests**

Build the generated fixture database twice from empty state, normalize ordered result rows to canonical JSON, SHA-256 them, and assert identical table counts and hashes.

- [ ] **Step 4: Run tests and commit**

Run: `uv run pytest tests/unit/test_correctness.py tests/integration/test_correctness_queries.py -q`  
Expected: all tests PASS.

```bash
git add src/openalex_spike/correctness.py tests
git commit -m "feat: enforce Stage 1 correctness gates"
```

## Task 8: Add the fixed bibliometric query suite and sequential runner

**Files:**
- Create: `sql/queries/q01_works_by_year.sql`
- Create: `sql/queries/q02_topic_totals.sql`
- Create: `sql/queries/q03_author_output.sql`
- Create: `sql/queries/q04_collaboration.sql`
- Create: `sql/queries/q05_one_hop.sql`
- Create: `sql/queries/q06_two_hop.sql`
- Create: `sql/queries/q07_citations_by_year.sql`
- Create: `src/openalex_spike/benchmark.py`
- Test: `tests/unit/test_benchmark.py`

- [ ] **Step 1: Write query-catalog tests**

Assert that exactly seven named queries load, every query has a class (`routine`, `join`, `one_hop`, or `two_hop`), only q06 is diagnostic, and seed placeholders exist only in q05/q06.

- [ ] **Step 2: Add complete SQL files**

```sql
-- q01_works_by_year.sql
SELECT publication_year, work_type, is_oa, is_xpac, count() AS works
FROM openalex_spike.works
GROUP BY publication_year, work_type, is_oa, is_xpac
ORDER BY publication_year, work_type, is_oa, is_xpac;
```

```sql
-- q02_topic_totals.sql
SELECT
    w.publication_year,
    t.topic_id,
    t.display_name,
    countDistinct(w.work_id) AS works,
    sum(w.cited_by_count) AS citations
FROM openalex_spike.works AS w
INNER JOIN openalex_spike.work_topic AS wt ON w.work_id = wt.work_id
INNER JOIN openalex_spike.topics AS t ON wt.topic_id = t.topic_id
GROUP BY w.publication_year, t.topic_id, t.display_name
ORDER BY w.publication_year, works DESC;
```

```sql
-- q03_author_output.sql
SELECT
    a.author_id,
    a.display_name,
    countDistinct(wa.work_id) AS works,
    sum(w.cited_by_count) AS citations
FROM openalex_spike.work_author AS wa
INNER JOIN openalex_spike.authors AS a ON wa.author_id = a.author_id
INNER JOIN openalex_spike.works AS w ON wa.work_id = w.work_id
GROUP BY a.author_id, a.display_name
ORDER BY works DESC, a.author_id
LIMIT 1000;
```

```sql
-- q04_collaboration.sql
WITH work_country AS
(
    SELECT DISTINCT wi.work_id, i.country_code
    FROM openalex_spike.work_institution AS wi
    INNER JOIN openalex_spike.institutions AS i
        ON wi.institution_id = i.institution_id
    WHERE i.country_code IS NOT NULL AND i.country_code != ''
)
SELECT
    w.publication_year,
    a.country_code AS country_a,
    b.country_code AS country_b,
    countDistinct(a.work_id) AS collaborative_works
FROM work_country AS a
INNER JOIN work_country AS b
    ON a.work_id = b.work_id AND a.country_code < b.country_code
INNER JOIN openalex_spike.works AS w ON a.work_id = w.work_id
GROUP BY w.publication_year, country_a, country_b
ORDER BY w.publication_year, collaborative_works DESC;
```

q04 intentionally includes the country-pair self-join because cross-country
collaboration is part of the requested workload. Its memory cost is not treated
as an accidental query bug or silently replaced with a precomputed table.
Likewise, q02/q03 intentionally retain exact `countDistinct(work_id)` after
bridge joins. Spill or memory pressure from these exact bibliometric counts is
part of the tested workload, not grounds for silently substituting approximate
aggregates.

```sql
-- q05_one_hop.sql
SELECT 'outgoing' AS direction, cited_work_id AS neighbour_work_id
FROM openalex_spike.citation_edge
WHERE citing_work_id = {seed_work_id:UInt64}
UNION ALL
SELECT 'incoming' AS direction, citing_work_id AS neighbour_work_id
FROM openalex_spike.citation_edge
WHERE cited_work_id = {seed_work_id:UInt64};
```

```sql
-- q06_two_hop.sql (diagnostic only)
SELECT countDistinct(second.cited_work_id) AS second_hop_works
FROM openalex_spike.citation_edge AS first
INNER JOIN openalex_spike.citation_edge AS second
    ON first.cited_work_id = second.citing_work_id
WHERE first.citing_work_id = {seed_work_id:UInt64};
```

```sql
-- q07_citations_by_year.sql
SELECT
    citing_year,
    cited_work_id,
    count() AS citations
FROM openalex_spike.citation_edge
GROUP BY citing_year, cited_work_id
ORDER BY citations DESC, cited_work_id
LIMIT 1000;
```

All seed values use typed ClickHouse query parameters, never string
interpolation.

- [ ] **Step 3: Implement deterministic seeds and sequential metrics**

Select seeds from median, p95, and maximum `referenced_works_count`. Apply the
active envelope to every session: sequential queries use `max_threads=16`;
`max_memory_usage`, external group-by bytes, and external sort bytes come from
the configured 32/50 GB envelope; `join_algorithm='auto'`. For each query:
restart ClickHouse, label the first result `post_restart_run`, execute five
subsequent runs with UUID query IDs, `SYSTEM FLUSH LOGS`, and export matching
`system.query_log` rows. Record elapsed time, read rows/bytes, result rows, peak
memory, and spill profile events. Export `system.settings` rows where
`changed=1` plus the named relevant defaults to `settings.json`.

- [ ] **Step 4: Test with a fake client and commit**

The fake client returns fixed telemetry. Assert one post-restart plus five warm results, stable query IDs, no use of the word `cold`, and q06 marked non-gating.

Run: `uv run pytest tests/unit/test_benchmark.py -q`  
Expected: all benchmark runner tests PASS.

```bash
git add sql/queries src/openalex_spike/benchmark.py tests/unit/test_benchmark.py
git commit -m "feat: add reproducible bibliometric benchmark suite"
```

## Task 9: Add the three-client concurrency harness

**Files:**
- Create: `src/openalex_spike/concurrency.py`
- Test: `tests/unit/test_concurrency.py`

- [ ] **Step 1: Write tests for deterministic scheduling and verdict caps**

Use a fake clock and runner. Assert three workers cycle through routine/join/one-hop queries, stop when every gated class reaches 50 or 3,600 seconds, exclude two-hop, and set `verdict_cap="conditional"` when any class has fewer than 50 samples.

- [ ] **Step 2: Implement closed-loop workers**

Use `ThreadPoolExecutor(max_workers=3)`, one ClickHouse client per worker, a
fixed catalog order rotated by worker index, monotonic deadlines, and a
thread-safe metrics queue. Every concurrent session uses `max_threads=8` plus
the active envelope's memory/spill settings. Do not retry query errors: record
the first error, set `forced_verdict="fail"`, and stop the run. This Fail flag
dominates the under-50-sample Conditional cap.

- [ ] **Step 3: Calculate defensible statistics**

For each query and class report count, median, nearest-rank p95, maximum, and an
`insufficient_sample` flag. When count is below 50, retain the descriptive p95
but exclude it from verdict evaluation and cap the non-error verdict at
Conditional. Preserve raw per-query records in JSONL so statistics are
reproducible.

- [ ] **Step 4: Run tests and commit**

Run: `uv run pytest tests/unit/test_concurrency.py -q`  
Expected: all concurrency tests PASS.

```bash
git add src/openalex_spike/concurrency.py tests/unit/test_concurrency.py
git commit -m "feat: benchmark three concurrent ClickHouse clients"
```

## Task 10: Model storage per table and render the evidence report

**Files:**
- Create: `src/openalex_spike/storage.py`
- Create: `src/openalex_spike/report.py`
- Test: `tests/unit/test_storage.py`
- Test: `tests/unit/test_report.py`

- [ ] **Step 1: Write per-table scaling tests**

```python
def test_citation_edges_scale_by_edges_per_work_not_raw_bytes():
    estimate = estimate_works_derived(
        sample_work_rows=1_000,
        sample_output_rows=25_000,
        sample_native_bytes=200_000,
        full_work_rows=510_372_821,
    )
    assert estimate.output_rows == 12_759_320_525
    assert estimate.native_bytes == 102_074_564_200
```

Also test low/expected/high stratum rates, complete-dimension no-scaling, projection ratio, one/two-generation layouts, observed peak, conservative 100% headroom, and `Likely fits`/`Uncertain`/`Likely exceeds` classification.

- [ ] **Step 2: Implement system.parts and disk-peak collection**

Poll `system.parts` and `system.projection_parts` plus `.data/clickhouse` directory bytes during loads and projection materialization. Store timestamped samples. Never infer peak from final size alone.

- [ ] **Step 3: Implement report rendering**

Render `results/<run-id>/report.json` and `report.md` containing input/manifest identity, host/container identity, settings, correctness gates, tier distributions, sequential/concurrent metrics, edge retention beside citation results, reverse-projection before/after cost, memory-envelope comparison, scaling slopes with explicit non-prediction language, capacity ranges, and separate local-engine/capacity verdicts.

- [ ] **Step 4: Run tests and commit**

Run: `uv run pytest tests/unit/test_storage.py tests/unit/test_report.py -q`  
Expected: all storage/report tests PASS.

```bash
git add src/openalex_spike/storage.py src/openalex_spike/report.py tests/unit
git commit -m "feat: report benchmark and capacity evidence"
```

## Task 11: Wire an explicit, resumable CLI

**Files:**
- Create: `src/openalex_spike/cli.py`
- Test: `tests/unit/test_cli.py`

- [ ] **Step 1: Write CLI contract tests**

Assert these commands exist and refuse missing prerequisites with nonzero
status: `pin-manifests`, `select`, `download`, `clickhouse-up`, `stage1`,
`stage2`, `report`, and `clickhouse-down`. Assert `download` exposes
`--tier`, `--include-complete-authors`, and `--include-small-dimensions`; the
last two map only to the complete pinned entity manifests defined in Task 4.
Assert there is no command that silently chooses an alternate storage path or
engine.

- [ ] **Step 2: Implement argparse command routing**

Each command writes a run-state JSON recording completed step, inputs, outputs,
and command version. `stage1` requires pinned/verified Stage 1 files, builds the
real 1 GiB database twice under isolated database names, compares normalized
counts/result hashes, and stops on any correctness or rebuild-determinism
failure. `stage2` requires a passing Stage 1 state and runs the 3/15/45 GB curve
at 50 GB, then repeats 45 GB at 32 GB, then builds/measures the reverse
projection.

- [ ] **Step 3: Add safe SQL template validation**

Before replacing `{{WORKS_GLOB}}` or dimension globs, require paths to be
relative beneath `/var/lib/clickhouse/user_files/raw/tiers/`, reject quotes and
`..`, and log the rendered SQL SHA-256. Perform template replacement only with
literal `str.replace`; never call `str.format`, so typed ClickHouse parameter
braces and SQL backslashes are untouched. Query values use ClickHouse typed
parameters.

- [ ] **Step 4: Run tests and commit**

Run: `uv run pytest tests/unit/test_cli.py -q && uv run openalex-spike --help`  
Expected: CLI tests PASS and help lists the eight commands.

```bash
git add src/openalex_spike/cli.py tests/unit/test_cli.py
git commit -m "feat: orchestrate the validation pipeline"
```

## Task 12: Document and execute the 1 GiB correctness stage

**Files:**
- Create: `README.md`
- Create: `results/stage1/report.json`
- Create: `results/stage1/report.md`
- Modify: `.gitignore`

- [ ] **Step 1: Document prerequisites and exact commands**

README must state that Docker Desktop needs at least 32 GB for Stage 1 and at least 54 GB for the 50 GB run, raw downloads are not committed, local results are sample-scale, and Alliance performance remains unvalidated. Include:

```bash
uv sync --extra dev
uv run openalex-spike pin-manifests
uv run openalex-spike select
uv run openalex-spike download --tier stage1 --include-small-dimensions
uv run openalex-spike clickhouse-up --memory-gb 32
uv run openalex-spike stage1
uv run openalex-spike report --run stage1
uv run openalex-spike clickhouse-down
```

- [ ] **Step 2: Run all unit and integration tests**

Run: `uv run pytest -q`  
Expected: all tests PASS.

- [ ] **Step 3: Execute Stage 1 end-to-end**

Run the documented commands. Expected: selected Works input approximately 1
GiB; every correctness gate PASS; no emulation; two isolated real-data builds
produce identical normalized counts/result hashes; report files generated. If
a gate fails, stop, diagnose, and revise the design—do not continue to Stage 2.

- [ ] **Step 4: Inspect evidence and commit only compact results**

Confirm filtered query evidence contains only measured IDs and no credentials/URLs with signed tokens. Keep raw query JSONL only if compact; keep raw Parquet and ClickHouse state ignored.

```bash
git add README.md .gitignore results/stage1
git commit -m "test: validate OpenAlex Stage 1 in ClickHouse"
```

## Task 13: Execute the 98 GB multi-scale performance stage

**Files:**
- Create: `results/stage2/report.json`
- Create: `results/stage2/report.md`
- Create: `results/stage2/query-log.jsonl`
- Create: `results/stage2/disk-samples.jsonl`

- [ ] **Step 1: Download and verify the maximum nested selection**

Run: `uv run openalex-spike download --tier stage2_large --include-complete-authors --include-small-dimensions`  
Expected: approximately 98.1 GB for the pinned 2026-06-26 manifest; exact bytes and rows match the selection and manifests.

- [ ] **Step 2: Run the 50 GB scaling curve**

Run: `uv run openalex-spike clickhouse-up --memory-gb 50 && uv run openalex-spike stage2 --memory-gb 50`  
Expected: 3/15/45 GB tiers complete in order, correctness remains passing, sequential metrics and scaling slopes are recorded, three-client classes reach 50 samples or receive a Conditional cap, and two-hop is diagnostic only.

- [ ] **Step 3: Run the 32 GB sensitivity envelope**

Run: `uv run openalex-spike stage2 --memory-gb 32 --tier stage2_large`  
Expected: the 45 GB tier records the 32 GB envelope with its distinct per-query/spill settings and does not overwrite 50 GB results.

- [ ] **Step 4: Build and measure the reverse projection**

Run the planned projection variant and repeat q05/q07. Expected: build time, peak/final disk, and before/after metrics are present.

- [ ] **Step 5: Generate, inspect, and commit compact evidence**

Run: `uv run openalex-spike report --run stage2`  
Expected: report distinguishes local engine verdict, storage capacity result, and unvalidated Alliance claims.

```bash
git add results/stage2
git commit -m "test: benchmark OpenAlex ClickHouse sample"
```

## Task 14: Prepare the Alliance environmental-spike handoff

**Files:**
- Create: `docs/alliance-clickhouse-spike-runbook.md`

- [ ] **Step 1: Write the no-fallback Alliance runbook**

Include the measured resource request range, exact pinned image digest, one-file Swift/S3 authentication test, public-port prohibition, persistent-volume throughput test, full/maximum-corpus load command, DBeaver-over-SSH test, and explicit stop condition if Swift is not S3-compatible.

- [ ] **Step 2: Link every request to local evidence**

For CPU, RAM, block storage, object storage, and rebuild overlap, cite the exact Stage 2 report field that supports the requested quantity. Label modeled and measured values separately.

- [ ] **Step 3: Run final QA and commit**

Run: `uv run pytest -q && git diff --check`  
Expected: all tests PASS and no whitespace errors.

```bash
git add docs/alliance-clickhouse-spike-runbook.md
git commit -m "docs: add Alliance ClickHouse spike runbook"
```
