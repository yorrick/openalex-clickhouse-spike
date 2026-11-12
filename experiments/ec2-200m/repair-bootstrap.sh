set -eu
/opt/oa200/.venv/bin/python - <<'PY'
import os,json,duckdb,pathlib
p=pathlib.Path('/opt/oa200');out={'home_set_in_ssm':bool(os.environ.get('HOME')),'cloud_init_failure':'DuckDB INSTALL could not resolve empty home directory'}
d=duckdb.connect();directory=p/'duckdbhome';directory.mkdir(exist_ok=True)
d.execute('SET home_directory=?',[str(directory)]);d.execute('INSTALL postgres');d.execute('LOAD postgres');d.execute('INSTALL httpfs');d.execute('LOAD httpfs');out['explicit_home_extension_install_and_load_pass']=True
(p/'results/bootstrap-home-repair.json').write_text(json.dumps(out,indent=2))
print(out)
PY
docker pull postgres@sha256:5a5a84b19854a9ffaa54082c166ff4ec27473a361e496e5ea167f298f2da9722
docker pull clickhouse/clickhouse-server@sha256:1f7cd090d5c4e2b8bfe0ea5d8ae6125937e1d932c6371b4d25fbd6088829dc9c
uname -a > /opt/oa200/results/uname.txt
lscpu -J > /opt/oa200/results/lscpu.json
lsblk -J -b -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS > /opt/oa200/results/lsblk.json
date -u +%FT%TZ > /opt/oa200/results/bootstrap-ready.txt
