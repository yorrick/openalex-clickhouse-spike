set -euo pipefail
cd /opt/oa200
test "$(systemctl is-active oa200-bench.service || true)" = failed
cp runtime.log results/runtime-through-source-scope-error.log
.venv/bin/aws s3 cp s3://oa200-20261112-e504ff-502425560524/run/code/payload.tar.gz payload.tar.gz --region us-east-1 --only-show-errors
printf '%s  payload.tar.gz\n' 629c5edc810b765368d4f45d4dde4694ddc9b33d93a4f1bd9dc713511c4f4765 | sha256sum -c -
tar xzf payload.tar.gz
.venv/bin/python - <<'CHECK'
import pathlib,json,hashlib,time
p=pathlib.Path('/opt/oa200');assert json.loads((p/'results/smoke-pass.json').read_text())['all11_full_results_match']
x={'at':time.time(),'payload_sha256':'629c5edc810b765368d4f45d4dde4694ddc9b33d93a4f1bd9dc713511c4f4765','amendment':'Historical source provenance catalog also includes15lookup entities (393files,30.131MB) outside the42column/9table benchmark. Explicitly project only Works/Authors/Institutions/Sources/Topics, record unused raw inventory. Resume already sealed download and completed author projections; no alternate source or schema substitution.','files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in p.glob('*.py')}}
(p/'results/harness-code-hashes.json').write_text(json.dumps(x,indent=2))
CHECK
systemctl reset-failed oa200-bench.service
systemctl start oa200-bench.service
