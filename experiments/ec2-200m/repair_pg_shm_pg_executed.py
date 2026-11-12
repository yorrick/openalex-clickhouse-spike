"""Bounded PG repair after the paired baseline, without reloading its database."""
import json,time,threading,shutil
from pathlib import Path
import run_engines as e
import helpers as h
from helpers import HERE,dump,docker,connect

def main():
 assert (HERE/'results/engines-complete.json').exists(), 'Finish the sequential baseline first'
 assert not e.owned(e.CH)['State']['Running'], 'Never overlap database engines'
 before=e.owned(e.PG);assert not before['State']['Running']
 assert before['HostConfig']['Memory']==32*2**30 and before['HostConfig']['NanoCpus']==16*10**9
 folder=HERE/'results/postgres'
 baseline=folder/'container-baseline-8g-shm.json'
 if not baseline.exists():dump(baseline,{k:before[k] for k in ['Id','Name','HostConfig','Mounts','State','Image']})
 if before['HostConfig']['ShmSize']!=32*2**30:
  assert before['HostConfig']['ShmSize']==8*2**30
  # Removing a stopped container does not remove the bind-mounted PostgreSQL data.
  docker('rm',e.PG)
 e.start_pg();h.NAME=e.PG
 threading.Thread(target=h.background_guard,daemon=True).start()
 info=e.owned(e.PG);assert info['HostConfig']['ShmSize']==info['HostConfig']['Memory']==info['HostConfig']['MemorySwap']==32*2**30
 assert info['HostConfig']['NanoCpus']==16*10**9
 with connect() as pg:
  indexes=pg.execute("SELECT c.relname,i.indisvalid,i.indisready FROM pg_index i JOIN pg_class c ON c.oid=i.indexrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' ORDER BY c.relname").fetchall()
  expected=json.loads((folder/'prepared.json').read_text())['indexes']
  assert [list(x) for x in indexes]==expected and len(indexes)==14 and all(x[1] and x[2] for x in indexes)
  dump(folder/'shm-repair-preflight.json',{'at':time.time(),'indexes':indexes,'storage':e.pgstorage(pg),'physical_cpu':16,'memory_limit_bytes':32*2**30,'shm_ceiling_bytes':32*2**30,'reason':'Initial parallel hash joins exhausted the separate 8 GiB DSM tmpfs ceiling. Total memory remains 32 GiB. work_mem reduced to 512MB per operation because 2GB x 8 parallel sorts plus shared hash and shared_buffers can exceed the allocation. This is the single bounded profile per affected family.'})
 selected=json.loads((HERE/'results/postgres-cases.json').read_text())
 e.clear_cache()
 for name in ['q02','q03']:
  original=selected[name]
  assert original['state']=='failed' and 'shared memory' in original['error'] and 'No space left' in original['error']
  rec=e.pg_case(name,original['sql'],{'work_mem':'512MB','enable_nestloop':'off'},label=name+'-shm32-work512')
  if rec.get('qa'):
   ch=json.loads((HERE/'results/clickhouse-cases.json').read_text())[name]
   if ch.get('qa'):assert rec['qa']['canonical_sha256']==ch['qa']['canonical_sha256'] and rec['qa']['rows']==ch['qa']['rows']
  selected[name]=rec
  dump(HERE/'results/postgres-selected.json',selected)
 # The initial full-edge aggregation timed out with ~1.03 average busy cores
 # and 19.2 GB of physical writes. Test one streaming grouping profile using
 # the existing cited-work-leading covering index, without adding an index.
 original=selected['q07'];assert original['state']=='timeout'
 sql=original['sql'].replace('GROUP BY citing_year, cited_work_id','GROUP BY cited_work_id, citing_year')
 assert sql!=original['sql']
 settings={'work_mem':'512MB','enable_hashagg':'off'}
 with connect() as pg:
  for k,v in settings.items():pg.execute('SELECT set_config(%s,%s,false)',[k,v])
  plan=pg.execute('EXPLAIN (SETTINGS, FORMAT JSON) '+sql).fetchone()[0]
  dump(folder/'q07-ordered-count-estimated-plan.json',plan)
  temp_before=pg.execute('SELECT temp_bytes,temp_files FROM pg_stat_database WHERE datname=current_database()').fetchone()
 rec=e.pg_case('q07',sql,settings,label='q07-ordered-count')
 if rec.get('qa'):
  ch=json.loads((HERE/'results/clickhouse-cases.json').read_text())['q07']
  if ch.get('qa'):assert rec['qa']['canonical_sha256']==ch['qa']['canonical_sha256'] and rec['qa']['rows']==ch['qa']['rows']
 with connect() as pg:
  temp_after=pg.execute('SELECT temp_bytes,temp_files FROM pg_stat_database WHERE datname=current_database()').fetchone()
  dump(folder/'q07-ordered-count-temp-statistics.json',{'before':temp_before,'after':temp_after,'note':'Database cumulative counters around this profile, not a physical-device byte counter.'})
 selected['q07']=rec;dump(HERE/'results/postgres-selected.json',selected)
 with connect() as pg:dump(folder/'storage-after-repair.json',e.pgstorage(pg))
 docker('stop',e.PG)
 dump(folder/'repair-complete.json',{'at':time.time(),'selected_states':{k:v['state'] for k,v in selected.items()}})

if __name__=='__main__':main()
