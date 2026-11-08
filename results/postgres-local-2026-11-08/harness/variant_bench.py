from pathlib import Path
import sys,json,time,hashlib,statistics,psycopg
from psycopg.rows import dict_row
from pg_helpers import HERE,connect,dump,Monitor
from index_and_benchmark import summarize_monitor,MOD,ROOT

def main():
 tier,name,query,path=sys.argv[1:];sql=Path(path).read_text();folder=HERE/'results'/tier;result={'variant':name,'query':query,'tier':tier,'sql':sql,'state':'running','runs':[],'settings_changed':False};out=folder/(name+'.json');oracle=json.loads((ROOT/'results/aws-scaling-2026-11-06'/f'{tier}.json').read_text())['cases'][query];dump(out,result)
 with connect() as pg:
  for i in range(4):
   m=Monitor().start();st=time.monotonic()
   try:
    p=pg.execute('EXPLAIN (ANALYZE, BUFFERS, WAL, SETTINGS, TIMING OFF, FORMAT JSON) '+sql).fetchone()[0][0];client=time.monotonic()-st
   except psycopg.errors.QueryCanceled as e:
    xs=m.stop();result.update(state='timeout',timeout_seconds=300,error=str(e),resources=summarize_monitor(xs));dump(out,result);return
   except BaseException:m.stop();raise
   xs=m.stop();rec={'kind':'primer' if i==0 else f'warm{i}','execution_seconds':p['Execution Time']/1000,'planning_seconds':p['Planning Time']/1000,'client_seconds':client,'plan':p,'resources':summarize_monitor(xs)};result['runs'].append(rec);dump(folder/(name+f'-{i}-telemetry.json'),xs);dump(out,result);print(name,rec['kind'],rec['execution_seconds'],flush=True)
  st=time.monotonic()
  with pg.cursor(row_factory=dict_row) as c:c.execute(sql);rows=c.fetchall()
  canon=MOD.canonical_rows(query[:3],rows);h=hashlib.sha256('\n'.join(canon).encode()).hexdigest();match=h==oracle['canonical_result_sha256'] and len(rows)==oracle['result_rows'];result['qa']={'matched':match,'canonical_sha256':h,'expected_sha256':oracle['canonical_result_sha256'],'rows':len(rows),'expected_rows':oracle['result_rows'],'fetch_seconds':time.monotonic()-st};assert match,'Variant output mismatch'
  ts=[r['execution_seconds'] for r in result['runs'] if r['kind']!='primer'];result.update(state='complete',warm_seconds=ts,median_seconds=statistics.median(ts));dump(out,result);print(name,'QA MATCH; median',result['median_seconds'],flush=True)
if __name__=='__main__':main()
