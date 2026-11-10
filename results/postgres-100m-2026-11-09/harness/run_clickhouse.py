"""Matched local ClickHouse reference, sequential afterPG, same16CPU/32GiBcaps."""
from pathlib import Path
import hashlib,json,statistics,subprocess,time,uuid,threading,shutil
import psutil
from pg_helpers import HERE,dump
from benchmark_helpers import summarize_monitor
from tier_sql import queries,canonical_rows
NAME='openalex-ch100-bench-20261109'
IMAGE='clickhouse/clickhouse-server@sha256:1f7cd090d5c4e2b8bfe0ea5d8ae6125937e1d932c6371b4d25fbd6088829dc9c'
ROOT=Path('/Users/yorrickjansen/work/openalex/.claude/worktrees/postgres-scaling')
FOLDER=HERE/'results/clickhouse';FOLDER.mkdir(exist_ok=True)
SETTINGS={'max_threads':16,'max_memory_usage':24*(1<<30),'max_execution_time':300,'count_distinct_implementation':'uniqExact','max_bytes_before_external_group_by':4*(1<<30),'max_bytes_before_external_sort':4*(1<<30),'join_algorithm':'hash','log_query_settings':1}

def read(p):return json.loads(p.read_text())
def docker(args,**kw):return subprocess.run(['docker',*args],capture_output=True,text=True,check=True,**kw)
def command(sql,fmt='JSONEachRow',qid=None,settings=None):
 args=['docker','exec','-i',NAME,'clickhouse-client','--database=openalex_spike','--format='+fmt]
 if qid:args+=['--query_id='+qid]
 for k,v in (settings or {}).items():args+=['--'+k+'='+str(v)]
 return args

def query(sql,fmt='JSONEachRow',settings=None,qid=None):
 r=subprocess.run(command(sql,fmt,qid,settings),input=sql,text=True,capture_output=True,check=True)
 return [json.loads(x) for x in r.stdout.splitlines() if x.strip()] if fmt=='JSONEachRow' else r.stdout
class Monitor:
 def __init__(self):self.samples=[];self.event=threading.Event()
 def sample(self):
  import pg_helpers
  old=pg_helpers.NAME;pg_helpers.NAME=NAME
  try:return pg_helpers.cg()
  finally:pg_helpers.NAME=old
 def start(self):self.samples=[self.sample()];self.thread=threading.Thread(target=self.loop,daemon=True);self.thread.start();return self
 def loop(self):
  while not self.event.wait(.5):
   try:self.samples.append(self.sample())
   except Exception as e:self.samples.append({'at':time.monotonic(),'error':str(e)})
 def stop(self):self.event.set();self.thread.join();self.samples.append(self.sample());return self.samples

def measure(label,sql,settings,output=False):
 qid='oapg100-'+label+'-'+uuid.uuid4().hex
 m=Monitor().start();st=time.monotonic();before=psutil.disk_io_counters()._asdict()
 try:r=subprocess.run(command(sql,'JSONEachRow' if output else 'Null',qid,settings),input=sql,text=True,capture_output=True,timeout=360)
 except subprocess.TimeoutExpired:
  query("KILL QUERY WHERE query_id='"+qid+"' SYNC",fmt='TabSeparatedRaw');r=subprocess.CompletedProcess([],124,'','Clientdeadline360s; ownedquerykilled')
 finally:xs=m.stop()
 elapsed=time.monotonic()-st;query('SYSTEM FLUSH LOGS',fmt='TabSeparatedRaw')
 stats=query("SELECT type,query_duration_ms/1000.0 AS seconds,read_rows,read_bytes,result_rows,memory_usage AS peak_memory_bytes,ProfileEvents,Settings,exception_code,exception FROM system.query_log WHERE query_id='"+qid+"' AND type IN ('QueryFinish','ExceptionWhileProcessing','ExceptionBeforeStart') ORDER BY event_time_microseconds DESC LIMIT 1")
 assert len(stats)==1
 rec={'query_id':qid,'state':'complete' if r.returncode==0 else 'failed','client_seconds':elapsed,'query_log':stats[0],'requested_settings':settings,'resources':summarize_monitor(xs),'host_disk_before':before,'host_disk_after':psutil.disk_io_counters()._asdict(),'output_format':'JSONEachRow' if output else 'Null','error':r.stderr[-4000:] if r.returncode else None}
 dump(FOLDER/(label+'-telemetry.json'),xs);dump(FOLDER/(label+'-execution.json'),rec)
 rows=[json.loads(line) for line in r.stdout.splitlines() if line.strip()] if output and r.returncode==0 else []
 return rows,rec

