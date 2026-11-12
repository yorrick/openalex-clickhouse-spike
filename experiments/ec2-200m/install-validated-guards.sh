set -euo pipefail
cd /opt/oa200
.venv/bin/aws s3 cp s3://oa200-20261112-e504ff-502425560524/run/code/payload.tar.gz payload.tar.gz --region us-east-1 --only-show-errors
printf '%s  payload.tar.gz\n' f3d85a8692c351b5787e4bc6c9b343cbb79ce8b937ddea09ead241d12088adc6 | sha256sum -c -
tar xzf payload.tar.gz
.venv/bin/python - <<'CHECK'
import pathlib,json,hashlib,time
p=pathlib.Path('/opt/oa200');proof={'at':time.time(),'payload_sha256':'f3d85a8692c351b5787e4bc6c9b343cbb79ce8b937ddea09ead241d12088adc6','files':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in p.glob('*.py')},'note':'Readiness and ownership fixes passed all11typedfixturecases. Added disjoint smoke container names/bind guards and serial independent raw-value sample audit before real engine loading; SQL/settings unchanged.'}
(p/'results/harness-code-hashes.json').write_text(json.dumps(proof,indent=2))
CHECK
tail -6 runtime.log
