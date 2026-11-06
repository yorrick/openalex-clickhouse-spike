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


def fixture():
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
        sqls=catalog(root,'openalex_fixture',[1])
        rows={name:query(service,sql,output=True)[0] for name,sql in sqls.items()}
        if any(not value for value in rows.values()) or rows['q06-s1'][0]['second_hop_works']<1:
            raise RuntimeError('Fixture query catalog unexpectedly empty')
        save('fixture.json',{'passed':True,'counts':counts,'correctness':correctness,'rows':rows})
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
        return [],{'query_id':qid,'state':'timeout','seconds_lower_bound':300}
    finally:
        stop.set()
        if collect:
            thread.join(); samples.append(sample(cgroup))
    service.execute_script('SYSTEM FLUSH LOGS')
    metrics=service.query_json(f"SELECT type,query_duration_ms/1000.0 AS seconds,read_rows,read_bytes,result_rows,memory_usage AS peak_memory_bytes,ProfileEvents FROM system.query_log WHERE query_id='{qid}' AND type IN ('QueryFinish','ExceptionWhileProcessing','ExceptionBeforeStart') ORDER BY event_time_microseconds DESC LIMIT 1")
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
    if p.returncode and record['state'] not in ('timeout','memory_limit_exceeded'):
        raise RuntimeError('ClickHouse query failed: '+p.stderr[-3000:])
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


