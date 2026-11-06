"""Measured Stage2 EC2 trial. Raw EBS read-only; CH writes separate root gp3."""
from pathlib import Path
from datetime import datetime, timezone
from scope import validate_scope, manifest_identity
from time import monotonic, sleep
from threading import Event, Thread
import errno
import hashlib
import json
import os
import platform
import runpy
import shutil
import subprocess
import traceback
import uuid

import boto3
import pyarrow as pa
import pyarrow.parquet as pq

from openalex_spike.cli import _prepare_stage2_dimensions, _load_stage2_tier
from openalex_spike.clickhouse import ClickHouseService

BASE=Path('/root/work/data/openalex-small-spike')
ROOT=BASE/'repo'
OUT=BASE/'benchmark-results'
MOUNT=Path('/mnt/openalex-input')
S3=boto3.client('s3',region_name='us-east-1')
BUCKET=os.environ['SPIKE_BUCKET']
GIB=1<<30
DEADLINE=monotonic()+100*60
SPILL_SUPPORTED=False
SETTINGS={'max_threads':18,'max_memory_usage':12*GIB,'max_execution_time':300,
          'count_distinct_implementation':'uniqExact','max_bytes_before_external_group_by':4*GIB,
          'max_bytes_before_external_sort':4*GIB,'join_algorithm':'auto'}


class Service(ClickHouseService):
    def published_hosts(self, *, inspect=None):
        if inspect is None:
            inspect=json.loads(self._run(['docker','inspect',self.container_id()]))[0]
        ports=inspect['NetworkSettings']['Ports']
        if '9009/tcp' in ports and ports['9009/tcp'] in (None,[]):
            inspect={**inspect,'NetworkSettings':{**inspect['NetworkSettings'],'Ports':{k:v for k,v in ports.items() if k!='9009/tcp'}}}
        result=super().published_hosts(inspect=inspect)
        if result!={'8123':'127.0.0.1','9000':'127.0.0.1'}:
            raise RuntimeError('Expected loopback-only published ports')
        return result


def run(args,check=True):
    p=subprocess.run(args,text=True,capture_output=True)
    if check and p.returncode:
        raise RuntimeError(str(args)+': '+p.stderr[-4000:])
    return p


def save(name,value):
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/name
    path.write_text(json.dumps(value,indent=2)+'\n')
    S3.upload_file(str(path),BUCKET,'run/cloud/'+name)


def start_service(root):
    data=root/'.data/clickhouse'
    data.mkdir(parents=True,exist_ok=True)
    if any(data.iterdir()):
        raise RuntimeError('Expected fresh ClickHouse data directory')
    os.chown(data,101,101)
    data.chmod(0o700)
    service=Service(root)
    service.up(memory_gb=50,cpus=18)
    return service


