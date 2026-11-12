#!/bin/bash
set -euo pipefail
cd /opt/oa200
.venv/bin/aws s3 cp s3://oa200-20261112-e504ff-502425560524/run/code/payload.tar.gz repair-payload.tar.gz --region us-east-1 --only-show-errors
echo '0e5f0022151f654d63a74b1db55f66916b55210653ffcfce715acfcd12af94ec  repair-payload.tar.gz' | sha256sum -c -
tar -xzf repair-payload.tar.gz
.venv/bin/python -m py_compile repair_pg_shm.py run_engines.py
.venv/bin/python - <<'PY'
from pathlib import Path
import hashlib,json,time
paths=[Path('run_engines.py'),Path('repair_pg_shm.py'),Path('run_engines_baseline.py')]
assert hashlib.sha256(Path('run_engines_baseline.py').read_bytes()).hexdigest()=='0a84659cad14ce93022cba1eb6563d0c6f6a8d9597effa13d7b919d879e50386'
Path('results/repair-code-hashes.json').write_text(json.dumps({'at':time.time(),'payload_sha256':'0e5f0022151f654d63a74b1db55f66916b55210653ffcfce715acfcd12af94ec','files':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}},indent=2))
PY
# Install code only. The baseline process already has its functions loaded and is
# deliberately allowed to complete before the separate repair is started.
tail -6 runtime.log