def main():
    global DEADLINE,SPILL_SUPPORTED
    primary_settings=dict(SETTINGS)
    config=json.loads((BASE/'selection.json').read_text())
    validate_scope(config)
    DEADLINE=monotonic()+max(0,(datetime.fromisoformat(config['work_deadline_at'])-datetime.now(timezone.utc)).total_seconds())
    if platform.machine()!='aarch64' or os.geteuid()!=0:
        raise RuntimeError('Expected root on native ARM64')
    save('status.json',{'state':'fixture'})
    if config['tier']=='stage2_small':
        fixture()
    mount_raw(config)
    # Root disk calibration is read-only against a temporary scratch file on CH disk.
    path=BASE/'fio-control.bin'
    write_control=run(['fio','--name=write-control','--filename='+str(path),'--size=1G','--rw=write','--bs=1M','--direct=1','--iodepth=16','--ioengine=libaio','--end_fsync=1','--output-format=json'])
    before=sample(Path('/sys/fs/cgroup'))
    control=run(['fio','--name=read-control','--filename='+str(path),'--size=1G','--rw=read','--bs=1M','--direct=1','--iodepth=16','--ioengine=libaio','--runtime=8','--time_based','--readonly','--output-format=json'])
    save('disk-control.json',{'read':json.loads(control.stdout),'write':json.loads(write_control.stdout),'before':before,'after':sample(Path('/sys/fs/cgroup'))}); path.unlink()
    service=start_service(ROOT)
    try:
        save('environment.json',service.environment_evidence())
        if service.query_value("SELECT count() FROM system.events WHERE event='ExternalProcessingCompressedBytesTotal' SETTINGS system_events_show_zero_values=1")!='1':
            raise RuntimeError('Required spill counter absent')
        SPILL_SUPPORTED=True
        save('counter-availability.json',{'ExternalProcessingCompressedBytesTotal':True,'absent_query_event_means_zero_only_after_supported_counter_check':True})
        config_files={f['key']:f for f in config['files']}
        expected={e:sum(f['rows'] for f in config['files'] if f['entity']==e) for e in ('authors','institutions','sources','topics')}
        save('status.json',{'state':'loading_dimensions','tier':config['tier']})
        started=monotonic()
        counts,dimension_samples=_prepare_stage2_dimensions(service,root=ROOT,database='openalex_benchmark',expected_counts=expected,result_dir=OUT/'dimensions')
        dimensions_seconds=monotonic()-started
        save('status.json',{'state':'loading_works','tier':config['tier']})
        started=monotonic()
        correctness,profile,storage=_load_stage2_tier(service,root=ROOT,database='openalex_benchmark',tier=config['tier'],expected_rows=config['tiers'][config['tier']]['work_rows'],result_dir=OUT/'tier',minimum_ordinary_author_reference_coverage=.999)
        load_seconds=monotonic()-started
        save('build.json',{'dimensions_seconds':dimensions_seconds,'works_seconds':load_seconds,'counts':counts,'correctness':correctness,'profile':profile,'dimension_storage':dimension_samples,'work_storage':storage})
        panel=seeds(service,config)
        sqls=catalog(ROOT,'openalex_benchmark',panel)
        save('queries.json',sqls)
        merge_started=monotonic(); stable=0; merges_quiescent=False
        while monotonic()-merge_started<600 and monotonic()+330<DEADLINE:
            active=int(service.query_value("SELECT count() FROM system.merges WHERE database='openalex_benchmark'"))
            stable=stable+1 if active==0 else 0
            if stable>=3:
                merges_quiescent=True;break
            sleep(2)
        service.execute_script('SYSTEM STOP MERGES')
        if int(service.query_value("SELECT count() FROM system.merges WHERE database='openalex_benchmark'"))!=0:
            merges_quiescent=False
        save('merge-state.json',{'quiescent':merges_quiescent,'wait_seconds':monotonic()-merge_started})
        plans={}
        for name,sql in sqls.items():
            if name[:3] not in plans:
                plans[name[:3]]=service._compose(['exec','-T','clickhouse',*service._client_command('--format=TabSeparatedRaw')],input_text='EXPLAIN PLAN '+sql)
        save('query-plans.json',plans)
        timings={name:[] for name in sqls}; blocked=set()
        for block in range(4):
            for name,sql in sqls.items():
                if name in blocked:
                    continue
                if monotonic()+330>DEADLINE:
                    blocked.add(name); continue
                save('status.json',{'state':'querying','tier':config['tier'],'query':name,'block':block})
                _,metrics=query(service,sql,collect=True)
                metrics['block']='primer' if block==0 else 'warm'+str(block)
                timings[name].append(metrics)
                if metrics['state']!='complete':
                    blocked.add(name)
                save('timings.json',timings)
        qa={};qa_rows={}
        for name,sql in sqls.items():
            if name in blocked or monotonic()+330>DEADLINE:
                continue
            rows,metrics=query(service,sql,output=True)
            if metrics['state']!='complete':
                blocked.add(name);continue
            if not rows:
                raise RuntimeError(name+' QA result unexpectedly empty')
            save(name+'-rows.json',rows)
            qa[name]={'rows':len(rows),'query':metrics['query_id']}
            qa_rows[name]=rows
        graph=[]
        for seed in panel:
            one=qa_rows.get('q05-s'+str(seed));two=qa_rows.get('q06-s'+str(seed))
            graph.append({'seed':seed,'outgoing':sum(r['direction']=='outgoing' for r in one) if one else None,'incoming':sum(r['direction']=='incoming' for r in one) if one else None,'second_hop':int(two[0]['second_hop_works']) if two else None})
        sizes=service.query_json("SELECT table,sum(bytes_on_disk) AS bytes,sum(rows) AS rows,count() AS active_parts,sum(data_uncompressed_bytes) AS uncompressed_bytes FROM system.parts WHERE active AND database='openalex_benchmark' GROUP BY table ORDER BY table")
        summary={'state':'complete','primary_complete':True,'tier':config['tier'],'seeds':panel,'graph':graph,'timings':timings,'qa':qa,'table_bytes':sizes,'load_seconds':load_seconds,'dimensions_seconds':dimensions_seconds,'blocked_queries':sorted(blocked),'settings':primary_settings,'merges_quiescent':merges_quiescent,'cold_tests':{},'variants':{},'optional_phase':'not_completed'}
        save('summary.json',summary)
        save('status.json',{'state':'primary_complete','tier':config['tier']})
        cold={};variants={};optional_error=None
        try:
            cold={}
            for name,sql in sqls.items():
                if name in blocked or monotonic()+330>DEADLINE:
                    continue
                service.execute_script('SYSTEM DROP MARK CACHE; SYSTEM DROP UNCOMPRESSED CACHE')
                run(['sync'])
                Path('/proc/sys/vm/drop_caches').write_text('3\n')
                _,metrics=query(service,sql,collect=True)
                cold[name]=metrics
                save('cold.json',cold)
            variants={}
            if config.get('run_resource_variants',False):
                candidates=[(name,max(r.get('seconds',0) for r in runs if r.get('block')!='primer')) for name,runs in timings.items() if name not in blocked and len(runs)==4]
                if candidates and monotonic()+15*60<DEADLINE:
                    target=max(candidates,key=lambda item:item[1])[0]
                    warm=timings[target][-1]
                    events=warm.get('ProfileEvents',{})
                    cpu=(events.get('UserTimeMicroseconds',0)+events.get('SystemTimeMicroseconds',0))/max(1,warm.get('seconds',1)*18*1e6)
                    if cpu>=.7:
                        variants['cpu']={'target':target,'cpu_fraction':cpu,'blocks':[]}
                        for count in (18,32,18):
                            if monotonic()+330>DEADLINE:
                                break
                            run(['docker','update','--cpus',str(count),service.container_id()])
                            query(service,sqls[target],cpus=count)
                            block=[]
                            for _ in range(3):
                                if monotonic()+330>DEADLINE:
                                    break
                                _,metrics=query(service,sqls[target],cpus=count,collect=True); block.append(metrics)
                            variants['cpu']['blocks'].append({'cpus':count,'runs':block})
                            save('variants.json',variants)
                        run(['docker','update','--cpus','18',service.container_id()])
                    if warm.get('spill_bytes') is not None and warm['spill_bytes']>0 and monotonic()+15*60<DEADLINE:
                        variants['memory_settings']={'target':target,'blocks':[]}
                        for query_gib,spill_gib in ((12,4),(24,8),(12,4)):
                            if monotonic()+330>DEADLINE:
                                break
                            SETTINGS.update(max_memory_usage=query_gib*GIB,max_bytes_before_external_group_by=spill_gib*GIB,max_bytes_before_external_sort=spill_gib*GIB)
                            query(service,sqls[target])
                            block=[]
                            for _ in range(3):
                                if monotonic()+330>DEADLINE:
                                    break
                                _,metrics=query(service,sqls[target],collect=True); block.append(metrics)
                            variants['memory_settings']['blocks'].append({'query_memory_gib':query_gib,'spill_gib':spill_gib,'runs':block})
                            save('variants.json',variants)
        except Exception as exc:
            optional_error={'error':str(exc),'traceback':traceback.format_exc(),'outcome':'INCONCLUSIVE_OPTIONAL'}
        finally:
            SETTINGS.clear();SETTINGS.update(primary_settings)
        summary.update(cold_tests=cold,variants=variants,optional_phase='failed' if optional_error else 'complete',optional_error=optional_error)
        save('summary.json',summary);save('status.json',{'state':'complete','tier':config['tier']})
    except BaseException as exc:
        save('status.json',{'state':'failed','error':str(exc),'traceback':traceback.format_exc()})
        raise
    finally:
        service.down()
        run(['umount',str(ROOT/'.data/raw')],check=False)
        run(['umount',str(MOUNT)],check=False)


if __name__=='__main__':
    try:
        main()
    except BaseException as exc:
        save('status.json',{'state':'failed','error':str(exc),'traceback':traceback.format_exc()})
        raise