def fixture(optimized_sql):
    global SPILL_SUPPORTED
    root=BASE/'fixture-repo'
    shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','.data','.claude'))
    raw=root/'.data/raw'
    writer=runpy.run_path(str(ROOT/'tests/integration/test_transform_sql.py'))['_write_parquet_fixtures']
    writer(raw)
    path=raw/'fixtures/works/fixture.parquet'
    table=pq.read_table(path)
    works=table.to_pylist()
    works[0]['authorships'][0]['institutions'].append({'id':'https://openalex.org/I2','display_name':'Institute Two'})
    third=json.loads(json.dumps(works[0])); third['id']='https://openalex.org/W3'; third['referenced_works']=['https://openalex.org/W1']; works.append(third)
    for w in works:
        w['referenced_works_count']=len(w['referenced_works'] or [])
    pq.write_table(pa.Table.from_pylist(works),path)
    for entity in ('works','authors','institutions','sources','topics'):
        target=raw/'tiers/stage2_large'/entity
        target.mkdir(parents=True)
        os.link(raw/'fixtures'/entity/'fixture.parquet',target/'fixture.parquet')
    service=start_service(root)
    try:
        counts,_=_prepare_stage2_dimensions(service,root=root,database='openalex_fixture',
            expected_counts={e:2 for e in ('authors','institutions','sources','topics')},result_dir=OUT/'fixture-dimensions')
        correctness,profile,_=_load_stage2_tier(service,root=root,database='openalex_fixture',tier='stage2_large',
            expected_rows=3,result_dir=OUT/'fixture',minimum_ordinary_author_reference_coverage=.999)
        if service.query_value("SELECT count() FROM system.events WHERE event='ExternalProcessingCompressedBytesTotal' SETTINGS system_events_show_zero_values=1")!='1':raise RuntimeError('Fixture spill counter unsupported')
        SPILL_SUPPORTED=True
        sqls=catalog(root,'openalex_fixture',[1])
        rows={name:query(service,sql,output=True)[0] for name,sql in sqls.items()}
        if any(not value for value in rows.values()) or rows['q06-s1'][0]['second_hop_works']<1:
            raise RuntimeError('Fixture query catalog unexpectedly empty')
        proof=run_cases(service,sqls['q02'],optimized_sql.replace('openalex_spike','openalex_fixture'),q02_signature(rows['q02']),len(rows['q02']),prefix='fixture-tuning')
        if not proof['all_cases_validated']:raise RuntimeError('Native tiny tuning preflight did not validate every case')
        save('fixture.json',{'passed':True,'counts':counts,'correctness':correctness,'rows':rows,'tuning':proof})
    finally:
        service.down()
    shutil.rmtree(root)


def mount_raw(config):
    wanted=config['raw_volume_id'].replace('-','')
    devices=json.loads(run(['lsblk','-J','-p','-o','NAME,SERIAL,TYPE,MOUNTPOINT']).stdout)['blockdevices']
    matches=[d for d in devices if str(d.get('serial','')).strip()==wanted and d['type']=='disk']
    def mounted(d):
        return d.get('mountpoint') or any(mounted(c) for c in d.get('children',[]))
    if len(matches)!=1 or mounted(matches[0]):
        raise RuntimeError('Raw EBS identity or unmounted-state check failed')
    device=matches[0]['name']
    run(['blockdev','--setro',device])
    MOUNT.mkdir(exist_ok=True)
    run(['mount','-t','ext4','-o','ro,noload',device,str(MOUNT)])
    dataset=json.loads((MOUNT/'dataset.json').read_text())
    if dataset.get('manifest_identity')!=manifest_identity(config) or dataset['state']!='complete' or dataset['series_id']!=config['series_id'] or dataset['bytes']!=98_301_763_421 or dataset['all_sha256_match'] is not True:
        raise RuntimeError('Retained input dataset identity failed')
    if run(['blockdev','--getro',device]).stdout.strip()!='1' or not(os.statvfs(MOUNT).f_flag&os.ST_RDONLY):
        raise RuntimeError('Input EBS is writable')
    try:
        (MOUNT/'.must-not-write').write_bytes(b'x')
    except OSError as exc:
        if exc.errno!=errno.EROFS:
            raise
    else:
        raise RuntimeError('Input EBS accepted a write')
    target=ROOT/'.data/raw'; target.mkdir(parents=True)
    run(['mount','--bind',str(MOUNT/'raw'),str(target)])
    run(['mount','-o','remount,bind,ro',str(target)])
    if not(os.statvfs(target).f_flag&os.ST_RDONLY):
        raise RuntimeError('Raw Docker bind source is writable')
    save('input-mount.json',{'dataset':dataset,'device':device,'block_read_only':True,'filesystem_read_only':True,'write_errno':'EROFS'})


def catalog(root,database,seeds):
    result={}
    for path in sorted((root/'sql/queries').glob('q*.sql')):
        name=path.name[:3]
        sql=path.read_text().replace('openalex_spike',database)
        if name=='q07':
            old='ORDER BY citations DESC, cited_work_id'
            if sql.count(old)!=1:
                raise RuntimeError('Pinned q07 SQL differs')
            sql=sql.replace(old,'ORDER BY citations DESC, cited_work_id, citing_year NULLS LAST')
        if name in ('q05','q06'):
            for seed in seeds:
                result[f'{name}-s{seed}']=sql.replace('{seed_work_id:UInt64}',str(seed))
        else:
            result[name]=sql
    if len(result)!=5+2*len(seeds):
        raise RuntimeError('Incomplete query catalog')
    return result


