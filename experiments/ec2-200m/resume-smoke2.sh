set -euo pipefail
cd /opt/oa200
systemctl stop oa200-bench.service || true
cp smoke/results/engine-error.json results/smoke-attempt2-readiness-error.json
.venv/bin/aws s3 cp s3://oa200-20261112-e504ff-502425560524/run/code/payload.tar.gz payload.tar.gz --region us-east-1 --only-show-errors
printf '%s  payload.tar.gz\n' 6c45a2cbc6c82caf21c5207ecdb825adfa07142f6578d7e435bb12354ca063f9 | sha256sum -c -
tar xzf payload.tar.gz
systemctl reset-failed oa200-bench.service || true
systemctl start oa200-bench.service
