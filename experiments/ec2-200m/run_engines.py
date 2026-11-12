from pathlib import Path
import hashlib,json,statistics,subprocess,time,uuid,secrets,threading,shutil,traceback
import psycopg
from psycopg.rows import dict_row
import helpers as h
from helpers import HERE,dump,sha,docker,run,Monitor,summary,connect,guard,duck
from tier_sql import canonical_rows,queries
T=json.loads((HERE/'projection-templates.json').read_text());COUNTS=json.loads((HERE/'results/projection-complete.json').read_text())['counts'] if (HERE/'results/projection-complete.json').exists() else {}
PG='oa200-pg';CH='oa200-ch'
PGIMAGE='postgres@sha256:5a5a84b19854a9ffaa54082c166ff4ec27473a361e496e5ea167f298f2da9722'
CHIMAGE='clickhouse/clickhouse-server@sha256:1f7cd090d5c4e2b8bfe0ea5d8ae6125937e1d932c6371b4d25fbd6088829dc9c'
CHSET={'max_threads':16,'max_memory_usage':24*2**30,'max_execution_time':300,'count_distinct_implementation':'uniqExact','max_bytes_before_external_group_by':4*2**30,'max_bytes_before_external_sort':4*2**30,'join_algorithm':'hash','log_query_settings':1}

def exists(name):return subprocess.run(['docker','inspect',name],capture_output=True,text=True).returncode==0
def owned(name):
 x=json.loads(docker('inspect',name).stdout)[0];assert x['Config']['Labels'].get('openalex.study')=='ec2-200m-20261112'
 expected=HERE/('pgdata' if name==PG else 'chdata');assert any(Path(m['Source']).resolve()==expected.resolve() for m in x['Mounts']), 'Container bind mount belongs to a different phase'
 return x

def start_pg():
 h.NAME=PG;guard();(HERE/'pgdata').mkdir(exist_ok=True);(HERE/'secrets').mkdir(exist_ok=True)
 pw=HERE/'secrets/password'
 if not pw.exists():pw.write_text(secrets.token_urlsafe(32));pw.chmod(0o600)
 if not exists(PG):
  # DSM is charged to the same 32 GiB cgroup limit. The tmpfs ceiling must not
  # independently fail an otherwise memory-accounted parallel hash join.
  docker('run','-d','--name',PG,'--label','openalex.study=ec2-200m-20261112','--cpus','16','--memory','32g','--memory-swap','32g','--shm-size','32g','-p','127.0.0.1:15432:5432','-v',str(HERE/'pgdata')+':/var/lib/postgresql','-v',str(HERE/'secrets')+':/run/secrets:ro','-e','POSTGRES_PASSWORD_FILE=/run/secrets/password','-e','POSTGRES_USER=openalex','-e','POSTGRES_DB=openalex',PGIMAGE,'-c','shared_buffers=8GB','-c','work_mem=128MB','-c','max_parallel_workers_per_gather=8','-c','max_parallel_workers=16','-c','max_worker_processes=32','-c','max_wal_size=4GB','-c','track_io_timing=on')
 elif not owned(PG)['State']['Running']:docker('start',PG)
 for _ in range(120):
  try:
   with connect() as pg:pg.execute('SELECT 1')
   break
  except psycopg.OperationalError:time.sleep(1)
 else:raise RuntimeError('PG did not become ready')
 info=owned(PG);dump(HERE/'results/postgres/container.json',{k:info[k] for k in ['Id','Name','HostConfig','Mounts','State','Image']})

def pgstorage(pg):
 return {'database_bytes':pg.execute('SELECT pg_database_size(current_database())').fetchone()[0],'tables':[dict(zip(['table','rows_estimated','heap_bytes','indexes_bytes','total_bytes'],x)) for x in pg.execute("SELECT c.relname,c.reltuples::bigint,pg_relation_size(c.oid),pg_indexes_size(c.oid),pg_total_relation_size(c.oid) FROM pg_class c JOIN pg_namespace n ON c.relnamespace=n.oid WHERE n.nspname='public' AND c.relkind='r' ORDER BY c.relname")],'settings':dict(pg.execute("SELECT name,setting FROM pg_settings WHERE name IN ('shared_buffers','work_mem','max_parallel_workers_per_gather','max_parallel_workers','max_worker_processes','max_wal_size','fsync','full_page_writes','synchronous_commit','jit','track_io_timing')").fetchall())}

