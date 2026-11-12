set -euo pipefail
cd /opt/oa200
test "$(systemctl is-active oa200-bench.service || true)" = failed
cp smoke/results/engine-error.json results/smoke-initial-ch-ownership-error.json
.venv/bin/aws s3 cp s3://oa200-20261112-e504ff-502425560524/run/code/payload.tar.gz payload.tar.gz --region us-east-1 --only-show-errors
printf '%s  payload.tar.gz\n' aa6a8b33bc7ee71be8e635742c90542c050a7909c1665c4c1929994dfbcd4a7c | sha256sum -c -
tar xzf payload.tar.gz
systemctl reset-failed oa200-bench.service
systemctl start oa200-bench.service
tail -5 runtime.log
