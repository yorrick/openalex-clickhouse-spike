"""Independent recomputation of native medians/resources and full raw-Athena output fingerprints."""
from pathlib import Path
import json,gzip,hashlib,statistics,sys
import pyarrow as pa,pyarrow.csv as pc
from tier_sql import canonical_rows
HERE=Path(__file__).resolve().parent;CLOUD=HERE/'cloud-results'
def read(p):return json.loads(Path(p).read_text())
def stats(xs):
 good=[x for x in xs if 'cpu' in x];assert len(good)>=2
 a,b=good[0],good[-1];dt=b['at']-a['at'];assert dt>0
 cpu=(b['cpu']['usage_usec']-a['cpu']['usage_usec'])/1e6
 return {'window_seconds':dt,'cpu_seconds':cpu,'average_busy_cores':cpu/dt,'memory_current_peak_bytes':max(x['memory_current'] for x in good),'memory_anon_peak_bytes':max(x['memory'].get('anon',0) for x in good),'memory_file_peak_bytes':max(x['memory'].get('file',0) for x in good),'memory_shmem_peak_bytes':max(x['memory'].get('shmem',0) for x in good),'memory_events_delta':{k:b['memory_events'][k]-a['memory_events'].get(k,0) for k in b['memory_events']},'io_delta':{k:sum(x.get(k,0) for x in b['io'].values())-sum(x.get(k,0) for x in a['io'].values()) for k in ['rbytes','wbytes','rios','wios']}}
def main():
 selected={engine:read(CLOUD/(engine+'-selected.json' if (CLOUD/(engine+'-selected.json')).exists() else engine+'-cases.json')) for engine in ['postgres','clickhouse']}
 athena=read(HERE/'athena-cases.json');coverage={};observations=0;checks=[]
 for engine,cases in selected.items():
  assert len(cases)==11,(engine,'unexpected case count')
  coverage[engine]={k:v['state'] for k,v in cases.items()}
  for name,case in cases.items():
   if case['state']!='complete':
    assert 'median_seconds' not in case,('Incomplete case has fabricated median',engine,name);continue
   assert len(case['runs'])==4;warm=case['runs'][1:];values=[r['execution_seconds'] if engine=='postgres' else r['query_log']['seconds'] for r in warm];assert abs(statistics.median(values)-case['median_seconds'])<1e-9
   label=case.get('label',name)
   for i,run in enumerate(case['runs']):
    observations+=1
    xs=read(CLOUD/engine/(label+f'-{i}-telemetry.json'));actual=stats(xs);recorded=run['resources']
    assert abs(actual['average_busy_cores']-recorded['average_busy_cores'])<1e-8
    assert actual['memory_current_peak_bytes']==recorded['memory_current_peak_bytes'] and actual['io_delta']==recorded['io_delta']
    if engine=='postgres':assert abs(run['execution_seconds']-run['plan']['Execution Time']/1000)<1e-9
    else:assert run['query_log']['exception_code']==0
   reference=athena.get(name,{}).get('reference') or ((athena.get(name,{}).get('runs') or [None])[0])
   assert reference is not None,(name,'missing raw Athena reference')
   assert case['qa']['rows']==reference['rows'] and case['qa']['canonical_sha256']==reference['canonical_sha256'],(engine,name,'full typed output differs from raw Athena')
   checks.append({'engine':engine,'case':name,'rows':case['qa']['rows'],'sha256':case['qa']['canonical_sha256'],'matched_raw_athena':True})
 csv_count=0
 for name,case in athena.items():
  for r in case.get('runs',[]):
   path=HERE/'athena-csv'/(r['query_id']+'.csv.gz')
   assert path.exists(),path
   with gzip.open(path,'rb') as f:data=f.read()
   table=pc.read_csv(pa.BufferReader(data),parse_options=pc.ParseOptions(newlines_in_values=True),convert_options=pc.ConvertOptions(column_types={k:pa.string() for k in __import__('tier_sql').RESULT_TYPES[name[:3]]},strings_can_be_null=True,quoted_strings_can_be_null=False,null_values=['']))
   canon=canonical_rows(name[:3],table.to_pylist());h=hashlib.sha256('\n'.join(canon).encode()).hexdigest();assert len(canon)==r['rows'] and h==r['canonical_sha256'];csv_count+=1
 source=read(HERE/'remote-inputs.json')['files'];host={x['source_key']:x for x in [read(p) for p in (CLOUD/'download').glob('*.json')]};assert len(host)==len(source)==3572
 for f in source:
  actual=host[f['source_key']];assert actual['version_id']==f['version_id'] and actual['sha256']==f['server_full_sha256'] and actual['footer_rows']==f['rows'] and actual['bytes']==f['bytes']
 counts=read(CLOUD/'projection-complete.json')['counts'];assert counts['works']==200313862 and counts['authors']==119129660 and counts['institutions']==127784 and counts['sources']==283287 and counts['topics']==4516
 for engine in ['postgres','clickhouse']:
  p=read(CLOUD/engine/'prepared.json');assert p['counts']==counts
  for table,n in counts.items():assert read(CLOUD/engine/('load-'+table+'.json'))['rows']==n
  if engine=='postgres':assert len(p['indexes'])==14 and all(x[1] and x[2] for x in p['indexes'])
  else:assert {x['table']:int(x['rows']) for x in p['storage']}==counts
 sample=read(CLOUD/'normalization-sample-qa.json');assert sample['passed']
 # Recheck censored attempts and the preserved baseline profiles as well as the
 # selected completed timings. A failed query's CPU/I/O is still real evidence.
 all_traces=set()
 def check_trace(engine,label,index,recorded):
  key=(engine,label,index)
  actual=stats(read(CLOUD/engine/(label+f'-{index}-telemetry.json')))
  assert abs(actual['average_busy_cores']-recorded['average_busy_cores'])<1e-8
  assert actual['memory_current_peak_bytes']==recorded['memory_current_peak_bytes'] and actual['io_delta']==recorded['io_delta']
  for k in ['window_seconds','cpu_seconds']:assert abs(actual[k]-recorded[k])<1e-8
  for k in ['memory_anon_peak_bytes','memory_file_peak_bytes','memory_shmem_peak_bytes','memory_events_delta']:assert actual[k]==recorded[k]
  all_traces.add(key)
 for engine in ['postgres','clickhouse']:
  baseline=read(CLOUD/(engine+'-cases.json'))
  for cases in [baseline,selected[engine]]:
   for name,case in cases.items():
    label=case.get('label',name)
    for i,run in enumerate(case.get('runs',[])):check_trace(engine,label,i,run['resources'])
    if engine=='postgres' and case.get('resources'):check_trace(engine,label,len(case.get('runs',[])),case['resources'])
    if engine=='clickhouse' and case.get('qa_execution'):check_trace(engine,label,4,case['qa_execution']['resources'])
 result={'verified':True,'scope':'Every completed selected native case matches raw Athena; independent median/resource recomputation; full archived CSV reparse; source checksum/footer equivalence. Incomplete cases remain explicit.','coverage':coverage,'completed_full_output_checks':checks,'native_observations_recomputed':observations,'all_profile_trace_observations_recomputed':len(all_traces),'full_csv_results_reparsed':csv_count,'all3572source_server_host_sha_footer_matches':True,'loaded_counts':counts,'independent_value_sample':sample['sample_source_rows']}
 (HERE/'results/verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['completed_full_output_checks','coverage']},indent=2))
if __name__=='__main__':main()
