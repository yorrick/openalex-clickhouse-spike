"""Sequential100m PostgreSQL load and measurement, same retained schema/resources."""
from pathlib import Path
import hashlib,json,statistics,sys,time,shutil,subprocess
import psutil,psycopg
from psycopg.rows import dict_row
from pg_helpers import HERE,connect,duck,dump,Monitor,NAME
from benchmark_helpers import INDEXES,snapshot,summarize_monitor
from tier_sql import canonical_rows,queries
TABLES=['works','work_author','work_institution','work_topic','citation_edge']
FOLDER=HERE/'results/postgres'
FOLDER.mkdir(exist_ok=True)

def read(p): return json.loads(Path(p).read_text())
def guard():
 if shutil.disk_usage(HERE).free < 80*(1<<30): raise RuntimeError('Host free disk below80GiB guard')
def wait_proof(table):
 p=HERE/'results'/('project-'+table+'.json')
 while not p.exists() or read(p).get('state')!='complete':
  if not psutil.pid_exists(30968): raise RuntimeError('Projector ended before '+table+' completed')
  time.sleep(10)
 proof=read(p); assert proof['table']==table and proof['rows']>0
 return proof

def load():
 # Wait for a fully sealed base file before replacing the archived32m database.
 wait_proof('works')
 with connect() as pg:
  if not (FOLDER/'reset.json').exists():
   assert pg.execute('SELECT count(*) FROM works').fetchone()[0]==31885241
   assert pg.execute('SELECT count(*) FROM authors').fetchone()[0]==119129660
   dump(FOLDER/'storage-before-reset.json',snapshot(pg))
   pg.execute("SET statement_timeout='30min'")
   pg.execute('ALTER TABLE works DROP CONSTRAINT works_pk')
   for name,_ in INDEXES[5:]: pg.execute('DROP INDEX '+name)
   pg.execute('TRUNCATE '+','.join(TABLES))
   dump(FOLDER/'reset.json',{'at':time.time(),'old_works':31885241,'retained_authors':119129660,'only_truncated':TABLES,'dropped_indexes':[x[0] for x in INDEXES[4:]]})
 d=duck()
 for table in TABLES:
  proof=wait_proof(table); guard(); out=FOLDER/('load-'+table+'.json')
  if out.exists() and read(out).get('state')=='complete': continue
  with connect() as pg: assert pg.execute('SELECT count(*) FROM '+table).fetchone()[0]==0
  path=HERE/'projected'/(table+'.parquet')
  assert path.stat().st_size==proof['bytes']
  sql='INSERT INTO pg.public.'+table+' SELECT * FROM read_parquet('+"'"+str(path).replace("'","''")+"')"
  (HERE/'sql'/('load-'+table+'.sql')).write_text(sql+';\n')
  rec={'state':'running','table':table,'input_sha256':proof['sha256'],'sql':sql,'at':time.time()}; dump(out,rec)
  m=Monitor().start(); st=time.monotonic(); before=psutil.disk_io_counters()._asdict()
  try:
   d.execute(sql); elapsed=time.monotonic()-st
   xs=m.stop()
   with connect() as pg:
    pg.execute("SET statement_timeout='30min'")
    n=pg.execute('SELECT count(*) FROM '+table).fetchone()[0]
    heap=pg.execute('SELECT pg_relation_size(%s)',[table]).fetchone()[0]
   assert n==proof['rows'],(table,n,proof['rows'])
   rec.update(state='complete',rows=n,seconds=elapsed,heap_bytes=heap,resources=summarize_monitor(xs),host_io_before=before,host_io_after=psutil.disk_io_counters()._asdict(),host_free_after=shutil.disk_usage(HERE).free)
  except BaseException as e:
   xs=m.stop(); rec.update(state='failed',error=(type(e).__name__+':'+str(e)).replace((HERE/'secrets/password').read_text(),'[REDACTED]'))
   dump(out,rec);dump(FOLDER/('load-'+table+'-telemetry.json'),xs);raise
  dump(FOLDER/('load-'+table+'-telemetry.json'),xs);dump(out,rec);print('Loaded',table,n,round(elapsed,3),'seconds',flush=True)
 d.close()
 with connect() as pg:
  pg.execute("SET statement_timeout='30min'")
  pg.execute("SET maintenance_work_mem='8GB'")
  pg.execute('SET max_parallel_maintenance_workers=8')
  dump(FOLDER/'maintenance-settings.json',dict(pg.execute("SELECT name,setting FROM pg_settings WHERE name IN ('statement_timeout','maintenance_work_mem','max_parallel_maintenance_workers','shared_buffers')").fetchall()))
  for name,sql in INDEXES[4:]:
   guard();out=FOLDER/('index-'+name+'.json')
   exists=pg.execute('SELECT to_regclass(%s)',[name]).fetchone()[0]
   if exists:
    assert out.exists() and read(out)['state']=='complete';continue
   print('Building',name,flush=True);m=Monitor().start();st=time.monotonic()
   try:pg.execute(sql)
   finally:xs=m.stop();dump(FOLDER/('index-'+name+'-telemetry.json'),xs)
   dump(out,{'state':'complete','sql':sql,'seconds':time.monotonic()-st,'resources':summarize_monitor(xs)})
  print('Vacuum analyze',flush=True);st=time.monotonic();pg.execute('VACUUM (ANALYZE)');dump(FOLDER/'vacuum.json',{'seconds':time.monotonic()-st})
  ix=pg.execute("SELECT c.relname,i.indisvalid,i.indisready FROM pg_index i JOIN pg_class c ON c.oid=i.indexrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' ORDER BY c.relname").fetchall()
  assert len(ix)==14 and all(x[1] and x[2] for x in ix)
  counts={t:pg.execute('SELECT count(*) FROM '+t).fetchone()[0] for t in TABLES+['authors','institutions','sources','topics']}
  assert counts['works']==100087422 and counts['authors']==119129660
  dump(FOLDER/'load-validation.json',{'all14valid_ready':True,'indexes':ix,'counts':counts,'storage':snapshot(pg)})
 print('POSTGRES READY',flush=True)

