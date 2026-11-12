#!/bin/bash
set -euo pipefail
cd /opt/oa200
.venv/bin/aws s3 cp s3://oa200-20261112-e504ff-502425560524/run/code/payload.tar.gz final-payload.tar.gz --region us-east-1 --only-show-errors
echo '012915c2a64b75addb5c7f95f0c5294feee5a0b42d15861979caa9f2323f00c7  final-payload.tar.gz' | sha256sum -c -
tar -xzf final-payload.tar.gz
.venv/bin/python settle_metadata.py
/bin/bash freeze_evidence.sh