def load_pg():
 start_pg();folder=HERE/'results/postgres';folder.mkdir(exist_ok=True)
 with connect() as pg:pg.execute(T['pg_schema'])
 d=duck('4GB');d.execute('LOAD postgres');password=(HERE/'secrets/password').read_text();d.execute('ATTACH ? AS pg (TYPE postgres)',[f"host=127.0.0.1 port=15432 dbname=openalex user=openalex password={password} options='-c statement_timeout=0'"])
 for t in T['columns']:
  out=folder/('load-'+t+'.json')
  if out.exists():assert json.loads(out.read_text())['state']=='complete';continue
  guard()
  with connect() as pg:assert pg.execute('SELECT count(*) FROM '+t).fetchone()[0]==0
  st=time.monotonic();mon=Monitor().start();sql=f"INSERT INTO pg.public.{t} SELECT * FROM read_parquet('{HERE}/projected/{t}/*.parquet')"
  try:d.execute(sql)
  finally:xs=mon.stop();dump(folder/('load-'+t+'-telemetry.json'),xs)
  seconds=time.monotonic()-st
  with connect() as pg:
   pg.execute("SET statement_timeout='30min'");n=pg.execute('SELECT count(*) FROM '+t).fetchone()[0]
  assert n==COUNTS[t],(t,n,COUNTS[t]);dump(out,{'state':'complete','rows':n,'seconds':seconds,'sql':sql,'resources':summary(xs)});print('PG LOADED',t,n,seconds,flush=True)
 d.close()
 with connect() as pg:
  pg.execute("SET statement_timeout='90min'");pg.execute("SET maintenance_work_mem='8GB'");pg.execute('SET max_parallel_maintenance_workers=8')
  for name,sql in T['indexes']:
   out=folder/('index-'+name+'.json')
   if pg.execute('SELECT to_regclass(%s)',[name]).fetchone()[0]:assert out.exists();continue
   guard();st=time.monotonic();mon=Monitor().start()
   try:pg.execute(sql)
   finally:xs=mon.stop();dump(folder/('index-'+name+'-telemetry.json'),xs)
   dump(out,{'state':'complete','sql':sql,'seconds':time.monotonic()-st,'resources':summary(xs)});print('PG INDEX',name,time.monotonic()-st,flush=True)
  st=time.monotonic();pg.execute('VACUUM (ANALYZE)');dump(folder/'vacuum.json',{'seconds':time.monotonic()-st})
  indexes=pg.execute("SELECT c.relname,i.indisvalid,i.indisready FROM pg_index i JOIN pg_class c ON c.oid=i.indexrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' ORDER BY c.relname").fetchall();assert len(indexes)==14 and all(x[1] and x[2] for x in indexes)
  dump(folder/'prepared.json',{'indexes':indexes,'counts':COUNTS,'storage':pgstorage(pg)})


def pg_case(name,sql,settings,label=None):
 folder=HERE/'results/postgres';label=label or name;out=folder/(label+'.json')
 if out.exists() and json.loads(out.read_text()).get('state') in ['complete','failed','timeout']:return json.loads(out.read_text())
 rec={'name':name,'label':label,'state':'running','sql':sql,'sql_sha256':hashlib.sha256(sql.encode()).hexdigest(),'requested_settings':settings,'runs':[]};dump(out,rec);(HERE/'sql'/('executed-postgres-'+label+'.sql')).write_text(sql)
 with connect() as pg:
  for k,v in settings.items():pg.execute('SELECT set_config(%s,%s,false)',[k,v])
  rec['effective_settings']=dict(pg.execute("SELECT name,setting FROM pg_settings WHERE name=ANY(%s)",[list(settings)+['shared_buffers','max_parallel_workers_per_gather','max_parallel_workers','work_mem','jit','statement_timeout']]).fetchall())
  for i in range(4):
   guard();st=time.monotonic();mon=Monitor().start()
   try:plan=pg.execute('EXPLAIN (ANALYZE, BUFFERS, WAL, SETTINGS, TIMING OFF, FORMAT JSON) '+sql).fetchone()[0][0]
   except Exception as e:
    xs=mon.stop();dump(folder/(label+f'-{i}-telemetry.json'),xs);rec.update(state='timeout' if isinstance(e,psycopg.errors.QueryCanceled) else 'failed',error=str(e),seconds_until_error=time.monotonic()-st,resources=summary(xs));dump(out,rec);print('PG',label,rec['state'],flush=True);return rec
   xs=mon.stop();dump(folder/(label+f'-{i}-telemetry.json'),xs);rec['runs'].append({'kind':'primer' if i==0 else f'warm{i}','execution_seconds':plan['Execution Time']/1000,'planning_seconds':plan['Planning Time']/1000,'client_seconds':time.monotonic()-st,'plan':plan,'resources':summary(xs)});dump(out,rec);print('PG',label,i,plan['Execution Time']/1000,flush=True)
  st=time.monotonic()
  try:
   with pg.cursor(row_factory=dict_row) as c:c.execute(sql);rows=c.fetchall()
  except Exception as e:rec.update(state='qa_failed',error=str(e));dump(out,rec);return rec
  canon=canonical_rows(name[:3],rows);rec['qa']={'rows':len(rows),'canonical_sha256':hashlib.sha256('\n'.join(canon).encode()).hexdigest(),'fetch_seconds':time.monotonic()-st}
  rec.update(state='complete',warm_seconds=[r['execution_seconds'] for r in rec['runs'][1:]]);rec['median_seconds']=statistics.median(rec['warm_seconds']);dump(out,rec);return rec

