#!/bin/bash
set -euo pipefail
exec > >(tee -a /var/log/oa200-bootstrap.log) 2>&1
cat >/etc/systemd/system/oa200-expire.service <<'EOF'
[Service]
Type=oneshot
ExecStart=/usr/bin/systemctl poweroff
EOF
cat >/etc/systemd/system/oa200-expire.timer <<'EOF'
[Timer]
OnBootSec=12h
AccuracySec=1s
[Install]
WantedBy=timers.target
EOF
systemctl daemon-reload
systemctl enable --now oa200-expire.timer
apt-get -o DPkg::Lock::Timeout=300 update
DEBIAN_FRONTEND=noninteractive apt-get -o DPkg::Lock::Timeout=300 install -y docker.io python3-venv python3-pip sysstat jq
systemctl enable --now docker
snap start amazon-ssm-agent || true
DISK=$(python3 - <<'PY'
import json,subprocess
x=json.loads(subprocess.check_output(['lsblk','-J','-b','-o','PATH,SIZE,TYPE,FSTYPE,MOUNTPOINTS']))
y=[d['path'] for d in x['blockdevices'] if d['type']=='disk' and int(d['size'])==1024*2**30 and not d.get('children') and not d.get('fstype') and not any(d.get('mountpoints',[]))]
assert len(y)==1,y
print(y[0])
PY
)
mkfs.ext4 -E lazy_itable_init=0,lazy_journal_init=0 -L oa200scratch "$DISK"
STUDY=/home/ubuntu/work/data/openalex-ec2-200m-20261112
mkdir -p "$STUDY"
mount -o noatime "$DISK" "$STUDY"
ln -s "$STUDY" /opt/oa200
mkdir -p "$STUDY/results" "$STUDY/secrets" "$STUDY/temp"
chmod 700 "$STUDY/secrets"
python3 -m venv "$STUDY/.venv"
"$STUDY/.venv/bin/pip" install --disable-pip-version-check 'boto3>=1.40' 'duckdb==2.0.0' 'pyarrow==26.0.0' 'psycopg[binary]==3.3.8' 'psutil==7.2.2' awscli
"$STUDY/.venv/bin/python" - <<'PY'
import duckdb
from pathlib import Path
p=Path('/opt/oa200/duckdbhome');p.mkdir(exist_ok=True)
x=duckdb.connect();x.execute('SET home_directory=?',[str(p)]);x.execute('INSTALL postgres');x.execute('INSTALL httpfs')
PY
docker pull postgres@sha256:5a5a84b19854a9ffaa54082c166ff4ec27473a361e496e5ea167f298f2da9722
docker pull clickhouse/clickhouse-server@sha256:1f7cd090d5c4e2b8bfe0ea5d8ae6125937e1d932c6371b4d25fbd6088829dc9c
uname -a > "$STUDY/results/uname.txt"
lscpu -J > "$STUDY/results/lscpu.json"
lsblk -J -b -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS > "$STUDY/results/lsblk.json"
date -u +%FT%TZ > "$STUDY/results/bootstrap-ready.txt"