def sample(cgroup):
    result={'at':monotonic(),'disks':{}}
    fs=os.statvfs(ROOT)
    result['scratch_filesystem']={'total_bytes':fs.f_blocks*fs.f_frsize,'used_bytes':(fs.f_blocks-fs.f_bfree)*fs.f_frsize,'available_bytes':fs.f_bavail*fs.f_frsize}
    for name in ('cpu.stat','cpu.pressure','io.pressure','io.stat','memory.current','memory.stat'):
        p=cgroup/name
        result[name]=p.read_text() if p.exists() else None
    for line in Path('/proc/diskstats').read_text().splitlines():
        fields=line.split()
        if fields[2].startswith('nvme') and 'p' not in fields[2]:
            result['disks'][fields[2]]=[int(x) for x in fields[3:]]
    return result


def query(service,sql,output=False,cpus=18,collect=False):
    qid=str(uuid.uuid4())
    command=['docker','compose','exec','-T','clickhouse',*service._client_command('--query_id='+qid,'--format='+('JSONEachRow' if output else 'Null'))]
    command.extend('--'+k+'='+str(cpus if k=='max_threads' else v) for k,v in SETTINGS.items())
    cid=service.container_id()
    pid=service._run(['docker','inspect','--format','{{.State.Pid}}',cid])
    cgroup=Path('/sys/fs/cgroup')/Path('/proc/'+pid+'/cgroup').read_text().strip().split('::')[1].lstrip('/')
    stop=Event(); samples=[]
    def monitor():
        while not stop.is_set():
            samples.append(sample(cgroup)); stop.wait(.5)
    thread=Thread(target=monitor,daemon=True)
    if collect:
        thread.start()
    started=monotonic()
    try:
        p=subprocess.run(command,cwd=service.project_dir,input=sql,text=True,capture_output=True,timeout=330)
        command_seconds=monotonic()-started
    except subprocess.TimeoutExpired:
        service.execute_script(f"KILL QUERY WHERE query_id='{qid}' SYNC")
        return [],{'query_id':qid,'state':'timeout','seconds_lower_bound':300,'telemetry':samples,'requested_settings':dict(SETTINGS,max_threads=cpus)}
    finally:
        stop.set()
        if collect:
            thread.join(); samples.append(sample(cgroup))
    service.execute_script('SYSTEM FLUSH LOGS')
    metrics=service.query_json(f"SELECT type,query_duration_ms/1000.0 AS seconds,read_rows,read_bytes,result_rows,memory_usage AS peak_memory_bytes,ProfileEvents,Settings FROM system.query_log WHERE query_id='{qid}' AND type IN ('QueryFinish','ExceptionWhileProcessing','ExceptionBeforeStart') ORDER BY event_time_microseconds DESC LIMIT 1")
    record={'query_id':qid,'client_seconds':command_seconds,'format':'JSONEachRow' if output else 'Null','state':'complete' if p.returncode==0 else 'failed','error':p.stderr[-3000:] if p.returncode else None,'telemetry':samples,'requested_settings':dict(SETTINGS,max_threads=cpus)}
    if metrics:
        record.update(metrics[0])
        record['ProfileEvents']={k:int(v) for k,v in record['ProfileEvents'].items()}
        for key in ('read_rows','read_bytes','result_rows','peak_memory_bytes'):
            record[key]=int(record[key])
        record['spill_bytes']=record['ProfileEvents'].get('ExternalProcessingCompressedBytesTotal',0) if SPILL_SUPPORTED else None
        record['spill_counter_supported']=SPILL_SUPPORTED
    if p.returncode and ('TIMEOUT_EXCEEDED' in p.stderr or 'TIMEOUT' in p.stderr):
        record.update(state='timeout',seconds_lower_bound=300)
    if p.returncode and 'MEMORY_LIMIT_EXCEEDED' in p.stderr:
        record['state']='memory_limit_exceeded'
    if p.returncode==0 and not metrics:
        raise RuntimeError('Successful query missing query_log evidence')
    return [json.loads(line) for line in p.stdout.splitlines()] if output and p.returncode==0 else [],record


