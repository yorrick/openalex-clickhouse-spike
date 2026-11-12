#!/bin/bash
set -euo pipefail
cd /opt/oa200
.venv/bin/python - <<'PY'
from pathlib import Path
import json
p=Path('results/postgres/q07-ordered-count-estimated-plan.json')
if p.exists():
 x=json.loads(p.read_text())
 def walk(n,depth=0):
  print(' '*depth,{k:n[k] for k in ['Node Type','Plan Rows','Parallel Aware','Workers Planned','Index Name','Group Key','Sort Key','Presorted Key'] if k in n})
  for child in n.get('Plans',[]):walk(child,depth+1)
 walk(x[0]['Plan'])
else:print('Estimated plan pending')
PY
tail -6 runtime-repair.log
