from __future__ import annotations

from pathlib import Path
from typing import Any
import json


def render_report(
    destination: Path, evidence: dict[str, Any]
) -> tuple[Path, Path]:
    required = {
        "run_id",
        "inputs",
        "environment",
        "correctness",
        "sequential",
        "concurrent",
        "storage",
        "local_engine_verdict",
        "capacity_verdict",
        "limitations",
    }
    missing = required - evidence.keys()
    if missing:
        raise ValueError(f"report evidence is missing: {sorted(missing)}")
    destination.mkdir(parents=True, exist_ok=True)
    json_path = destination / "report.json"
    markdown_path = destination / "report.md"
    json_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")

    limitations = "\n".join(f"- {item}" for item in evidence["limitations"])
    markdown = f"""# OpenAlex ClickHouse validation — {evidence['run_id']}

Local engine verdict: {evidence['local_engine_verdict']}

Capacity verdict: {evidence['capacity_verdict']}

## Input and environment identity

```json
{json.dumps({'inputs': evidence['inputs'], 'environment': evidence['environment']}, indent=2, sort_keys=True)}
```

## Correctness

```json
{json.dumps(evidence['correctness'], indent=2, sort_keys=True)}
```

## Sequential and concurrent evidence

```json
{json.dumps({'sequential': evidence['sequential'], 'concurrent': evidence['concurrent']}, indent=2, sort_keys=True)}
```

## Storage and capacity evidence

```json
{json.dumps(evidence['storage'], indent=2, sort_keys=True)}
```

Scaling slopes are empirical evidence from sampled tiers; they are not a full-size prediction.

## Limitations

{limitations}
"""
    markdown_path.write_text(markdown)
    return json_path, markdown_path