def seeds(service,config):
    if config.get('seeds'):
        return config['seeds']
    # Eligible seeds have an internal next-hop; selection runs only on the 2m tier.
    degree="SELECT citing_work_id AS seed,count() AS degree FROM openalex_benchmark.citation_edge GROUP BY citing_work_id HAVING countIf(cited_work_id IN (SELECT DISTINCT citing_work_id FROM openalex_benchmark.citation_edge))>0"
    quantiles=service.query_json("SELECT quantileExact(.5)(degree) AS median,quantileExact(.9)(degree) AS p90,quantileExact(.99)(degree) AS p99 FROM ("+degree+")")[0]
    chosen=[]
    for label in ('median','p90','p99'):
        selected=service.query_json("SELECT seed,degree FROM ("+degree+") WHERE seed NOT IN ("+','.join(str(r['seed']) for r in chosen or [{'seed':0}])+") ORDER BY abs(toInt64(degree)-"+str(quantiles[label])+"),seed LIMIT 1")
        if len(selected)!=1:
            raise RuntimeError('Cannot select distinct graph panel')
        chosen.extend(selected)
    save('seed-preregistration.json',{'policy':'outgoing degree p50/p90/p99 from seeds with internal next-hop in 2m tier, before timing','quantiles':quantiles,'panel':chosen})
    return [int(r['seed']) for r in chosen]


def q02_signature(rows):
    columns={'publication_year','t.topic_id','display_name','works','citations'}
    encoded=[]
    for row in rows:
        if set(row)!=columns:
            raise RuntimeError('Unexpected q02 result schema: '+str(set(row)))
        values=[None if row['publication_year'] is None else int(row['publication_year']),int(row['t.topic_id']),row['display_name'],int(row['works']),int(row['citations'])]
        encoded.append(json.dumps(values,ensure_ascii=False,separators=(',',':')))
    return hashlib.sha256('\n'.join(sorted(encoded)).encode()).hexdigest()


POLICY={'clock':'query_log server seconds, FORMAT Null','warm_repeats':3,'target_seconds':60,'pass_rule':'all three warm observations under60s, exact typed QA, effective settings verified','controls_max_median_ratio':1.20,'control_failure':'INCONCLUSIVE_COMPARISON','case_order':['original_a','memory24','parallel_hash24','preaggregate12','original_b']}

