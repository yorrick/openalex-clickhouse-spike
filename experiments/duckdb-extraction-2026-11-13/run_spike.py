"""Throwaway local extraction experiment. No AWS authentication, compute or writes."""
from pathlib import Path
import os,sys,json,time,hashlib,resource,subprocess,statistics,datetime,decimal,math,base64,threading
S=Path(__file__).resolve().parent
for k in list(os.environ):
    if k.startswith('AWS_'): os.environ.pop(k)
(S/'empty-secrets').mkdir(exist_ok=True)
(S/'empty-aws-config').touch(exist_ok=True)
os.environ.update(AWS_CONFIG_FILE=str(S/'empty-aws-config'),AWS_SHARED_CREDENTIALS_FILE=str(S/'empty-aws-config'),AWS_EC2_METADATA_DISABLED='true')
P=json.loads((S/'input.json').read_text()); URI=P['file']['url']; N=P['file']['meta']['content_length']; KEY=URI.split('s3://openalex/')[1]
def dump(name,x): (S/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def lit(x):return "'"+str(x).replace("'","''")+"'"
def cpu():
    r=resource.getrusage(resource.RUSAGE_SELF);return r.ru_utime+r.ru_stime
def connection(profile=None):
    import duckdb
    c=duckdb.connect(config={'secret_directory':str(S/'empty-secrets'),'allow_persistent_secrets':False,'autoload_known_extensions':False,'autoinstall_known_extensions':False})
    c.execute('LOAD httpfs')
    for q in ["SET enable_global_s3_configuration=false","SET httpfs_enable_credential_refresh=false","SET enable_external_file_cache=false","SET enable_http_metadata_cache=false","SET merge_http_secret_into_s3_request=false","SET threads=8","SET memory_limit='8GB'",f"SET temp_directory={lit(S/'spill')}"] : c.execute(q)
    c.execute("CREATE SECRET openalex_anonymous(TYPE s3,PROVIDER config,KEY_ID '',SECRET '',SESSION_TOKEN '',REGION 'us-east-1',ENDPOINT 's3.us-east-1.amazonaws.com',SCOPE 's3://openalex',REQUESTER_PAYS false)")
    c.execute("CALL enable_logging('HTTP',storage='memory',storage_buffer_size=0)")
    if profile:
        c.execute("SET enable_profiling='json'");c.execute('SET profiling_output='+lit(profile))
    return c

def child(mode,run):
    started=time.perf_counter();out=S/'outputs'/f'{mode}-{run}.parquet';out.parent.mkdir(exist_ok=True)
    c=connection(S/f'{mode}-{run}-profile.json');setup=time.perf_counter()-started
    src=S/'raw.parquet' if mode.startswith('local_') else URI
    columns='id, publication_year' if mode.endswith('narrow') else '*'
    sql=f'COPY (SELECT {columns} FROM read_parquet({lit(src)},hive_partitioning=false) WHERE publication_year=2018) TO {lit(out)} (FORMAT PARQUET,COMPRESSION ZSTD)'
    (S/f'{mode}-{run}.sql').write_text(sql+';\n')
    t=time.perf_counter();u=cpu();count=c.execute(sql).fetchone()[0];elapsed=time.perf_counter()-t;cpus=cpu()-u;c.execute('PRAGMA disable_profiling')
    logs=[{'request':json.loads(a),'response':json.loads(b)} for a,b in c.execute("SELECT to_json(request),to_json(response) FROM duckdb_logs_parsed('HTTP')").fetchall()]
    transferred=0;get=0;head=0
    for z in logs:
        req,resp=z['request'],z['response'];headers={k.lower():v for k,v in req['headers'].items()}
        assert not {'authorization','x-amz-security-token'}&headers.keys(), 'Authentication header observed'
        assert not any(x in req['url'].lower() for x in ['x-amz-credential','x-amz-signature','x-amz-security-token'])
        assert resp['status'] in ['OK_200','PartialContent_206'],resp['status']
        if req['type']=='GET':
            n=int(next(v for k,v in resp['headers'].items() if k.lower()=='content-length'));transferred+=n;get+=1
        elif req['type']=='HEAD':head+=1
        else:raise RuntimeError('Unexpected remote operation '+req['type'])
    dump(f'{mode}-{run}-http.json',logs)
    record={'mode':mode,'run':run,'source':str(src),'sql':sql,'rows_written':count,'copy_seconds':elapsed,'setup_seconds':setup,'process_seconds_so_far':time.perf_counter()-started,'query_cpu_seconds':cpus,'average_busy_cores':cpus/elapsed,'process_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'s3_successful_get_payload_bytes':transferred,'s3_get_requests':get,'s3_head_requests':head,'payload_ratio_to_full_object':transferred/N,'no_authentication_headers':True,'output_file':str(out),'output_bytes':out.stat().st_size,'settings':dict(c.execute("SELECT name,value FROM duckdb_settings() WHERE name IN ('threads','memory_limit','enable_global_s3_configuration','httpfs_enable_credential_refresh','enable_external_file_cache','secret_directory')").fetchall()),'peak_rss_scope':'Fresh macOS process including extension/setup/COPY; ru_maxrss is bytes on macOS','payload_scope':'Sum Content-Length of successful GET responses; excludes HEAD bodies, HTTP/TLS overhead. No failed HTTP responses observed.'}
    dump(f'{mode}-{run}.json',record);c.close();print(json.dumps({k:record[k] for k in ['mode','run','rows_written','copy_seconds','s3_successful_get_payload_bytes','output_bytes']}),flush=True)

def canonical(x):
    if isinstance(x,dict):return {k:canonical(v) for k,v in sorted(x.items())}
    if isinstance(x,(list,tuple)):return [canonical(v) for v in x]
    if isinstance(x,(datetime.datetime,datetime.date,datetime.time)):return {'__datetime__':x.isoformat()}
    if isinstance(x,decimal.Decimal):return {'__decimal__':str(x)}
    if isinstance(x,bytes):return {'__bytes__':base64.b64encode(x).decode()}
    if isinstance(x,float) and not math.isfinite(x):return {'__float__':str(x)}
    return x

def value_hash(path,narrow=False,raw=False):
    import pyarrow.parquet as pq
    import pyarrow.compute as pc
    f=pq.ParquetFile(path);hashes=[]
    for batch in f.iter_batches(batch_size=512,columns=['id','publication_year'] if narrow else None):
        if raw:batch=batch.filter(pc.equal(batch.column(batch.schema.get_field_index('publication_year')),2018))
        for row in batch.to_pylist():
            if not raw:assert row['publication_year']==2018
            b=json.dumps(canonical(row),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode();hashes.append(hashlib.sha256(b).digest())
    return {'rows':len(hashes),'canonical_multiset_sha256':hashlib.sha256(b''.join(sorted(hashes))).hexdigest(),'column_names': ['id','publication_year'] if narrow else f.schema_arrow.names}

def main():
    import boto3,psutil,shutil
    from botocore import UNSIGNED
    from botocore.config import Config
    assert sys.platform=='darwin','RSS unit convention requires macOS'
    assert shutil.disk_usage(S).free>50*2**30
    client=boto3.client('s3',region_name='us-east-1',config=Config(signature_version=UNSIGNED,max_pool_connections=8))
    def check_request(request,**kw):
        assert not any(k.lower() in ['authorization','x-amz-security-token'] for k in request.headers),'Signed SDK request'
    client.meta.events.register('before-send.s3.*',check_request)
    h=client.head_object(Bucket='openalex',Key=KEY);assert h['ContentLength']==N
    etag=h['ETag'];dump('source-head-before.json',{k:h.get(k) for k in ['ContentLength','ETag','VersionId','LastModified']})
    print('Baseline: unsigned full GetObject of',N,'bytes',flush=True)
    t=time.perf_counter();u=cpu();resp=client.get_object(Bucket='openalex',Key=KEY,IfMatch=etag);assert resp['ContentLength']==N;seen=0;digest=hashlib.sha256()
    with (S/'raw.parquet').open('wb') as f:
        for block in resp['Body'].iter_chunks(chunk_size=4*2**20):
            f.write(block);digest.update(block);seen+=len(block)
        f.flush();os.fsync(f.fileno())
    resp['Body'].close();elapsed=time.perf_counter()-t;assert seen==N
    dump('baseline-download.json',{'s3_get_payload_bytes':seen,'download_and_file_fsync_seconds':elapsed,'cpu_seconds':cpu()-u,'sha256':digest.hexdigest(),'count':1,'no_authentication':True,'includes':'GetObject, writing local file, SHA256 streaming and fsync','not_includes':'SDK creation and HEAD request'})
    print('Baseline complete',round(elapsed,3),'s',flush=True)
    results=[];total=seen
    for mode in ['local_narrow','local_full','s3_narrow','s3_full']:
        for run in range(1,4):
            assert shutil.disk_usage(S).free>50*2**30
            assert total<3*2**30
            print('START',mode,run,flush=True);pt=time.perf_counter();proc=subprocess.Popen([sys.executable,__file__,'child',mode,str(run)],cwd=S,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=os.environ.copy());samples=[]
            while proc.poll() is None:
                try:
                    pp=psutil.Process(proc.pid);rss=pp.memory_info().rss;samples.append({'at_seconds':time.perf_counter()-pt,'rss_bytes':rss,'cpu_seconds':sum(pp.cpu_times()[:2])})
                    if rss>12*2**30 or time.perf_counter()-pt>240:proc.kill();raise RuntimeError('Process RSS/time limit')
                except psutil.NoSuchProcess:pass
                time.sleep(.1)
            stdout,stderr=proc.communicate();(S/f'{mode}-{run}.stderr').write_text(stderr);assert proc.returncode==0,(mode,run,stderr[-1800:])
            z=json.loads((S/f'{mode}-{run}.json').read_text());z['parent_process_wall_seconds']=time.perf_counter()-pt;dump(f'{mode}-{run}.json',z);dump(f'{mode}-{run}-resource-samples.json',samples);results.append(z);total+=z['s3_successful_get_payload_bytes'];print(stdout.strip(),flush=True)
    end=client.head_object(Bucket='openalex',Key=KEY);assert end['ETag']==etag and end['ContentLength']==N
    dump('source-head-after.json',{k:end.get(k) for k in ['ContentLength','ETag','VersionId','LastModified']})
    assert total<3*2**30,total
    print('Verifying rows and nested values independently through PyArrow',flush=True)
    refs={}
    for narrow in [True,False]:
        key='narrow' if narrow else 'full';refs[key]=value_hash(S/'raw.parquet',narrow=narrow,raw=True);assert refs[key]['rows']>0
    for z in results:
        narrow=z['mode'].endswith('narrow');ref=refs['narrow' if narrow else 'full'];v=value_hash(z['output_file'],narrow=narrow);assert v==ref,(z['mode'],z['run'],v,ref);z['independent_value_qa']=v;dump(f"{z['mode']}-{z['run']}.json",z)
    summary={'input':P,'baseline_download':json.loads((S/'baseline-download.json').read_text()),'variants':{},'all_row_values_match_pyarrow_raw_reference':True,'reference':refs,'s3_source_etag_unchanged':True,'total_successful_s3_get_payload_bytes':total,'all_data_local':True,'aws_account_used':False,'cache_scope':'Each query runs in a fresh process with DuckDB external-file cache disabled; local source is likely OS-cache resident after download. OS caches were not cleared. Network/S3 caches uncontrolled.'}
    for mode in ['local_narrow','local_full','s3_narrow','s3_full']:
        cases=[z for z in results if z['mode']==mode];summary['variants'][mode]={'repeat':3,'copy_seconds':[z['copy_seconds'] for z in cases],'median_copy_seconds':statistics.median(z['copy_seconds'] for z in cases),'get_payload_bytes':[z['s3_successful_get_payload_bytes'] for z in cases],'get_requests':[z['s3_get_requests'] for z in cases],'output_bytes':[z['output_bytes'] for z in cases],'rows':cases[0]['rows_written'],'peak_process_rss_bytes':max(z['process_peak_rss_bytes'] for z in cases),'average_busy_cores':[z['average_busy_cores'] for z in cases]}
    for mode,target in [('s3_narrow',.10),('s3_full',.25)]:summary['variants'][mode]['predeclared_transfer_target']=target;summary['variants'][mode]['target_met_all_runs']=all(v/N<=target for v in summary['variants'][mode]['get_payload_bytes'])
    dump('summary.json',summary);print(json.dumps(summary['variants'],indent=2),flush=True)
if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='child':child(sys.argv[2],int(sys.argv[3]))
    else:main()