def bench_pg():
 cases={}
 for name in catalog():
  family=name[:3];filename={'q02':'q02_preaggregate_topic_names.sql','q03':'q03_rank_valid_ids_before_names.sql','q04':'q04_country_pairs.sql'}.get(family,name+'-postgres.sql');sql=(HERE/'sql'/filename).read_text();settings={'work_mem':'2GB','enable_nestloop':'off'} if family in ['q02','q03','q04'] else {'work_mem':'512MB' if family=='q07' else '128MB'}
  cases[name]=pg_case(name,sql,settings)
 with connect() as pg:dump(HERE/'results/postgres/storage-after-queries.json',pgstorage(pg))
 dump(HERE/'results/postgres-cases.json',cases);docker('stop',PG);dump(HERE/'results/postgres/stopped.json',{'at':time.time()})


def chquery(sql,fmt='JSONEachRow',settings=None,qid=None,deadline=2100,database='openalex_spike'):
 args=['docker','exec','-i',CH,'clickhouse-client','--database='+database,'--format='+fmt]
 if qid:args+=['--query_id='+qid]
 args+=['--'+k+'='+str(v) for k,v in (settings or {}).items()]
 r=run(args,input=sql,timeout=deadline)
 return [json.loads(s) for s in r.stdout.splitlines() if s.strip()] if fmt=='JSONEachRow' else r.stdout

