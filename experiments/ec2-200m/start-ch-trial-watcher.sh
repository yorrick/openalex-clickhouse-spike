#!/bin/bash
set -euo pipefail
cd /opt/oa200
.venv/bin/aws s3 cp s3://oa200-20261112-e504ff-502425560524/run/code/payload.tar.gz trial-payload.tar.gz --region us-east-1 --only-show-errors
echo 'e8f05e245f6a95abae38a6b27496e3af2113ffae0e09491c50e88adcfbe79ae3  trial-payload.tar.gz' | sha256sum -c -
tar -xzf trial-payload.tar.gz
.venv/bin/python -m py_compile run_engines.py trial_ch_grace.py
.venv/bin/python - <<'PY'
from pathlib import Path
import json,hashlib,time
names=['run_engines.py','trial_ch_grace.py','sql/clickhouse-q04_country_sets.sql']
Path('results/ch-trial-code-hashes.json').write_text(json.dumps({'at':time.time(),'payload_sha256':'e8f05e245f6a95abae38a6b27496e3af2113ffae0e09491c50e88adcfbe79ae3','files':{name:hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in names}},indent=2))
PY
cat > after-pg-ch-trial.sh <<'EOF'
#!/bin/bash
set -euo pipefail
cd /opt/oa200
while ! test -f results/postgres/repair-complete.json; do
 if systemctl is-failed --quiet oa200-pg-repair.service; then echo 'PG repair failed; inspect before CH trial'; exit 1; fi
 if test "$(date -u +%s)" -gt 1794547200; then echo 'CH trial time reserve exhausted'; exit 1; fi
 sleep 5
done
exec .venv/bin/python trial_ch_grace.py
EOF
chmod 700 after-pg-ch-trial.sh
systemd-run --unit=oa200-ch-trial --property=WorkingDirectory=/opt/oa200 --property=StandardOutput=append:/opt/oa200/runtime-ch-trial.log --property=StandardError=append:/opt/oa200/runtime-ch-trial.log /bin/bash /opt/oa200/after-pg-ch-trial.sh
systemctl is-active oa200-ch-trial.service
