#!/bin/bash
set -euo pipefail
cd /opt/oa200
.venv/bin/python - <<'PY'
import json
from pathlib import Path
for q in ['q02','q03']:
 p=Path('results/postgres')/(q+'-estimated-plan-after-shm-error.json')
 x=json.loads(p.read_text())
 def walk(n,level=0):
  print(' '*level,{k:n[k] for k in ['Node Type','Join Type','Plan Rows','Plan Width','Parallel Aware','Workers Planned','Hash Cond','Relation Name','Group Key'] if k in n})
  for c in n.get('Plans',[]):walk(c,level+1)
 print(q);walk(x[0]['Plan'] if isinstance(x,list) else x.get('Plan',x))
for p in sorted(Path('results/postgres').glob('q0*.json')):
 if 'telemetry' in p.name or 'plan-' in p.name:continue
 x=json.loads(p.read_text());print(p.name,x.get('state'),x.get('median_seconds'),x.get('qa'))
PY
tail -5 runtime.log
df -h /opt/oa200