def load_ch():
 h.NAME=CH;guard();assert not owned(PG)['State']['Running'];(HERE/'chdata').mkdir(exist_ok=True);conf=HERE/'chconfig';conf.mkdir(exist_ok=True)
 uid=int(docker('run','--rm','--network','none','--entrypoint','id',CHIMAGE,'-u','clickhouse').stdout);gid=int(docker('run','--rm','--network','none','--entrypoint','id',CHIMAGE,'-g','clickhouse').stdout)
 __import__('os').chown(HERE/'chdata',uid,gid)
 dump(HERE/'results/clickhouse/data-directory-owner.json',{'image':CHIMAGE,'uid':uid,'gid':gid,'scope':'Only this study writable CH data directory; source input remains read-only'})
 (conf/'benchmark.xml').write_text('<clickhouse><user_files_path>/input/</user_files_path><query_log replace="1"><database>system</database><table>query_log</table><flush_interval_milliseconds>1000</flush_interval_milliseconds></query_log><logger><level>warning</level></logger></clickhouse>')
 if not exists(CH):docker('run','-d','--name',CH,'--label','openalex.study=ec2-200m-20261112','--network','none','--cpus','16','--memory','32g','--memory-swap','32g','--ulimit','nofile=262144:262144','-e','CLICKHOUSE_SKIP_USER_SETUP=1','-e','CLICKHOUSE_DO_NOT_CHOWN=1','-v',str(HERE/'projected')+':/input:ro','-v',str(HERE/'chdata')+':/var/lib/clickhouse','-v',str(conf)+':/etc/clickhouse-server/config.d:ro',CHIMAGE)
 elif not owned(CH)['State']['Running']:docker('start',CH)
 host=owned(CH)['Config']['Hostname'];docker('exec','-i',CH,'sh','-c','cat >> /etc/hosts',input='127.0.0.1 '+host+'\n')
 for _ in range(120):
  try:chquery('SELECT 1',database='default');break
  except subprocess.CalledProcessError:time.sleep(1)
 else:raise RuntimeError('CH not ready')
 folder=HERE/'results/clickhouse';folder.mkdir(exist_ok=True);info=owned(CH);dump(folder/'container.json',{k:info[k] for k in ['Id','Name','HostConfig','Mounts','State','Image']})
 if not (folder/'schema.json').exists():
  sql=(HERE/'sql/clickhouse-schema.sql').read_text();docker('exec','-i',CH,'clickhouse-client','--multiquery',input=sql)
  chquery('ALTER TABLE citation_edge ADD PROJECTION by_cited (SELECT * ORDER BY (cited_work_id,citing_work_id))',fmt='TabSeparatedRaw')
  dump(folder/'schema.json',{'sha256':hashlib.sha256(sql.encode()).hexdigest(),'reverse_projection_created_before_load':True})
 for t in T['columns']:
  out=folder/('load-'+t+'.json')
  if out.exists():assert json.loads(out.read_text())['state']=='complete';continue
  guard();chquery('ALTER TABLE '+t+' MODIFY SETTING old_parts_lifetime=0',fmt='TabSeparatedRaw');assert int(chquery('SELECT count() AS n FROM '+t)[0]['n'])==0
  st=time.monotonic();mon=Monitor().start();sql='INSERT INTO '+t+" SELECT * FROM file('"+t+"/*.parquet',Parquet)"
  try:chquery(sql,fmt='TabSeparatedRaw',settings=dict(CHSET,max_execution_time=7200),deadline=7300)
  finally:xs=mon.stop();dump(folder/('load-'+t+'-telemetry.json'),xs)
  n=int(chquery('SELECT count() AS n FROM '+t)[0]['n']);assert n==COUNTS[t];dump(out,{'state':'complete','rows':n,'seconds':time.monotonic()-st,'sql':sql,'resources':summary(xs)});print('CH LOADED',t,n,flush=True)
 if not (folder/'prepared.json').exists():
  for t in T['columns']:chquery('OPTIMIZE TABLE '+t+' FINAL',fmt='TabSeparatedRaw',settings=dict(CHSET,max_execution_time=5400),deadline=5500)
  for _ in range(300):
   if int(chquery('SELECT count() AS n FROM system.merges')[0]['n'])==0 and int(chquery("SELECT count() AS n FROM system.parts WHERE database='openalex_spike' AND NOT active")[0]['n'])==0:break
   time.sleep(1)
  else:raise RuntimeError('CH merges or inactive parts remain')
  dump(folder/'prepared.json',{'counts':COUNTS,'storage':chquery("SELECT table,sum(rows) AS rows,sum(bytes_on_disk) AS bytes_on_disk,sum(data_compressed_bytes) AS data_compressed_bytes FROM system.parts WHERE database='openalex_spike' AND active GROUP BY table ORDER BY table"),'projections':chquery("SELECT table,name,sum(rows) AS rows,sum(bytes_on_disk) AS bytes_on_disk FROM system.projection_parts WHERE active GROUP BY table,name")})

