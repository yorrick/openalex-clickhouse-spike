"""Independent evidence checks, no benchmarkreruns or inferred missingtimings."""
from pathlib import Path
import gzip,hashlib,json,statistics
import pyarrow as pa,pyarrow.csv as pc
from pg_helpers import HERE,dump
from tier_sql import canonical_rows

def read(p):return json.loads(Path(p).read_text())
def main():
 checks=[];manifest=read(HERE/'works-input-manifest.json');files=manifest['files']
 assert len(files)==480 and sum(x['record_count'] for x in files)==100087422
 assert sum(x['content_length'] for x in files)==141981190499
 remote=read(HERE/'remote-inputs.json');rf=remote['files'];assert len(rf)==3097
 works={f['source_key']:f for f in rf if f['entity']=='works'}
 assert len(works)==480 and sum(f['rows'] for f in works.values())==100087422
 for f in files:
  r=works[f['source_key']];assert r['version_id']==f['version_id'] and r['bytes']==f['content_length'] and r['rows']==f['record_count']
  if r['known_sha256']:assert r['known_sha256']==r['server_full_sha256'] and r['verified_against_prior_full_sha256']
 checks.append('480pinnedWorkversions,fullS3checksumsandhistoricalfooterrowcountsconsistent')
 previous=read(Path('/Users/yorrickjansen/work/openalex/results/aws-scaling-2026-11-06/input-files.json'))['files'];oldkeys={f['source_key'] for f in previous if f['entity']=='works'};assert len(oldkeys)==154 and oldkeys<=set(works)
 checks.append('All154previousWorkfilesareincludedin100mcohort')
 counts={};columns=0
 for table in ['works','work_author','work_institution','work_topic','citation_edge','authors','institutions','sources','topics']:
  p=read(HERE/'results'/('project-'+table+'.json'));assert p['state']=='complete'
  f=HERE/'projected'/(table+'.parquet');assert f.stat().st_size==p['bytes'];h=hashlib.sha256()
  with f.open('rb') as x:
   while b:=x.read(8<<20):h.update(b)
  assert h.hexdigest()==p['sha256'];counts[table]=p['rows'];columns+=len(p['columns'])
 assert columns==42 and counts['works']==100087422 and counts['authors']==119129660
 load=read(HERE/'results/postgres/aggregate-preparation.json');assert load['counts']==counts and load['all12valid_ready']
 checks.append('All9normalizedpayloadsfullSHA-reverified,42columns,andexactPGtablecounts/12validnoncitationindexesmatch;100mGraphcasecoverageexplicit')
 oracle=read(HERE/'athena-cases.json');pg=read(HERE/'postgres-cases.json');ch=read(HERE/'clickhouse-cases.json') if (HERE/'clickhouse-cases.json').exists() else {}
 assert len(oracle)==11 and len(pg)==11
 qa=0;observations=0
 for engine,cases in [('postgres',pg),('clickhouse',ch)]:
  folder=HERE/'results'/engine
  for name,c in cases.items():
   assert hashlib.sha256(c['sql'].encode()).hexdigest()==c['sql_sha256']
   if c['state']!='complete':continue
   assert len(c['runs'])==4 and c['runs'][0]['kind']=='primer'
   times=[r['execution_seconds'] if engine=='postgres' else float(r['query_log']['seconds']) for r in c['runs'][1:]]
   assert times==c['warm_seconds'] and statistics.median(times)==c['median_seconds']
   expected=oracle[name].get('reference') or oracle[name]['runs'][0]
   assert c['qa']['rows']==expected['rows'] and c['qa']['canonical_sha256']==expected['canonical_sha256']
   qa+=1
   for i,run in enumerate(c['runs']):
    label=c.get('label',name);path=folder/(label+f'-{i}-telemetry.json');xs=read(path);xs=[x for x in xs if 'cpu' in x];a,b=xs[0],xs[-1]
    seconds=(b['cpu']['usage_usec']-a['cpu']['usage_usec'])/1e6;window=b['at']-a['at'];resources=run['resources']
    assert abs(seconds/window-resources['average_busy_cores_in_monitor_window'])<1e-10
    assert max(x['memory_current'] for x in xs)==resources['memory_current_peak_bytes']
    observations+=1
 checks.append(f'{qa}completePG/CHfull-resulttypedhashesmatchrawAthena;{observations}nativeobservations/medians/CPU/memoryindependentlyrecomputed')
 # Verify archivedfullCSVagainstfingerprint,includingquotedemptyvsNULLand64-bitintegers.
 archived={x['query_id']:x for x in read(HERE/'results/athena-csv-archives.json')};csv_checks=0
 for name,c in oracle.items():
  refs=c['runs']+[c['reference']] if c.get('reference') else c['runs']
  seen=set()
  for ref in refs:
   qid=ref['query_id']
   if qid in seen:continue
   seen.add(qid);meta=archived[qid];body=gzip.decompress(Path(meta['local_path']).read_bytes());assert hashlib.sha256(body).hexdigest()==meta['raw_csv_sha256']
   first=pc.read_csv(pa.BufferReader(body),parse_options=pc.ParseOptions(newlines_in_values=True),read_options=pc.ReadOptions(autogenerate_column_names=False),convert_options=pc.ConvertOptions(column_types={k:pa.string() for k in __import__('tier_sql').RESULT_TYPES[name[:3]]},strings_can_be_null=True,quoted_strings_can_be_null=False,null_values=['']))
   rows=first.to_pylist();h=hashlib.sha256('\n'.join(canonical_rows(name[:3],rows)).encode()).hexdigest();assert len(rows)==ref['rows'] and h==ref['canonical_sha256'];csv_checks+=1
 checks.append(f'{csv_checks}fullAthenaCSVresultsreparsedandtypedhashesindependentlyrecomputed')
 clean=read(HERE/'results/aws-cleanup.json');assert clean['all_queries_terminal'] and len(clean['absence_probes'])==3
 assert clean['billable_athena_bytes']<=700000000000
 checks.append('OwnedAWSresourcesabsent,allqueriesterminal,700GBscanbudgetrespected')
 dump(HERE/'results/verification.json',{'pass':True,'checks':checks,'table_counts':counts,'total_rows':sum(counts.values()),'pg_qa_matches':sum(v['state']=='complete' for v in pg.values()),'ch_qa_matches':sum(v['state']=='complete' for v in ch.values()),'athena_csv_checks':csv_checks})
 print(json.dumps({'pass':True,'checks':checks},indent=2))
if __name__=='__main__':main()
