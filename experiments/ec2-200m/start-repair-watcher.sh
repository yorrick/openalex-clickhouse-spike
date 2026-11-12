#!/bin/bash
set -euo pipefail
cd /opt/oa200
test ! -f results/postgres/repair-complete.json
cat > after-baseline-repair.sh <<'EOF'
#!/bin/bash
set -euo pipefail
cd /opt/oa200
while ! test -f results/engines-complete.json; do
 if test -f results/engine-error.json; then echo 'Baseline failed; inspect evidence before repair'; exit 1; fi
 # Leave more than 90 minutes before the independent termination deadline.
 if test "$(date -u +%s)" -gt 1794547200; then echo 'Repair time reserve exhausted'; exit 1; fi
 sleep 5
done
exec .venv/bin/python repair_pg_shm.py
EOF
chmod 700 after-baseline-repair.sh
systemd-run --unit=oa200-pg-repair --property=WorkingDirectory=/opt/oa200 --property=StandardOutput=append:/opt/oa200/runtime-repair.log --property=StandardError=append:/opt/oa200/runtime-repair.log /bin/bash /opt/oa200/after-baseline-repair.sh
systemctl is-active oa200-pg-repair.service
