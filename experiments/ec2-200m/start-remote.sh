set -euo pipefail
cd /opt/oa200
test -f results/bootstrap-ready.txt
.venv/bin/aws s3 cp s3://oa200-20261112-e504ff-502425560524/run/code/payload.tar.gz payload.tar.gz --region us-east-1 --only-show-errors
printf '%s  payload.tar.gz\n' 463fe6acd0bac1dcc16f9d533d84f3c1e521255b471334059472f6059baf5370 | sha256sum -c -
tar xzf payload.tar.gz
chmod +x pipeline.sh
cat > /usr/local/sbin/oa200-sync <<'EOF'
#!/bin/bash
set -eu
/opt/oa200/.venv/bin/aws s3 sync /opt/oa200/results s3://oa200-20261112-e504ff-502425560524/run/results --region us-east-1 --only-show-errors
/opt/oa200/.venv/bin/aws s3 sync /opt/oa200/sql s3://oa200-20261112-e504ff-502425560524/run/results/sql --region us-east-1 --only-show-errors
if [ -d /opt/oa200/smoke/results ]; then
/opt/oa200/.venv/bin/aws s3 sync /opt/oa200/smoke/results s3://oa200-20261112-e504ff-502425560524/run/results/smoke --region us-east-1 --only-show-errors
fi
/opt/oa200/.venv/bin/aws s3 cp /opt/oa200/runtime.log s3://oa200-20261112-e504ff-502425560524/run/results/runtime.log --region us-east-1 --only-show-errors
EOF
chmod +x /usr/local/sbin/oa200-sync
cat > /etc/systemd/system/oa200-sync.service <<'EOF'
[Service]
Type=oneshot
ExecStart=/usr/local/sbin/oa200-sync
EOF
cat > /etc/systemd/system/oa200-sync.timer <<'EOF'
[Timer]
OnBootSec=1min
OnUnitActiveSec=1min
[Install]
WantedBy=timers.target
EOF
cat > /etc/systemd/system/oa200-bench.service <<'EOF'
[Unit]
After=docker.service
Requires=docker.service
[Service]
Type=simple
WorkingDirectory=/opt/oa200
ExecStart=/bin/bash /opt/oa200/pipeline.sh
ExecStopPost=/usr/local/sbin/oa200-sync
StandardOutput=append:/opt/oa200/runtime.log
StandardError=append:/opt/oa200/runtime.log
TimeoutStopSec=120
EOF
cat > /etc/systemd/system/oa200-expire.service <<'EOF'
[Service]
Type=oneshot
ExecStart=/bin/bash -c '/usr/local/sbin/oa200-sync; /usr/bin/systemctl poweroff'
TimeoutStartSec=180
EOF
touch runtime.log
systemctl daemon-reload
systemctl enable --now oa200-sync.timer
systemctl start oa200-bench.service
iostat -x -d -t 1 > results/host-iostat.log 2>&1 &
vmstat -t 1 > results/host-vmstat.log 2>&1 &
systemctl is-active oa200-expire.timer oa200-sync.timer oa200-bench.service
tail -8 runtime.log