def ch_case(name,sql,settings,label=None):
 folder=HERE/'results/clickhouse';label=label or name;out=folder/(label+'.json')
 if out.exists() and json.loads(out.read_text()).get('state') in ['complete','failed','timeout']:return json.loads(out.read_text())
 rec={'name':name,'label':label,'state':'running','sql':sql,'sql_sha256':hashlib.sha256(sql.encode()).hexdigest(),'requested_settings':settings,'runs':[]};dump(out,rec);(HERE/'sql'/('executed-clickhouse-'+label+'.sql')).write_text(sql)
 for i in range(5):
  guard();qid='oa200-'+label+'-'+uuid.uuid4().hex;mon=Monitor().start();st=time.monotonic();rows=[];error=None
  try:rows=chquery(sql,fmt='JSONEachRow' if i==4 else 'Null',settings=settings,qid=qid,deadline=360)
  except subprocess.TimeoutExpired:
   chquery("KILL QUERY WHERE query_id='"+qid+"' SYNC",fmt='TabSeparatedRaw');error='Client deadline 360s, owned query killed'
  except subprocess.CalledProcessError as e:error=e.stderr[-4000:]
  finally:xs=mon.stop();dump(folder/(label+f'-{i}-telemetry.json'),xs)
  chquery('SYSTEM FLUSH LOGS',fmt='TabSeparatedRaw');stats=chquery("SELECT type,query_duration_ms/1000.0 AS seconds,read_rows,read_bytes,result_rows,memory_usage AS peak_memory_bytes,ProfileEvents,Settings,exception_code,exception FROM system.query_log WHERE query_id='"+qid+"' AND type IN ('QueryFinish','ExceptionWhileProcessing','ExceptionBeforeStart') ORDER BY event_time_microseconds DESC LIMIT 1")
  r={'query_id':qid,'kind':'qa' if i==4 else 'primer' if i==0 else f'warm{i}','client_seconds':time.monotonic()-st,'query_log':stats[0] if stats else None,'resources':summary(xs),'error':error}
  if i<4:rec['runs'].append(r)
  else:rec['qa_execution']=r
  if error:rec.update(state='failed',error=error);dump(out,rec);print('CH',label,'FAILED',error,flush=True);return rec
  assert stats and stats[0]['type']=='QueryFinish';dump(out,rec);print('CH',label,i,stats[0]['seconds'],flush=True)
  if i==4:
   canon=canonical_rows(name[:3],rows);rec['qa']={'rows':len(rows),'canonical_sha256':hashlib.sha256('\n'.join(canon).encode()).hexdigest()}
 rec.update(state='complete',warm_seconds=[r['query_log']['seconds'] for r in rec['runs'][1:]]);rec['median_seconds']=statistics.median(rec['warm_seconds']);dump(out,rec);return rec

def catalog():
 out={}
 for seed in [51557542,24222542,2003585639]:
  for name,sql in queries(seed).items():out[name+('-s'+str(seed) if name in ['q05','q06'] else '')]=sql
 return out

def bench_ch():
 cases={}
 for name,defaultsql in catalog().items():
  family=name[:3]
  if family=='q03':sql=(HERE/'sql/clickhouse-q03_numeric_top_ids.sql').read_text()
  elif family in ['q01','q02','q04','q07']:sql=(HERE/'sql'/('clickhouse-'+family+'.sql')).read_text()
  else:sql=defaultsql
  cases[name]=ch_case(name,sql,CHSET)
 dump(HERE/'results/clickhouse-cases.json',cases);docker('stop',CH);dump(HERE/'results/clickhouse/stopped.json',{'at':time.time()})

def clear_cache():
 run(['sync']);Path('/proc/sys/vm/drop_caches').write_text('3\n')

def main():
 global COUNTS
 COUNTS=json.loads((HERE/'results/projection-complete.json').read_text())['counts']
 if HERE.name!='smoke' and not (HERE/'results/normalization-sample-qa.json').exists():run([__import__('sys').executable,str(HERE/'verify_normalization.py')],timeout=600)
 threading.Thread(target=h.background_guard,daemon=True).start()
 load_pg();clear_cache();bench_pg();clear_cache();load_ch();clear_cache();bench_ch()
 pg=json.loads((HERE/'results/postgres-cases.json').read_text());ch=json.loads((HERE/'results/clickhouse-cases.json').read_text());qa={}
 for name in catalog():
  a=pg.get(name,{});b=ch.get(name,{});qa[name]={'pg':a.get('state'),'ch':b.get('state'),'matched':None}
  if a.get('qa') and b.get('qa'):qa[name]['matched']=a['qa']['canonical_sha256']==b['qa']['canonical_sha256'] and a['qa']['rows']==b['qa']['rows']
 dump(HERE/'results/engine-comparison.json',qa);assert all(x['matched'] is not False for x in qa.values())
 dump(HERE/'results/engines-complete.json',{'at':time.time(),'qa':qa})
if __name__=='__main__':
 try:main()
 except BaseException as e:
  # Never emit the PG credential in evidence.
  password=(HERE/'secrets/password').read_text() if (HERE/'secrets/password').exists() else 'NO_PASSWORD_CREATED'
  error=traceback.format_exc().replace(password,'[REDACTED]');dump(HERE/'results/engine-error.json',{'at':time.time(),'error':error});print(error,flush=True);raise SystemExit(1)
