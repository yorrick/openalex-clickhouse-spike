#!/bin/bash
set -euo pipefail
cd /opt/oa200
.venv/bin/python - <<'PY'
from pathlib import Path
import tarfile,hashlib,json
proof=json.loads(Path('results/repair-code-hashes.json').read_text())
with tarfile.open('repair-payload.tar.gz') as tar:
 for name in ['run_engines.py','repair_pg_shm.py']:
  data=tar.extractfile(name).read();actual=hashlib.sha256(data).hexdigest();assert actual==proof['files'][name]
  path=Path(name).with_stem(Path(name).stem+'_pg_executed');path.write_bytes(data)
  print(path.name,actual)
PY
tail -6 runtime-repair.log
