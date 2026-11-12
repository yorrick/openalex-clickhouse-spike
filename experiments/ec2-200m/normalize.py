from pathlib import Path
import concurrent.futures,time,json,hashlib,threading
import boto3,pyarrow.parquet as pq
from botocore import UNSIGNED
from botocore.config import Config
from helpers import HERE,dump,sha,guard,duck
MAN=json.loads((HERE/'input-manifest.json').read_text());T=json.loads((HERE/'projection-templates.json').read_text())
PUB=boto3.client('s3',region_name='us-east-1',config=Config(signature_version=UNSIGNED,max_pool_connections=16,retries={'max_attempts':5,'mode':'standard'}))

def download(f):
 key=f['source_key'];tag=hashlib.sha256(key.encode()).hexdigest();path=HERE/'raw'/f['entity']/(tag+'.parquet');path.parent.mkdir(parents=True,exist_ok=True);proof=HERE/'results/download'/(tag+'.json')
 if proof.exists():
  p=json.loads(proof.read_text());assert p['version_id']==f['version_id'] and path.stat().st_size==f['bytes'] and sha(path)==p['sha256'];return p
 guard();start=time.monotonic();temp=path.with_suffix('.part')
 PUB.download_file('openalex',key,str(temp),ExtraArgs={'VersionId':f['version_id']})
 assert temp.stat().st_size==f['bytes'];h=sha(temp)
 if f.get('known_sha256'):assert h==f['known_sha256'],key
 n=pq.ParquetFile(temp).metadata.num_rows;assert n==f['rows'],(key,n,f['rows']);temp.rename(path)
 p=dict(f,sha256=h,footer_rows=n,path=str(path.relative_to(HERE)),seconds=time.monotonic()-start);dump(proof,p);return p

def main():
 st=time.monotonic()
 if not (HERE/'results/download-complete.json').exists():
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
   for i,p in enumerate(pool.map(download,MAN['inputs'])):
    if i%50==0:print('download',i+1,'/',len(MAN['inputs']),flush=True)
 else:
  sealed=json.loads((HERE/'results/download-complete.json').read_text())
  assert sealed['files']==len(MAN['inputs']) and sealed['bytes']==sum(f['bytes'] for f in MAN['inputs']) and sealed['all_source_sizes_sha256_footer_counts_verified']
  for f in MAN['inputs']:
   tag=hashlib.sha256(f['source_key'].encode()).hexdigest();proof=json.loads((HERE/'results/download'/(tag+'.json')).read_text())
   assert proof['version_id']==f['version_id'] and proof['rows']==f['rows'] and proof['bytes']==f['bytes'] and (HERE/proof['path']).stat().st_size==f['bytes']
  dump(HERE/'results/download-checkpoint-reused.json',{'at':time.time(),'source_full_sha256_recomputed':False,'source_sha256_proofs_reused':True,'sizes_versions_footer_counts_bound_to_manifest':True,'scope':'Resume already completed download phase; no raw data mutation or redownload. Normalized outputs are still individually SHA256 sealed.'})
 sources=[json.loads((HERE/'results/download'/(hashlib.sha256(f['source_key'].encode()).hexdigest()+'.json')).read_text()) for f in MAN['inputs']]
 assert sum(f['rows'] for f in sources if f['entity']=='works')==MAN['works']
 if not (HERE/'results/download-complete.json').exists():dump(HERE/'results/download-complete.json',{'files':len(sources),'bytes':sum(f['bytes'] for f in sources),'seconds':time.monotonic()-st,'all_source_sizes_sha256_footer_counts_verified':True,'works':MAN['works']})
 entities={'works','authors','institutions','sources','topics'}
 selected=[f for f in sources if f['entity'] in entities]
 unused=[f for f in sources if f['entity'] not in entities]
 dump(HERE/'results/source-scope.json',{'normalized_entities':sorted(entities),'normalized_source_files':len(selected),'normalized_source_bytes':sum(f['bytes'] for f in selected),'downloaded_but_unloaded_entities':sorted({f['entity'] for f in unused}),'downloaded_but_unloaded_files':len(unused),'downloaded_but_unloaded_bytes':sum(f['bytes'] for f in unused),'reason':'Input provenance catalog also retains other historical entity files; the authorized benchmark keeps42columns in9tables, not those extra entities.'})
 d=duck();counts={t:0 for t in T['columns']};proofs={t:[] for t in counts}
 for i,f in enumerate(selected):
  entity=f['entity'];tables=['works','work_author','work_institution','work_topic','citation_edge'] if entity=='works' else [entity];tag=hashlib.sha256(f['source_key'].encode()).hexdigest();raw=HERE/f['path']
  for t in tables:
   folder=HERE/'projected'/t;folder.mkdir(parents=True,exist_ok=True);target=folder/(tag+'.parquet');proof=HERE/'results/projected'/t/(tag+'.json')
   if proof.exists():
    p=json.loads(proof.read_text());assert p['source_sha256']==f['sha256'] and sha(target)==p['sha256']
   else:
    guard();start=time.monotonic();sql=T['sql'][t].replace('__INPUT__',str(raw));temp=target.with_suffix('.part')
    d.execute('COPY ('+sql+") TO '"+str(temp)+"' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 122880)")
    n=pq.ParquetFile(temp).metadata.num_rows;temp.rename(target);p={'table':t,'source_key':f['source_key'],'source_sha256':f['sha256'],'rows':n,'bytes':target.stat().st_size,'sha256':sha(target),'sql_sha256':hashlib.sha256(sql.encode()).hexdigest(),'seconds':time.monotonic()-start};dump(proof,p)
   counts[t]+=p['rows'];proofs[t].append(p)
  if i%25==0:print('normalize',i+1,'/',len(sources),counts,flush=True)
 d.close();assert counts['works']==MAN['works'];assert counts['authors']==119129660
 dump(HERE/'results/projection-complete.json',{'counts':counts,'tables':{t:{'files':len(ps),'bytes':sum(x['bytes'] for x in ps),'rows':counts[t]} for t,ps in proofs.items()},'seconds_since_download_start':time.monotonic()-st,'shared_payloads':True})
 print('NORMALIZATION COMPLETE',counts,flush=True)
if __name__=='__main__':main()
