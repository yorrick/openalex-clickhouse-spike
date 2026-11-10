"""Oneauthor-query-shape trialafteroriginal24GiBnamegroupinghitquerymemorylimit."""
import hashlib,json,statistics,subprocess,time
from pg_helpers import HERE,dump
import run_clickhouse as ch
from tier_sql import canonical_rows

def read(p):return json.loads(p.read_text())
def main():
 path=HERE/'clickhouse-cases.json';assert path.exists(),'FinishotherCHcasesfirst'
 cases=read(path);dump(HERE/'clickhouse-cases-before-author-tune.json',cases);old=cases['q03'];assert old['state']=='failed' and old['runs'][0]['query_log']['exception_code']==241
 state=json.loads(ch.docker(['inspect',ch.NAME]).stdout)[0]
 assert state['Config']['Labels']['openalex.study']=='postgres-100m-20261109'
 plan={'at':time.time(),'reason':'Originalq03groups119m-Authornamesduringfulljoin/aggregationandhit24GiBquerylimit(code241).','candidate':'FiltervalidnumericAuthorIDs,aggregatenumericstatsandTop1000,thenAuthorsleftjoinTop1000righttoscanlabelswithouta119m-namerighthashtable.','proof_conditions':'AuthorsIDsuniqueinfrozen119129660-rowinput,validatedbyretainedPGAuthorsPK;exactsamefileloadedCH. Preserveorphanexclusion,COUNTdistinctWork,andduplicatecitationmultiplicity.','caps_unchanged':'16CPU32GiBcontainer,24GiBquery,4GiBspill,explicitHash','measurement':'1first+3warmNullandseparatefullrawAthenatypedresultQA;nootherlocalenginequeryconcurrent'};dump(HERE/'results/ch-author-tuning-plan.json',plan)
 if not state['State']['Running']:ch.docker(['start',ch.NAME])
 host=json.loads(ch.docker(['inspect',ch.NAME]).stdout)[0]['Config']['Hostname'];ch.docker(['exec','-i',ch.NAME,'sh','-c','cat >> /etc/hosts'],input='127.0.0.1 '+host+'\n')
 for _ in range(90):
  ready=subprocess.run(['docker','exec',ch.NAME,'clickhouse-client','--query','SELECT 1'],capture_output=True,text=True)
  if ready.returncode==0:break
  time.sleep(1)
 else:raise RuntimeError('CHauthortrialservernotready')
 sql=(HERE/'sql/clickhouse-q03_numeric_top_ids.sql').read_text();label='q03_numeric_top_ids';settings=dict(ch.SETTINGS)
 estimated=ch.query('EXPLAIN PLAN '+sql,fmt='TabSeparatedRaw',settings=settings);(HERE/'results/clickhouse/q03-numeric-explain.txt').write_text(estimated)
 rec={'name':'q03','label':label,'state':'running','sql':sql,'sql_sha256':hashlib.sha256(sql.encode()).hexdigest(),'runs':[],'requested_settings':settings};out=ch.FOLDER/(label+'.json');dump(out,rec)
 for i in range(4):
  _,run=ch.measure(label+'-'+str(i),sql,settings);run['kind']='primer' if i==0 else 'warm'+str(i);rec['runs'].append(run);dump(out,rec);print(label,run['kind'],run['state'],run['query_log']['seconds'],flush=True)
  if run['state']!='complete':rec['state']='failed';break
 if rec['state']!='failed':
  rows,qa_run=ch.measure(label+'-qa',sql,settings,output=True);assert qa_run['state']=='complete'
  h=hashlib.sha256('\n'.join(canonical_rows('q03',rows)).encode()).hexdigest();oracle=read(HERE/'athena-cases.json')['q03'];ref=oracle.get('reference') or oracle['runs'][0];qa={'rows':len(rows),'canonical_sha256':h,'expected_rows':ref['rows'],'expected_sha256':ref['canonical_sha256'],'matched':len(rows)==ref['rows'] and h==ref['canonical_sha256']};assert qa['matched']
  rec.update(state='complete',qa=qa,qa_execution=qa_run,warm_seconds=[float(r['query_log']['seconds']) for r in rec['runs'][1:]]);rec['median_seconds']=statistics.median(rec['warm_seconds']);print('Q03NUMERICMEDIAN',rec['median_seconds'],'QAMATCH',flush=True)
 dump(out,rec);dump(ch.FOLDER/'q03-original24-memory-failure.json',old)
 if rec['state']=='complete':cases['q03']=rec
 dump(path,cases);ch.docker(['stop',ch.NAME]);dump(HERE/'results/ch-author-tuning-complete.json',{'at':time.time(),'state':rec['state'],'selected_median_seconds':rec.get('median_seconds'),'container_stopped':True})
if __name__=='__main__':main()
