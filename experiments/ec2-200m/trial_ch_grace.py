"""One bounded profile per 200m hash-limit failure: partitioned joins for q02/q03, country sets for q04."""
import json,time,threading,traceback
import run_engines as e
import helpers as h
from helpers import HERE,dump,docker

def main():
 assert (HERE/'results/postgres/repair-complete.json').exists()
 assert not e.owned(e.PG)['State']['Running']
 assert not e.owned(e.CH)['State']['Running']
 docker('start',e.CH);h.NAME=e.CH
 threading.Thread(target=h.background_guard,daemon=True).start()
 for _ in range(120):
  try:e.chquery('SELECT 1',database='default');break
  except Exception:time.sleep(1)
 else:raise RuntimeError('Existing CH container did not become ready')
 info=e.owned(e.CH);assert info['HostConfig']['Memory']==info['HostConfig']['MemorySwap']==32*2**30 and info['HostConfig']['NanoCpus']==16*10**9
 settings=dict(e.CHSET,join_algorithm='grace_hash',grace_hash_join_initial_buckets=16,max_bytes_in_join=3*2**30)
 fixture="SELECT count() AS n FROM (SELECT number%2 AS k,number AS v FROM numbers(4)) AS a INNER JOIN (SELECT number%2 AS k,number AS v FROM numbers(4)) AS b ON a.k=b.k AND a.v<b.v"
 rows=e.chquery(fixture,settings=settings)
 assert int(rows[0]['n'])==2,rows
 names=['join_algorithm','grace_hash_join_initial_buckets','max_bytes_in_join','max_memory_usage','max_threads']
 available=e.chquery("SELECT name,type,value FROM system.settings WHERE name IN ("+','.join("'"+n+"'" for n in names)+")")
 assert len(available)==len(names)
 dump(HERE/'results/clickhouse/grace16-fixture.json',{'passed':True,'query':fixture,'rows':rows,'settings':settings,'available_settings':available,'reason':'All three initial large joins failed with code241 while FillingRightJoinSide attempted a16GiB hash allocation under24GiB. Partitioned grace hash is selected explicitly, without automatic algorithm fallback. Same SQL and resource allocation.','official_reference':'https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2'})
 pair_probe="SELECT arrayJoin(arrayFlatten(arrayMap(a -> arrayMap(b -> tuple(a,b),arrayFilter(b -> a<b,['CA','US','FR'])),['CA','US','FR']))) AS pair"
 pairs=e.chquery(pair_probe,settings=e.CHSET)
 assert sorted(tuple(x['pair']) for x in pairs)==[('CA','FR'),('CA','US'),('FR','US')]
 dump(HERE/'results/clickhouse/country-set-function-probe.json',{'passed':True,'sql':pair_probe,'rows':pairs})
 selected=json.loads((HERE/'results/clickhouse-cases.json').read_text());pg=json.loads((HERE/'results/postgres-selected.json').read_text())
 e.clear_cache()
 for name in ['q02','q03','q04']:
  original=selected[name];assert original['state']=='failed' and 'MEMORY_LIMIT_EXCEEDED' in original['error'] and 'FillingRightJoinSide' in original['error']
  sql=(HERE/'sql/clickhouse-q04_country_sets.sql').read_text() if name=='q04' else original['sql']
  profile=e.CHSET if name=='q04' else settings
  label='q04-countrysets' if name=='q04' else name+'-grace16'
  pipeline=e.chquery('EXPLAIN PIPELINE '+sql,fmt='TabSeparatedRaw',settings=profile)
  (HERE/'results/clickhouse'/(label+'-pipeline.txt')).write_text(pipeline)
  rec=e.ch_case(name,sql,profile,label=label)
  if rec.get('qa') and pg[name].get('qa'):assert rec['qa']['canonical_sha256']==pg[name]['qa']['canonical_sha256'] and rec['qa']['rows']==pg[name]['qa']['rows']
  selected[name]=rec;dump(HERE/'results/clickhouse-selected.json',selected)
 e.chquery('SYSTEM FLUSH LOGS',fmt='TabSeparatedRaw')
 maintenance=e.chquery("SELECT query_id,query,type,query_duration_ms,memory_usage,ProfileEvents,exception_code FROM system.query_log WHERE startsWith(query,'OPTIMIZE TABLE ') AND type IN ('QueryFinish','ExceptionWhileProcessing','ExceptionBeforeStart') ORDER BY event_time_microseconds")
 dump(HERE/'results/clickhouse/maintenance-query-log.json',maintenance)
 tables=e.chquery("SELECT name FROM system.tables WHERE database='system' AND name='part_log'")
 if tables:
  columns=e.chquery('DESCRIBE TABLE system.part_log');allowed={x['name'] for x in columns}
  wanted=[x for x in ['event_type','event_time_microseconds','duration_ms','database','table','part_name','rows','size_in_bytes','peak_memory_usage','error','exception','ProfileEvents'] if x in allowed]
  records=e.chquery('SELECT '+','.join('`'+x+'`' for x in wanted)+" FROM system.part_log WHERE database='openalex_spike'")
  dump(HERE/'results/clickhouse/maintenance-part-log.json',{'columns':columns,'records':records})
 dump(HERE/'results/clickhouse/grace16-complete.json',{'at':time.time(),'selected_states':{k:v['state'] for k,v in selected.items()},'part_log_available':bool(tables)})

if __name__=='__main__':
 try:main()
 except BaseException:
  dump(HERE/'results/clickhouse/grace16-error.json',{'at':time.time(),'error':traceback.format_exc()});raise
 finally:
  if e.exists(e.CH) and e.owned(e.CH)['State']['Running']:docker('stop',e.CH)