def run_cases(service,original,optimized,expected_sha,expected_rows,prefix='tuning'):
    from statistics import median
    base=dict(SETTINGS);base['log_query_settings']=1
    results={}
    cases=[('original_a',original,12,4,'auto'),('memory24',original,24,8,'auto'),('parallel_hash24',original,24,8,'parallel_hash'),('preaggregate12',optimized,12,4,'auto'),('original_b',original,12,4,'auto')]
    for name,sql,query_gib,spill_gib,algorithm in cases:
        entry={'state':'running','query_memory_gib':query_gib,'spill_gib':spill_gib,'join_algorithm':algorithm,'primer':None,'runs':[],'qa':None};results[name]=entry
        save(prefix+'.json',results)
        if monotonic()+330>DEADLINE:
            entry['state']='incomplete_deadline';save(prefix+'.json',results);continue
        SETTINGS.clear();SETTINGS.update(base,max_memory_usage=query_gib*GIB,max_bytes_before_external_group_by=spill_gib*GIB,max_bytes_before_external_sort=spill_gib*GIB,join_algorithm=algorithm)
        try:
            controls=('max_threads','max_memory_usage','max_bytes_before_external_group_by','max_bytes_before_external_sort','join_algorithm')
            setting_rows,_=query(service,"SELECT name,value,changed FROM system.settings WHERE changed OR name IN ('max_threads','max_memory_usage','max_bytes_before_external_group_by','max_bytes_before_external_sort','join_algorithm','max_bytes_in_join','max_rows_in_join','join_overflow_mode','default_max_bytes_in_join','partial_merge_join_rows_in_right_blocks','join_on_disk_max_files_to_merge')",output=True)
            entry['raw_settings']=setting_rows
            # getSetting exposes the effective value even if query_log omits a default.
            echo,_=query(service,'SELECT '+','.join("getSetting('"+k+"') AS "+k for k in controls),output=True)
            effective=echo[0];entry['effective_settings']=effective
            for key in controls:
                if str(effective.get(key))!=str(SETTINGS[key]):raise RuntimeError('Effective setting mismatch: '+key)
            entry['settings_verified']=True
            flags=['--'+k+'='+str(v) for k,v in SETTINGS.items()]
            entry['plan']=service._compose(['exec','-T','clickhouse',*service._client_command('--format=TabSeparatedRaw',*flags)],input_text='EXPLAIN PLAN actions=1 '+sql)
            save('status.json',{'state':prefix,'case':name,'phase':'primer'})
            entry['primer']=query(service,sql)[1];save(prefix+'.json',results)
            if entry['primer']['state']!='complete':entry['state']='failed_primer';continue
            for iteration in range(3):
                if monotonic()+330>DEADLINE:entry['state']='incomplete_deadline';break
                save('status.json',{'state':prefix,'case':name,'phase':'warm'+str(iteration+1)})
                metric=query(service,sql,collect=True)[1];entry['runs'].append(metric);save(prefix+'.json',results)
                if metric['state']!='complete':entry['state']='failed_timing';break
            if len(entry['runs'])!=3 or any(r['state']!='complete' for r in entry['runs']):continue
            if monotonic()+330>DEADLINE:entry['state']='incomplete_deadline';continue
            rows,metric=query(service,sql,output=True)
            if metric['state']!='complete':entry['state']='failed_qa';continue
            digest=q02_signature(rows);matched=digest==expected_sha and len(rows)==expected_rows
            entry['qa']={'matched':matched,'rows':len(rows),'canonical_sha256':digest,'query_id':metric['query_id']}
            entry['state']='complete' if matched else 'failed_correctness'
            if not matched:
                save(prefix+'-'+name+'-mismatch-rows.json',rows)
                raise RuntimeError('Tuning changed q02 typed multiset')
        except Exception as exc:
            entry.update(state='failed_exception',error=str(exc),traceback=traceback.format_exc())
            if (entry.get('qa') or {}).get('matched') is False:raise
        finally:save(prefix+'.json',results)
    SETTINGS.clear();SETTINGS.update(base)
    validated=all(e['state']=='complete' and (e.get('qa') or {}).get('matched') is True and e.get('settings_verified') is True and len(e['runs'])==3 for e in results.values())
    controls=[results[n] for n in ('original_a','original_b')]
    drift=None
    if all(e['state']=='complete' for e in controls):
        medians=[median(r['seconds'] for r in e['runs']) for e in controls]
        if min(medians)>0:drift=max(medians)/min(medians)
    stable=drift is not None and drift<=POLICY['controls_max_median_ratio']
    for entry in results.values():
        entry['target_outcome']='INCONCLUSIVE'
        if entry['state']=='complete':
            entry['target_outcome']='INCONCLUSIVE_COMPARISON' if not stable else ('PASS' if max(r['seconds'] for r in entry['runs'])<POLICY['target_seconds'] else 'FAIL_LATENCY')
    return {'state':'complete' if validated and stable else 'inconclusive','all_cases_validated':validated,'controls_stable':stable,'control_median_ratio':drift,'policy':POLICY,'cases':results}


