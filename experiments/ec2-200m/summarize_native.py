"""Generate report data from selected completed observations, without timing inference."""
from pathlib import Path
import json,statistics,sys
HERE=Path(__file__).resolve().parent
root=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'cloud-results'
result={}
for engine in ['postgres','clickhouse']:
 p=root/(engine+'-selected.json')
 if not p.exists():p=root/(engine+'-cases.json')
 if not p.exists():continue
 cases=json.loads(p.read_text());out=[]
 for name,x in cases.items():
  r={'case':name,'state':x['state'],'label':x.get('label',name),'settings':x.get('effective_settings',x.get('requested_settings'))}
  if x['state']=='complete':
   warm=x['runs'][1:];resources=[v['resources'] for v in warm];wall=sum(v['window_seconds'] for v in resources);cpu=sum(v['cpu_seconds'] for v in resources)
   r.update(median_seconds=x['median_seconds'],primer_seconds=x['runs'][0].get('execution_seconds',(x['runs'][0].get('query_log') or {}).get('seconds')),result_rows=x['qa']['rows'],qa_sha256=x['qa']['canonical_sha256'],average_busy_cores=cpu/wall,warm_cpu_allocation_utilization=cpu/wall/16,warm_peak_memory_gib=max(v['memory_current_peak_bytes'] for v in resources)/2**30,warm_peak_anon_gib=max(v['memory_anon_peak_bytes'] for v in resources)/2**30,warm_peak_file_gib=max(v['memory_file_peak_bytes'] for v in resources)/2**30,warm_peak_shmem_gib=max(v['memory_shmem_peak_bytes'] for v in resources)/2**30,median_physical_read_gib=statistics.median(v['io_delta']['rbytes']/2**30 for v in resources),median_physical_write_gib=statistics.median(v['io_delta']['wbytes']/2**30 for v in resources),average_physical_read_mib_s=sum(v['io_delta']['rbytes'] for v in resources)/wall/2**20,average_read_iops=sum(v['io_delta']['rios'] for v in resources)/wall,oom_events=sum(v['memory_events_delta'].get('oom',0) for v in resources),oom_kills=sum(v['memory_events_delta'].get('oom_kill',0) for v in resources))
  else:r.update(error=x.get('error'),seconds_until_error=x.get('seconds_until_error'))
  out.append(r)
 families={}
 for q in ['q01','q02','q03','q04','q05','q06','q07']:
  group=[r for r in out if r['case'].startswith(q)];complete=[r for r in group if r['state']=='complete']
  families[q]={'completed':len(complete),'expected':3 if q in ['q05','q06'] else 1}
  if len(complete)==families[q]['expected']:families[q]['worst_seed_median_seconds']=max(r['median_seconds'] for r in complete)
 result[engine]={'cases':out,'families':families}
(HERE/'results/native-summary.json').write_text(json.dumps(result,indent=2)+'\n')
for engine,x in result.items():
 print(engine)
 for r in x['cases']:
  if r['state']=='complete':print(r['case'],f"{r['median_seconds']:.6f}s",f"{r['average_busy_cores']:.2f} cores",f"{r['warm_peak_memory_gib']:.2f}GiB total",f"{r['warm_peak_anon_gib']:.2f}GiB anon",f"{r['median_physical_read_gib']:.3f}GiB read",f"{r['average_physical_read_mib_s']:.1f}MiB/s")
  else:print(r['case'],r['state'])
