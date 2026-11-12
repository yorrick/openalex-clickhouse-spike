#!/bin/bash
set -euo pipefail
cd /opt/oa200
if [ ! -f results/smoke-pass.json ]; then .venv/bin/python -u smoke.py; fi
.venv/bin/python -u normalize.py
.venv/bin/python -u run_engines.py
