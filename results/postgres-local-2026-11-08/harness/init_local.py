from pathlib import Path
import json,secrets,os,subprocess,platform,datetime
p=Path(__file__).resolve().parent
for n in ('pgdata','temp','secrets','results','sql'): (p/n).mkdir(exist_ok=True)
pw=p/'secrets/password'
if not pw.exists():pw.write_text(secrets.token_urlsafe(36));pw.chmod(0o600)
cmd=['docker','run','-d','--name','openalex-pg-bench-20261108','--label','project=openalex','--label','experiment=postgres-local-20261108','--cpus','16','--memory','32g','--memory-swap','32g','--shm-size','8g','-p','127.0.0.1:15432:5432','--mount',f'type=bind,src={p}/pgdata,dst=/var/lib/postgresql','--mount',f'type=bind,src={pw},dst=/run/secrets/postgres_password,readonly','-e','POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password','-e','POSTGRES_DB=openalex','-e','POSTGRES_USER=openalex','postgres:18','-c','shared_buffers=8GB','-c','work_mem=128MB','-c','maintenance_work_mem=2GB','-c','max_parallel_workers_per_gather=8','-c','max_parallel_workers=16','-c','max_worker_processes=24','-c','max_parallel_maintenance_workers=4','-c','effective_cache_size=24GB','-c','max_wal_size=4GB','-c','checkpoint_timeout=15min','-c','wal_compression=on','-c','track_io_timing=on','-c','log_checkpoints=on','-c','statement_timeout=300000']
r=subprocess.run(cmd,text=True,capture_output=True,check=True)
(p/'container.json').write_text(json.dumps({'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'name':'openalex-pg-bench-20261108','id':r.stdout.strip(),'command':cmd,'host':platform.platform(),'port':15432,'cpus':16,'memory_gib':32,'data_location':str(p/'pgdata'),'vm_free_bytes_before':8126210048,'host_free_note':'411GiB available before experiment','method':'PostgreSQL stock18.6, logged durable tables, host bind mount due VM space limitation; no other containers modified','user_no_claude_validation':True,'linear_issue':'YOR-68'},indent=2)+'\n')
print('Created dedicated PostgreSQL benchmark container')
