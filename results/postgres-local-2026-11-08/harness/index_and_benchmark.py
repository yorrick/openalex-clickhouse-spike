from pathlib import Path
import json,time,sys,hashlib,statistics,importlib.util,decimal,psutil,psycopg,subprocess
from psycopg.rows import dict_row
from pg_helpers import HERE,connect,dump,Monitor
ROOT=Path('/Users/yorrickjansen/work/openalex');SOURCE=Path('/Users/yorrickjansen/work/data/openalex-tier-scaling-20261106')
SPEC=importlib.util.spec_from_file_location('tier_sql',ROOT/'results/aws-scaling-2026-11-06/harness/tier_sql.py');MOD=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(MOD)
INDEXES=[('authors_pk','ALTER TABLE authors ADD CONSTRAINT authors_pk PRIMARY KEY(author_id)'),('institutions_pk','ALTER TABLE institutions ADD CONSTRAINT institutions_pk PRIMARY KEY(institution_id)'),('sources_pk','ALTER TABLE sources ADD CONSTRAINT sources_pk PRIMARY KEY(source_id)'),('topics_pk','ALTER TABLE topics ADD CONSTRAINT topics_pk PRIMARY KEY(topic_id)'),('works_pk','ALTER TABLE works ADD CONSTRAINT works_pk PRIMARY KEY(work_id)'),('works_year_id','CREATE INDEX works_year_id ON works(publication_year,work_id)'),('work_author_author_work','CREATE INDEX work_author_author_work ON work_author(author_id,work_id)'),('work_author_work_author','CREATE INDEX work_author_work_author ON work_author(work_id,author_id)'),('work_institution_institution_work_author','CREATE INDEX work_institution_institution_work_author ON work_institution(institution_id,work_id,author_id)'),('work_institution_work_institution','CREATE INDEX work_institution_work_institution ON work_institution(work_id,institution_id)'),('work_topic_topic_work','CREATE INDEX work_topic_topic_work ON work_topic(topic_id,work_id)'),('work_topic_work_topic','CREATE INDEX work_topic_work_topic ON work_topic(work_id,topic_id)'),('citation_edge_citing_cited','CREATE UNIQUE INDEX citation_edge_citing_cited ON citation_edge(citing_work_id,cited_work_id) INCLUDE(citing_year)'),('citation_edge_cited_citing','CREATE INDEX citation_edge_cited_citing ON citation_edge(cited_work_id,citing_work_id) INCLUDE(citing_year)')]
RUNS={'stage2_small':'oaspike-20261106195056-5ee45f','stage2_medium':'oaspike-20261106201804-2e9d23','stage2_large':'oaspike-20261106204843-b2d12b'}
def snapshot(pg):
 return {'database_bytes':pg.execute("SELECT pg_database_size(current_database())").fetchone()[0],'tables':[dict(zip(('table','rows_estimated','heap_bytes','indexes_bytes','total_bytes'),r)) for r in pg.execute("SELECT c.relname,c.reltuples::bigint,pg_relation_size(c.oid),pg_indexes_size(c.oid),pg_total_relation_size(c.oid) FROM pg_class c JOIN pg_namespace n ON c.relnamespace=n.oid WHERE n.nspname='public' AND c.relkind='r' ORDER BY c.relname").fetchall()],'io_columns':[x.name for x in pg.execute('SELECT * FROM pg_stat_io LIMIT 0').description],'io_rows':pg.execute('SELECT * FROM pg_stat_io').fetchall()}
def summarize_monitor(xs):
 good=[x for x in xs if 'cpu' in x];a,b=good[0],good[-1];dt=b['at']-a['at'];cpu=(b['cpu']['usage_usec']-a['cpu']['usage_usec'])/1e6
 return {'window_seconds':dt,'cpu_seconds':cpu,'average_busy_cores_in_monitor_window':cpu/dt if dt else None,'cpu_throttled_seconds':(b['cpu'].get('throttled_usec',0)-a['cpu'].get('throttled_usec',0))/1e6,'sample_count':len(good),'memory_current_peak_bytes':max(x['memory_current'] for x in good),'memory_anon_peak_bytes':max(x['memory'].get('anon',0) for x in good),'memory_file_peak_bytes':max(x['memory'].get('file',0) for x in good),'memory_shmem_peak_bytes':max(x['memory'].get('shmem',0) for x in good),'scope':'container cgroup over instrumented client window, includes idle background work and monitor overhead; file includes shmem, do not add them; tiny query samples are coarse; VirtioFS host writes may not appear in cgroup block IO'}