def one(name,sql,settings,oracle,label=None):
 guard();label=label or name;out=FOLDER/(label+'.json')
 if out.exists() and read(out).get('state') in ('complete','timeout','failed'):return read(out)
 rec={'name':name,'label':label,'state':'running','sql':sql,'sql_sha256':hashlib.sha256(sql.encode()).hexdigest(),'requested_settings':settings,'runs':[]};dump(out,rec)
 with connect() as pg:
  assert pg.execute('SHOW statement_timeout').fetchone()[0]=='5min'
  for k,v in settings.items(): pg.execute('SELECT set_config(%s,%s,false)',[k,v])
  rec['effective_settings']=dict(pg.execute("SELECT name,setting FROM pg_settings WHERE name=ANY(%s)",[list(settings)+['shared_buffers','max_parallel_workers_per_gather','max_parallel_workers','work_mem','jit']]).fetchall())
  for i in range(4):
   guard();m=Monitor().start();st=time.monotonic();before=psutil.disk_io_counters()._asdict()
   try:
    plan=pg.execute('EXPLAIN (ANALYZE, BUFFERS, WAL, SETTINGS, TIMING OFF, FORMAT JSON) '+sql).fetchone()[0][0]
    client=time.monotonic()-st;xs=m.stop()
   except BaseException as e:
    xs=m.stop();rec.update(state='timeout' if isinstance(e,psycopg.errors.QueryCanceled) else 'failed',error=(type(e).__name__+':'+str(e)).replace((HERE/'secrets/password').read_text(),'[REDACTED]'),client_seconds_until_error=time.monotonic()-st,resources=summarize_monitor(xs))
    dump(FOLDER/(label+f'-{i}-telemetry.json'),xs);dump(out,rec);print(label,rec['state'],flush=True);return rec
   rec['runs'].append({'kind':'primer' if i==0 else f'warm{i}','execution_seconds':plan['Execution Time']/1000,'planning_seconds':plan['Planning Time']/1000,'client_seconds':client,'plan':plan,'resources':summarize_monitor(xs),'host_disk_before':before,'host_disk_after':psutil.disk_io_counters()._asdict()})
   dump(FOLDER/(label+f'-{i}-telemetry.json'),xs);dump(out,rec);print(label,rec['runs'][-1]['kind'],rec['runs'][-1]['execution_seconds'],flush=True)
  st=time.monotonic()
  with pg.cursor(row_factory=dict_row) as c:c.execute(sql);rows=c.fetchall()
  canon=canonical_rows(name[:3],rows);h=hashlib.sha256('\n'.join(canon).encode()).hexdigest()
  expected=oracle.get('reference') or (oracle['runs'][0] if oracle.get('runs') else None)
  qa={'rows':len(rows),'canonical_sha256':h,'fetch_seconds':time.monotonic()-st,'independent_reference_available':expected is not None}
  if expected:qa.update(matched=(h==expected['canonical_sha256'] and len(rows)==expected['rows']),expected_sha256=expected['canonical_sha256'],expected_rows=expected['rows'])
  rec['qa']=qa
  if expected and not qa['matched']: rec['state']='mismatch';dump(out,rec);raise RuntimeError('Typed output mismatch:'+name)
  times=[x['execution_seconds'] for x in rec['runs'][1:]]
  rec.update(state='complete',warm_seconds=times,median_seconds=statistics.median(times));dump(out,rec);print(label,'median',rec['median_seconds'],'QA',qa.get('matched','unavailable'),flush=True)
 return rec

def bench():
 assert (FOLDER/'load-validation.json').exists()
 # Avoid contending with input projection or another local engine during timed queries.
 while not (HERE/'results/projection-complete.json').exists():time.sleep(10)
 oracle_path=HERE/'athena-cases.json'
 catalog={}
 for seed in [51557542,24222542,2003585639]:
  for name,sql in queries(seed).items():catalog[name+('-s'+str(seed) if name in ('q05','q06') else '')]=sql
 cases={}
 for name in catalog:
  sql=(HERE/'sql'/('q03_preaggregate_authors.sql' if name=='q03' else name+'-postgres.sql')).read_text()
  settings={'work_mem':'512MB'} if name[:3] in ('q02','q03','q04','q07') else {}
  if name=='q03':settings['enable_nestloop']='off'
  oracle=read(oracle_path).get(name,{}) if oracle_path.exists() else {}
  cases[name]=one(name,sql,settings,oracle)
 with connect() as pg:dump(FOLDER/'storage-after-queries.json',snapshot(pg))
 dump(HERE/'postgres-cases.json',cases)
 summary={}
 for family in ['q01','q02','q03','q04','q05','q06','q07']:
  group=[v for n,v in cases.items() if n[:3]==family]
  summary[family]={'median_seconds':max(v['median_seconds'] for v in group) if all(v['state']=='complete' for v in group) else None,'all_qa_match':all(v.get('qa',{}).get('matched',False) for v in group),'cases':{v['name']:v['state'] for v in group}}
 failed=[n for n,v in summary.items() if v['median_seconds'] is None or v['median_seconds']>=60]
 dump(HERE/'postgres-decision-initial.json',{'families':summary,'missed_60_seconds':failed,'volume_growth_stopped_pending_one_bounded_trial':bool(failed)})
 print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':
 if len(sys.argv)==1 or sys.argv[1]=='load':load()
 if len(sys.argv)==1 or sys.argv[1]=='bench':bench()