def parts(service):
    return service.query_json("SELECT table,name,rows,bytes_on_disk,marks FROM system.parts WHERE database='openalex_benchmark' AND active ORDER BY table,name")


def main():
    global DEADLINE,SPILL_SUPPORTED
    config=json.loads((BASE/'selection.json').read_text());validate_scope(config)
    DEADLINE=monotonic()+max(0,(datetime.fromisoformat(config['work_deadline_at'])-datetime.now(timezone.utc)).total_seconds())
    save('decision-policy.json',POLICY)
    mount_raw(config)
    # Exercise the exact case loop, real query_log/settings/telemetry and SQL on
    # three fixture Works before paying for the full 31.9m load on this same VM.
    fixture(config['optimized_sql'])
    service=start_service(ROOT)
    try:
        env=service.environment_evidence()
        if config['image_digest'] not in env['repo_digests']:raise RuntimeError('Tuning image differs from matched baseline')
        save('environment.json',env)
        if service.query_value("SELECT count() FROM system.events WHERE event='ExternalProcessingCompressedBytesTotal' SETTINGS system_events_show_zero_values=1")!='1':raise RuntimeError('Supported spill counter missing')
        SPILL_SUPPORTED=True
        counts={e:sum(f['rows'] for f in config['files'] if f['entity']==e) for e in ('authors','institutions','sources','topics')}
        save('status.json',{'state':'loading_dimensions'})
        started=monotonic();dimension_counts,dimension_storage=_prepare_stage2_dimensions(service,root=ROOT,database='openalex_benchmark',expected_counts=counts,result_dir=OUT/'dimensions');dimension_seconds=monotonic()-started
        save('status.json',{'state':'loading_works'})
        started=monotonic();correctness,profile,storage=_load_stage2_tier(service,root=ROOT,database='openalex_benchmark',tier='stage2_large',expected_rows=31885241,result_dir=OUT/'tier',minimum_ordinary_author_reference_coverage=.999);load_seconds=monotonic()-started
        save('build.json',{'dimensions_seconds':dimension_seconds,'works_seconds':load_seconds,'counts':dimension_counts,'correctness':correctness,'profile':profile,'dimension_storage':dimension_storage,'work_storage':storage})
        if correctness['normalized_sha256']!=config['expected_normalized_sha256']:raise RuntimeError('Tuning normalized tables differ from baseline')
        topic=service.query_json('SELECT count() AS n,uniqExact(topic_id) AS u FROM openalex_benchmark.topics')[0]
        if int(topic['n'])!=int(topic['u']):raise RuntimeError('Topic names are not unique per topic ID')
        for _ in range(300):
            if service.query_value("SELECT count() FROM system.merges WHERE database='openalex_benchmark'")=='0':break
            sleep(2)
        else:raise RuntimeError('Tuning merges did not become quiescent')
        service.execute_script('SYSTEM STOP MERGES')
        if service.query_value("SELECT count() FROM system.merges WHERE database='openalex_benchmark'")!='0':raise RuntimeError('Merge started before tuning')
        save('parts-before.json',parts(service))
        original=catalog(ROOT,'openalex_benchmark',config['seeds'])['q02'];optimized=config['optimized_sql'].replace('openalex_spike','openalex_benchmark')
        save('tuning-queries.json',{'original':original,'preaggregate':optimized})
        result=run_cases(service,original,optimized,config['expected_q02_sha256'],config['expected_q02_rows'])
        save('parts-after.json',parts(service))
        result.update(experiment='targeted_q02',normalized_sha256=correctness['normalized_sha256'],expected_q02_sha256=config['expected_q02_sha256'],source_identity=manifest_identity(config))
        save('summary.json',result)
        save('status.json',{'state':'complete','experiment_outcome':result['state']})
    except BaseException as exc:
        save('status.json',{'state':'failed','error':str(exc),'traceback':traceback.format_exc()});raise
    finally:
        service.down();run(['umount',str(ROOT/'.data/raw')],check=False);run(['umount',str(MOUNT)],check=False)


if __name__=='__main__':main()
