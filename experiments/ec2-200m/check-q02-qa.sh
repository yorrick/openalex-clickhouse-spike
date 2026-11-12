#!/bin/bash
set -euo pipefail
cd /opt/oa200
.venv/bin/python - <<'PYREMOTE'
from pathlib import Path
import json
x=json.loads(Path("results/clickhouse-selected.json").read_text())["q02"]
assert x["qa"]["rows"]==1264122 and x["qa"]["canonical_sha256"]=='73d142aaa9963a40d8a4779f8ef9ff01c498a764ce549c62a3641a186bea3603'
print("q02 full raw Athena output PASS",x["qa"],x["median_seconds"])
PYREMOTE
cat /usr/local/sbin/oa200-sync
systemctl status oa200-sync.service --no-pager -n 5