def main():
 assert (HERE/'postgres-cases.json').exists(),'PGnotfinished'
 assert (HERE/'results/projection-complete.json').exists()
 required_start_gib=55 if (FOLDER/'storage-before-queries.json').exists() else 75
 assert shutil.disk_usage(HERE).free>required_start_gib*(1<<30),'CHworkspacepreflight:40GiBreserveplusremainingallocatedphaseworkspace'
 pg=json.loads(docker(['inspect','openalex-pg-bench-20261108']).stdout)[0];assert not pg['State']['Running'],'Never overlapenginebenchmarks'
 data=HERE/'chdata';data.mkdir(exist_ok=True);config=HERE/'chconfig';config.mkdir(exist_ok=True)
 (config/'benchmark.xml').write_text('<clickhouse><user_files_path>/input/</user_files_path><query_log replace="1"><database>system</database><table>query_log</table><flush_interval_milliseconds>1000</flush_interval_milliseconds></query_log></clickhouse>\n')
 exists=subprocess.run(['docker','inspect',NAME],capture_output=True,text=True)
 if exists.returncode:
  docker(['run','-d','--name',NAME,'--label','openalex.study=postgres-100m-20261109','--network','none','--cpus','16','--memory','32g','--memory-swap','32g','--ulimit','nofile=262144:262144','-e','CLICKHOUSE_SKIP_USER_SETUP=1','-e','CLICKHOUSE_DO_NOT_CHOWN=1','-v',str(HERE/'projected')+':/input:ro','-v',str(data)+':/var/lib/clickhouse','-v',str(config)+':/etc/clickhouse-server/config.d:ro',IMAGE])
 else:
  owned=json.loads(exists.stdout)[0];assert owned['Config']['Labels'].get('openalex.study')=='postgres-100m-20261109'
  if not owned['State']['Running']:docker(['start',NAME])
 host=json.loads(docker(['inspect',NAME]).stdout)[0]['Config']['Hostname']
 docker(['exec','-i',NAME,'sh','-c','cat >> /etc/hosts'],input='127.0.0.1 '+host+'\n')
 for _ in range(90):
  r=subprocess.run(['docker','exec',NAME,'clickhouse-client','--query','SELECT 1'],capture_output=True,text=True)
  if r.returncode==0:break
  time.sleep(1)
 else:raise RuntimeError('CHnotready')
 dump(FOLDER/'container.json',json.loads(docker(['inspect',NAME]).stdout)[0]);docker(['exec','-i',NAME,'clickhouse-client','--multiquery'],input='CREATE DATABASE IF NOT EXISTS openalex_spike;')
 if not (FOLDER/'schema-created.json').exists():
  sql=(ROOT/'sql/00_schema.sql').read_text()
  sql=sql.replace('institution_type LowCardinality(String)','institution_type LowCardinality(Nullable(String))')
  start=sql.index('CREATE TABLE openalex_spike.sources');end=sql.index('CREATE TABLE openalex_spike.topics')
  block=sql[start:end].replace('display_name String','display_name Nullable(String)').replace('source_type LowCardinality(String)','source_type LowCardinality(Nullable(String))');sql=sql[:start]+block+sql[end:]
  (HERE/'sql/clickhouse-schema.sql').write_text(sql)
  docker(['exec','-i',NAME,'clickhouse-client','--multiquery'],input=sql);dump(FOLDER/'schema-created.json',{'sql_sha256':hashlib.sha256(sql.encode()).hexdigest(),'at':time.time()})
 for t in ['authors','institutions','sources','topics','works','work_author','work_institution','work_topic','citation_edge']:
  query('ALTER TABLE '+t+' MODIFY SETTING old_parts_lifetime=0',fmt='TabSeparatedRaw')
  proof=HERE/'results'/('project-'+t+'.json');source=read(proof);out=FOLDER/('load-'+t+'.json')
  if out.exists() and read(out).get('state')=='complete':continue
  assert int(query('SELECT count() AS n FROM '+t)[0]['n'])==0
  st=time.monotonic();m=Monitor().start()
  sql='INSERT INTO '+t+" SELECT * FROM file('"+t+".parquet',Parquet)"
  try:query(sql,fmt='TabSeparatedRaw',settings=SETTINGS)
  finally:xs=m.stop()
  n=int(query('SELECT count() AS n FROM '+t)[0]['n']);assert n==source['rows']
  dump(FOLDER/('load-'+t+'-telemetry.json'),xs);dump(out,{'state':'complete','rows':n,'seconds':time.monotonic()-st,'sql':sql,'source_sha256':source['sha256'],'resources':summarize_monitor(xs)});print('CHloaded',t,n,flush=True)
 if not (FOLDER/'reverse-projection.json').exists():
  sql=(ROOT/'sql/30_reverse_projection.sql').read_text();st=time.monotonic();docker(['exec','-i',NAME,'clickhouse-client','--multiquery'],input=sql);dump(FOLDER/'reverse-projection.json',{'sql':sql,'seconds':time.monotonic()-st})
 if not (FOLDER/'storage-before-queries.json').exists():
  # Finishall backgroundmerges beforetiming. Logactualpartstorage andheapcomparisonlimits.
  for t in ['authors','institutions','sources','topics','works','work_author','work_institution','work_topic','citation_edge']:query('OPTIMIZE TABLE '+t+' FINAL',fmt='TabSeparatedRaw',settings=dict(SETTINGS,max_execution_time=1800))
  for _ in range(120):
   if int(query('SELECT count() AS n FROM system.merges')[0]['n'])==0:break
   time.sleep(1)
  assert int(query('SELECT count() AS n FROM system.merges')[0]['n'])==0
  for _ in range(180):
   if int(query("SELECT count() AS n FROM system.parts WHERE database='openalex_spike' AND NOT active")[0]['n'])==0:break
   time.sleep(1)
  assert int(query("SELECT count() AS n FROM system.parts WHERE database='openalex_spike' AND NOT active")[0]['n'])==0,'Inactivepartsstilloccupyworkspace'
  dump(FOLDER/'storage-before-queries.json',query("SELECT table,sum(rows) AS rows,sum(bytes_on_disk) AS bytes_on_disk,sum(data_compressed_bytes) AS data_compressed_bytes,sum(data_uncompressed_bytes) AS data_uncompressed_bytes FROM system.parts WHERE active AND database='openalex_spike' GROUP BY table ORDER BY table"))
 catalog={}
 for seed in [51557542,24222542,2003585639]:
  for n,s in queries(seed).items():catalog[n+('-s'+str(seed) if n in ('q05','q06') else '')]=s
 oracle=read(HERE/'athena-cases.json');cases={}
 for name,sql in catalog.items():
  out=FOLDER/(name+'.json')
  if out.exists() and read(out).get('state') in ('complete','failed'):cases[name]=read(out);continue
  # Explicitaliaseskeeptypedresultcolumnsindependentofengine'sdefaultjoinedlabels.
  if name=='q02':sql=sql.replace('SELECT w.publication_year, t.topic_id, t.display_name,','SELECT w.publication_year AS publication_year, t.topic_id AS topic_id, t.display_name AS display_name,')
  if name=='q03':sql=sql.replace('SELECT a.author_id, a.display_name,','SELECT a.author_id AS author_id, a.display_name AS display_name,')
  settings=dict(SETTINGS)
  if name=='q02':
   sql=Path('/Users/yorrickjansen/work/data/openalex-tier-scaling-20261106/q02_preaggregate_topic_names.sql').read_text().replace('openalex_spike.','').replace('AS `t.topic_id`','AS topic_id')
   settings['distributed_aggregation_memory_efficient']=1
  effective=query("SELECT name,value,changed FROM system.settings WHERE name IN ("+','.join("'"+k+"'" for k in settings)+")",settings=settings)
  dump(FOLDER/(name+'-effective-settings.json'),effective)
  rec={'name':name,'state':'running','sql':sql,'sql_sha256':hashlib.sha256(sql.encode()).hexdigest(),'runs':[],'requested_settings':settings};dump(out,rec);(HERE/'sql'/('clickhouse-'+name+'.sql')).write_text(sql+';\n')
  for i in range(4):
   _,run=measure(name+'-'+str(i),sql,settings);run['kind']='primer' if i==0 else 'warm'+str(i);rec['runs'].append(run);dump(out,rec);print(name,run['kind'],run['state'],run['query_log']['seconds'],flush=True)
   if run['state']!='complete':rec['state']='failed';break
  if rec['state']=='failed':dump(out,rec);cases[name]=rec;continue
  rows,qa_run=measure(name+'-qa',sql,settings,output=True)
  if qa_run['state']!='complete':rec.update(state='failed',qa_execution=qa_run);dump(out,rec);cases[name]=rec;continue
  canon=canonical_rows(name[:3],rows);h=hashlib.sha256('\n'.join(canon).encode()).hexdigest();expected=oracle.get(name,{}).get('reference') or (oracle.get(name,{}).get('runs') or [None])[0];qa={'rows':len(rows),'canonical_sha256':h}
  if expected:qa.update(matched=h==expected['canonical_sha256'] and len(rows)==expected['rows'],expected_sha256=expected['canonical_sha256'],expected_rows=expected['rows'])
  rec.update(state='complete',qa=qa,qa_execution=qa_run,warm_seconds=[r['query_log']['seconds'] for r in rec['runs'][1:]]);rec['median_seconds']=statistics.median(rec['warm_seconds']);dump(out,rec);cases[name]=rec
  if expected:assert qa['matched'],name
 dump(HERE/'clickhouse-cases.json',cases);docker(['stop',NAME]);dump(FOLDER/'stopped.json',{'at':time.time(),'data_retained':str(data)})

if __name__=='__main__':main()
