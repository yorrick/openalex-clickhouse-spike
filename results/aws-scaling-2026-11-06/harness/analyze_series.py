"""Read persisted evidence; never launch resources, infer missing values, or run SQL."""
from pathlib import Path
from statistics import median
import json
import math
from controls import outcome,write

HERE=Path(__file__).resolve().parent


def fields(text):
    if text is None:return {}
    return {line.split()[0]:int(line.split()[1]) for line in text.splitlines() if len(line.split())==2}


def pressure(text):
    if text is None:return None
    row=next((line for line in text.splitlines() if line.startswith('some ')),None)
    if row is None:return None
    return int(dict(part.split('=') for part in row.split()[1:])['total'])


def resources(record):
    samples=record.get('telemetry',[]);events=record.get('ProfileEvents',{})
    result={'query_peak_bytes':record.get('peak_memory_bytes'),'spill_compressed_bytes':record.get('spill_bytes'),'telemetry_sample_count':len(samples),'allocated_cpus':18}
    result['external_join_compressed_bytes']=int(events.get('ExternalJoinCompressedBytes',0)) if record.get('spill_counter_supported') else None
    result['external_aggregation_compressed_bytes']=int(events.get('ExternalAggregationCompressedBytes',0)) if record.get('spill_counter_supported') else None
    result['telemetry_max_gap_seconds']=max((b['at']-a['at'] for a,b in zip(samples,samples[1:])),default=None)
    cpu_keys=('UserTimeMicroseconds','SystemTimeMicroseconds')
    cpu_seconds=sum(int(events[k]) for k in cpu_keys if k in events)/1e6 if all(k in events for k in cpu_keys) else None
    result['cpu_seconds']=cpu_seconds
    result['average_cpu_cores']=cpu_seconds/record['seconds'] if cpu_seconds is not None and record.get('seconds',0)>0 else None
    result['cpu_fraction']=cpu_seconds/(record['seconds']*18) if cpu_seconds is not None and record.get('seconds',0)>0 else None
    result['container_sampled_peak_bytes']=max([int(s['memory.current']) for s in samples if s.get('memory.current') is not None],default=None)
    result['container_sampled_peak_anon_bytes']=max([fields(s.get('memory.stat'))['anon'] for s in samples if 'anon' in fields(s.get('memory.stat'))],default=None)
    result['container_sampled_peak_file_bytes']=max([fields(s.get('memory.stat'))['file'] for s in samples if 'file' in fields(s.get('memory.stat'))],default=None)
    result['sampled_scratch_used_peak_bytes']=max([s['scratch_filesystem']['used_bytes'] for s in samples if s.get('scratch_filesystem')],default=None)
    result.update(physical_read_bytes=None,physical_write_bytes=None,io_stall_fraction=None,io_fraction=None)
    if len(samples)>=2:
        first,last=samples[0],samples[-1];seconds=last['at']-first['at']
        disks=[]
        for name,start in first['disks'].items():
            if name not in last['disks']:continue
            end=last['disks'][name];d=[b-a for a,b in zip(start,end)]
            ios=d[0]+d[4]
            disks.append({'device':name,'operations':ios,'io_wait_ms':d[3]+d[7],'read_bytes':d[2]*512,'write_bytes':d[6]*512,'iops':ios/seconds if seconds else None,'await_ms':(d[3]+d[7])/ios if ios else None,'utilization':d[9]/(seconds*1000) if seconds else None})
        if disks and set(first['disks'])==set(last['disks']):
            ios=sum(d['operations'] for d in disks)
            result['physical_iops']=ios/seconds if seconds>0 else None
            result['physical_await_ms']=sum(d['io_wait_ms'] for d in disks)/ios if ios else None
            result.update(physical_read_bytes=sum(d['read_bytes'] for d in disks),physical_write_bytes=sum(d['write_bytes'] for d in disks),io_fraction=max(d['utilization'] for d in disks),disk_windows=disks)
        p0,p1=pressure(first.get('io.pressure')),pressure(last.get('io.pressure'))
        if p0 is not None and p1 is not None and seconds>0:result['io_stall_fraction']=(p1-p0)/(seconds*1e6)
        result['telemetry_window_seconds']=seconds
        result['physical_read_bytes_s']=result['physical_read_bytes']/seconds if seconds>0 and result['physical_read_bytes'] is not None else None
        result['physical_write_bytes_s']=result['physical_write_bytes']/seconds if seconds>0 and result['physical_write_bytes'] is not None else None
        cpu0,cpu1=fields(first.get('cpu.stat')),fields(last.get('cpu.stat'))
        if 'usage_usec' in cpu0 and 'usage_usec' in cpu1 and seconds>0:
            result['container_average_cpu_cores']=(cpu1['usage_usec']-cpu0['usage_usec'])/(seconds*1e6)
        if 'throttled_usec' in cpu0 and 'throttled_usec' in cpu1:
            result['container_throttled_cpu_seconds']=(cpu1['throttled_usec']-cpu0['throttled_usec'])/1e6
    # Counter correlations do not establish a causal bottleneck.
    result['bottleneck']=None
    return result


