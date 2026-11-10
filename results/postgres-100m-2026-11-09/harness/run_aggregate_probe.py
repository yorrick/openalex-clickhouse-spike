"""Measure4aggregatefamiliesat100musingtheircompleteindexes;citationindexesnotrequired."""
from pathlib import Path
import json,time
from pg_helpers import HERE,connect,dump,Monitor
from benchmark_helpers import snapshot,summarize_monitor
from run_postgres import one

def read(p):return json.loads(p.read_text())
def main():
 folder=HERE/'results/postgres';prep=folder/'aggregate-preparation.json'
 if not prep.exists():
  with connect() as pg:
   pg.execute("SET statement_timeout='30min'");pg.execute("SET maintenance_work_mem='8GB'");pg.execute('SET max_parallel_maintenance_workers=8')
   pg.execute('ALTER TABLE citation_edge SET (autovacuum_enabled=false)')
   cancelled=pg.execute("SELECT pid,pg_cancel_backend(pid) FROM pg_stat_activity WHERE backend_type='autovacuum worker' AND query LIKE 'autovacuum: VACUUM%public.citation_edge'").fetchall()
   times={}
   for t in ['works','work_author','work_institution','work_topic','authors','institutions','sources','topics']:
    st=time.monotonic();m=Monitor().start()
    try:pg.execute('VACUUM (ANALYZE) '+t)
    finally:xs=m.stop();dump(folder/('vacuum-'+t+'-telemetry.json'),xs)
    times[t]={'seconds':time.monotonic()-st,'resources':summarize_monitor(xs)};print('Prepared',t,round(times[t]['seconds'],2),flush=True)
   indexes=pg.execute("SELECT c.relname,i.indisvalid,i.indisready FROM pg_index i JOIN pg_class c ON c.oid=i.indexrelid WHERE c.relnamespace='public'::regnamespace ORDER BY c.relname").fetchall();assert len(indexes)==12 and all(v and r for _,v,r in indexes)
   counts={t:read(folder/('load-'+t+'.json'))['rows'] for t in ['works','work_author','work_institution','work_topic','citation_edge']}
   for t in ['authors','institutions','sources','topics']:counts[t]=pg.execute('SELECT count(*) FROM '+t).fetchone()[0]
   assert counts['works']==100087422 and counts['citation_edge']==622671173 and counts['authors']==119129660
   dump(prep,{'at':time.time(),'counts':counts,'vacuum':times,'indexes':indexes,'all12valid_ready':True,'citation_index_creation_aborted_by_80GiB_guard':True,'citation_autovacuum_paused_for_aggregate_measurements':True,'cancelled_citation_autovacuum':cancelled,'storage':snapshot(pg),'scope':'q01-q04usealltheirsameindexes;citation_edgeisnotreferencedbythesefamilies'})
 print('AGGREGATEQUERIESREADY',flush=True);cases={}
 for name in ['q01','q02','q03','q04']:
  path=HERE/'sql'/('q03_preaggregate_authors.sql' if name=='q03' else name+'-postgres.sql');sql=path.read_text();assert 'citation_edge' not in sql.lower()
  settings={'work_mem':'512MB'} if name!='q01' else {}
  if name=='q03':settings['enable_nestloop']='off'
  oracle=read(HERE/'athena-cases.json')[name];cases[name]=one(name,sql,settings,oracle);dump(HERE/'postgres-aggregate-cases.json',cases)
 with connect() as pg:dump(folder/'storage-after-aggregates.json',snapshot(pg))
 failed=[n for n,v in cases.items() if v['state']!='complete' or v['median_seconds']>=60]
 dump(HERE/'postgres-aggregate-decision.json',{'cases':{n:{'state':v['state'],'median_seconds':v.get('median_seconds')} for n,v in cases.items()},'missed_60_seconds':failed,'citation_families_not_yet_measured':True,'do_not_increase_volume':bool(failed)})
 print('AGGREGATEPROBECOMPLETE',json.dumps({'missed_60_seconds':failed}),flush=True)
if __name__=='__main__':main()