def main():
 tier=sys.argv[1] if len(sys.argv)>1 else 'stage2_small';mode=sys.argv[2] if len(sys.argv)>2 else 'all';folder=HERE/'results'/tier;folder.mkdir(exist_ok=True)
 with connect() as pg:
  if mode in ('all','indexes'):
   for name,sql in INDEXES:
    proof=folder/(name+'.json')
    if pg.execute('SELECT to_regclass(%s)',[name]).fetchone()[0]:print('Index exists',name,flush=True);continue
    m=Monitor().start();st=time.monotonic();pg.execute(sql);elapsed=time.monotonic()-st;xs=m.stop();dump(proof,{'sql':sql,'seconds':elapsed,'resources':summarize_monitor(xs)});dump(folder/(name+'-telemetry.json'),xs);print('Index',name,round(elapsed,3),flush=True)
   st=time.monotonic();pg.execute('VACUUM (ANALYZE)');dump(folder/'vacuum-analyze.json',{'seconds':time.monotonic()-st});dump(folder/'storage-before-queries.json',snapshot(pg))
  if mode=='indexes':return
  oracle=json.loads((ROOT/'results/aws-scaling-2026-11-06'/f'{tier}.json').read_text())
  catalog=json.loads((SOURCE/RUNS[tier]/'cloud/queries.json').read_text())
  for name,source_sql in catalog.items():
   output=folder/(name+'.json')
   if output.exists() and json.loads(output.read_text()).get('state')=='complete':continue
   sql=source_sql.replace('openalex_benchmark.','public.').replace('countDistinct(', 'count(DISTINCT ').replace('count()', 'count(*)')
   (HERE/'sql'/f'{name}-postgres.sql').write_text(sql)
   print('Query',name,flush=True);result={'name':name,'tier':tier,'sql':sql,'sql_sha256':hashlib.sha256(sql.encode()).hexdigest(),'state':'running','runs':[]};dump(output,result)
   for i in range(4):
    m=Monitor().start();st=time.monotonic();hd=psutil.disk_io_counters()._asdict()
    try:
     plan=pg.execute('EXPLAIN (ANALYZE, BUFFERS, WAL, SETTINGS, TIMING OFF, FORMAT JSON) '+sql).fetchone()[0][0];elapsed=time.monotonic()-st;xs=m.stop()
     rec={'kind':'primer' if i==0 else f'warm{i}','execution_seconds':plan['Execution Time']/1000,'planning_seconds':plan['Planning Time']/1000,'client_seconds':elapsed,'plan':plan,'resources':summarize_monitor(xs),'host_disk_before':hd,'host_disk_after':psutil.disk_io_counters()._asdict()};result['runs'].append(rec);dump(folder/(name+f'-{i}-telemetry.json'),xs);dump(output,result);print(name,rec['kind'],round(rec['execution_seconds'],6),flush=True)
    except psycopg.errors.QueryCanceled as e:
     xs=m.stop();result.update(state='timeout',timeout_seconds=300,error=str(e),client_seconds_until_cancel=time.monotonic()-st,estimated_plan=pg.execute('EXPLAIN (FORMAT JSON) '+sql).fetchone()[0][0],resources=summarize_monitor(xs));dump(output,result);print(name,'TIMEOUT300s',flush=True);break
    except BaseException:
     m.stop();raise
   if result['state']=='timeout':continue
   st=time.monotonic()
   with pg.cursor(row_factory=dict_row) as cur:cur.execute(sql);rows=cur.fetchall()
   canonical=MOD.canonical_rows(name[:3],rows);digest=hashlib.sha256('\n'.join(canonical).encode()).hexdigest();expected=oracle['cases'][name];match=digest==expected['canonical_result_sha256'] and len(rows)==expected['result_rows'];result['qa']={'matched':match,'rows':len(rows),'expected_rows':expected['result_rows'],'canonical_sha256':digest,'expected_sha256':expected['canonical_result_sha256'],'client_fetch_seconds':time.monotonic()-st};dump(folder/(name+'-canonical.json'),canonical)
   if not match:
    result['state']='mismatch';dump(output,result);raise RuntimeError('Typed multiset mismatch: '+name)
   ts=[x['execution_seconds'] for x in result['runs'] if x['kind']!='primer'];result.update(state='complete',warm_seconds=ts,median_seconds=statistics.median(ts),min_seconds=min(ts),max_seconds=max(ts));dump(output,result);print(name,'QA MATCH',len(rows),'median',round(result['median_seconds'],6),flush=True)
   if name=='q03' and '--bracket-q03' in sys.argv:
    for label,sqlpath in [('q03_preaggregate_authors',HERE/'sql/q03_preaggregate_authors.sql'),('q03_control_b',HERE/'sql/q03-postgres.sql')]:
     subprocess.run([sys.executable,str(HERE/'variant_bench.py'),tier,label,'q03',str(sqlpath)],check=True)
  dump(folder/'storage-after-queries.json',snapshot(pg))
if __name__=='__main__':main()