def main():
    remote=json.loads((HERE/'remote-manifest.json').read_text());full=json.loads((HERE/'historical-full-snapshot.json').read_text());result={'full_reference':{k:v for k,v in full.items() if k!='entities'},'tiers':{}}
    for tier in ('stage2_small','stage2_medium','stage2_large'):
        state_path=HERE/(tier+'-state.json')
        if not state_path.exists():continue
        state=json.loads(state_path.read_text());path=HERE/state['ch_run']/'cloud/summary.json'
        if not path.exists():continue
        ch=json.loads(path.read_text());ath_path=HERE/state.get('athena_run','not-started')/'summary.json'
        ath=json.loads(ath_path.read_text()) if ath_path.exists() else {}
        cohort=remote['tiers'][tier]
        data={'state':state['state'],'works':cohort['work_rows'],'input_bytes':cohort['bytes'],'works_bytes':cohort['work_bytes'],'percent_full_works':100*cohort['work_rows']/full['works'],'percent_full_bytes':100*cohort['bytes']/full['all_parquet_bytes'],'dimensions_seconds':ch['dimensions_seconds'],'works_load_seconds':ch['load_seconds'],'table_bytes':ch['table_bytes'],'normalized_bytes':sum(int(t['bytes']) for t in ch['table_bytes']),'merges_quiescent':ch['merges_quiescent'],'graph':ch['graph'],'cases':{},'athena_all_matched':ath.get('all_matched'),'athena_billable_bytes':ath.get('billable_bytes'),'variants':ch.get('variants',{})}
        for name,records in ch['timings'].items():
            warm=[r for r in records if r.get('block','').startswith('warm')]
            times=[r['seconds'] for r in warm if r['state']=='complete']
            a=ath.get('timings',{}).get(name,[]);matching=False if any(r.get('matched') is False for r in a) else (True if len(a)==3 and all(r.get('matched') is True for r in a) else None)
            status=outcome(times,matched=matching,timeout=any(r['state']=='timeout' for r in records))
            if any(r['state']=='memory_limit_exceeded' for r in records):status='FAIL_RESOURCE'
            elif ch['merges_quiescent'] is not True:status='INCONCLUSIVE_MERGES'
            case={'warm_seconds':times,'median_seconds':median(times) if times else None,'min_seconds':min(times) if times else None,'max_seconds':max(times) if times else None,'status':status,'resources':[resources(r) for r in warm if r['state']=='complete'],'athena_runs':a,'qa_matched':matching}
            durations=[r['statistics']['TotalExecutionTimeInMillis']/1000 for r in a if r.get('statistics')]
            case['athena_median_seconds']=median(durations) if durations else None
            if name in ch.get('cold_tests',{}):case['cold']=ch['cold_tests'][name];case['cold_resources']=resources(case['cold'])
            data['cases'][name]=case
        result['tiers'][tier]=data
    for a,b in (('stage2_small','stage2_medium'),('stage2_medium','stage2_large')):
        if a not in result['tiers'] or b not in result['tiers']:continue
        d1,d2=result['tiers'][a],result['tiers'][b]
        for name,c2 in d2['cases'].items():
            c1=d1['cases'].get(name)
            if not c1 or not c1['median_seconds'] or not c2['median_seconds']:continue
            c2['growth_from_'+a]={'row_ratio':d2['works']/d1['works'],'time_ratio':c2['median_seconds']/c1['median_seconds'],'descriptive_exponent':math.log(c2['median_seconds']/c1['median_seconds'])/math.log(d2['works']/d1['works'])}
    write(HERE/'series-analysis.json',result)
    print(json.dumps({'tiers':{t:{'works':d['works'],'cases':len(d['cases']),'matched':d['athena_all_matched'],'normalized_bytes':d['normalized_bytes']} for t,d in result['tiers'].items()}}))


if __name__=='__main__':main()
