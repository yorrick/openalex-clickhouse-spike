#!/bin/bash
# Execute only after measured cases and any bounded trials are settled.
set -euo pipefail
cd /opt/oa200
test -f results/postgres-cases.json
test -f results/clickhouse-cases.json
.venv/bin/python -c 'import json; assert json.load(open("results/experiment-settled.json"))["settled"] is True'
systemctl stop oa200-sync.timer
systemctl stop oa200-bench.service
.venv/bin/python - <<'PY'
import subprocess
for unit in ['oa200-pg-repair.service','oa200-ch-trial.service']:
 state=subprocess.run(['systemctl','show','--property=LoadState','--value',unit],capture_output=True,text=True).stdout.strip()
 assert state in ['loaded','not-found'],(unit,state)
 if state=='loaded':subprocess.run(['systemctl','stop',unit],check=True)
PY
systemctl stop oa200-sync.service
.venv/bin/python - <<'PY'
from pathlib import Path
import hashlib,json,subprocess,psutil,shutil,time,tarfile
p=Path('/opt/oa200').resolve()
for name in ['oa200-pg','oa200-ch']:
 r=subprocess.run(['docker','inspect',name],capture_output=True,text=True,check=True);x=json.loads(r.stdout)[0];assert x['Config']['Labels'].get('openalex.study')=='ec2-200m-20261112'
 if x['State']['Running']:subprocess.run(['docker','stop',name],check=True)
samplers=[]
for process in psutil.process_iter(['pid','cmdline']):
 args=process.info['cmdline'] or []
 if args and [Path(args[0]).name,*args[1:]] in [['iostat','-x','-d','-t','1'],['vmstat','-t','1']]:
  process.terminate();samplers.append(process)
_,alive=psutil.wait_procs(samplers,timeout=5)
assert not alive, 'Host telemetry writers must stop before evidence is sealed'
for name in ['oa200-bootstrap.log','cloud-init-output.log']:
 source=Path('/var/log')/name
 if source.exists():shutil.copy2(source,p/'results'/name)
for name in ['runtime.log','runtime-repair.log','runtime-ch-trial.log']:
 source=p/name
 if source.exists():shutil.copy2(source,p/'results'/name)
password=(p/'secrets/password').read_bytes()
files=sorted(set([f for f in (p/'results').rglob('*') if f.is_file() and f.name!='frozen-manifest.json']+[f for f in (p/'sql').rglob('*') if f.is_file()]+[f for f in p.glob('*.py')]+[f for f in p.glob('*.sh')]+[p/'input-manifest.json',p/'projection-templates.json',p/'plan.md']))
records=[]
for f in files:
 assert not f.is_symlink();data=f.read_bytes();assert password not in data,('Credential detected',str(f));records.append({'path':str(f.relative_to(p)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
proof={'frozen_at':time.time(),'credential_scan_passed':True,'scope':'Only results, SQL, experiment source and input metadata; raw dataset, database files, venv and secrets excluded. Both main engines stopped; host iostat/vmstat stopped.','files':records}
manifest=p/'results/frozen-manifest.json';manifest.write_text(json.dumps(proof,indent=2)+'\n')
archive=p/'frozen-evidence.tar.gz'
with tarfile.open(archive,'w:gz',compresslevel=1) as tar:
 for f in files+[manifest]:tar.add(f,arcname=str(f.relative_to(p)),recursive=False)
h=hashlib.sha256(archive.read_bytes()).hexdigest();out={'archive_bytes':archive.stat().st_size,'archive_sha256':h,'members':len(files)+1,'manifest_files':len(records),'credential_scan_passed':True,'frozen_at':proof['frozen_at']};(p/'frozen-evidence.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
PY
.venv/bin/aws s3 cp frozen-evidence.tar.gz s3://oa200-20261112-e504ff-502425560524/run/final/frozen-evidence.tar.gz --region us-east-1 --only-show-errors
.venv/bin/aws s3 cp frozen-evidence.json s3://oa200-20261112-e504ff-502425560524/run/final/frozen-evidence.json --region us-east-1 --only-show-errors
/usr/local/sbin/oa200-sync
