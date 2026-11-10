"""Normalize retainedfields onAWS, downloadonlyflatParquet, no rawlaptopupload."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib,json,time,shutil,signal,psutil
import duckdb,pyarrow as pa
from athena_reference import Reference,OLD,ACCOUNT
from pg_helpers import HERE,dump
from tier_sql import numeric_id as num
from project_inputs import COLUMNS,sha
import load_data as original

def read(p):return json.loads(p.read_text())
def main():
 r=Reference();assert r.state['setup_complete']
 # Witness actual CTAScompression and workgroup-controlledoutputbeforefull ETL.
 probe=HERE/'results/ctas-probe.json'
 if not probe.exists():
  rec=next((x for x in r.records if x['sql'].startswith('CREATE TABLE pg100_ctas_probe') and x['state']=='SUCCEEDED'),None)
  if rec is None:_,rec=r.query("CREATE TABLE pg100_ctas_probe WITH (format='PARQUET',write_compression='ZSTD') AS SELECT CAST(9007199254740993 AS bigint) AS i,true AS b,'a' AS s",dml_override=True)
  loc=r.glue.get_table(DatabaseName=r.db,Name='pg100_ctas_probe')['Table']['StorageDescriptor']['Location'];assert loc.startswith('s3://'+r.bucket+'/')
  key=loc.split('/',3)[3].rstrip('/')+'/';objects=list(r.s3.get_paginator('list_objects_v2').paginate(Bucket=r.bucket,Prefix=key));fs=[o for page in objects for o in page.get('Contents',[])];assert fs
  path=HERE/'projected/ctas-probe.parquet';r.s3.download_file(r.bucket,fs[0]['Key'],str(path))
  d=duckdb.connect();actual=d.execute('SELECT * FROM read_parquet(?)',[str(path)]).fetchall();assert actual==[(9007199254740993,True,'a')];d.close()
  dump(probe,{'pass':True,'query_id':rec['id'],'location':loc,'downloaded_rows':actual,'workgroup_enforced_location_observed':True,'sha256':sha(path)})
 work=num('w.id');author=num('a.author.id');inst=num('i.id');topic=num('t.id');cited=num('ref');year='CASE WHEN w.publication_year BETWEEN 0 AND 65535 THEN w.publication_year END'
 specs={
 'works':f"SELECT {work} AS work_id,w.id AS canonical_id,{year} AS publication_year,w.type AS work_type,{num('w.primary_location.source.id')} AS source_id,coalesce(w.open_access.is_oa,false) AS is_oa,coalesce(w.is_xpac,false) AS is_xpac,cast(w.cited_by_count AS bigint) AS cited_by_count,{num('w.primary_topic.id')} AS primary_topic_id FROM raw_works w WHERE {work} IS NOT NULL",
 'work_author':f"SELECT {work} AS work_id,{author} AS author_id,a.author_position,coalesce(a.is_corresponding,false) AS is_corresponding FROM raw_works w CROSS JOIN UNNEST(w.authorships) AS u(a) WHERE {work} IS NOT NULL AND {author} IS NOT NULL",
 'work_institution':f"SELECT DISTINCT {work} AS work_id,{author} AS author_id,{inst} AS institution_id FROM raw_works w CROSS JOIN UNNEST(w.authorships) AS u(a) CROSS JOIN UNNEST(a.institutions) AS v(i) WHERE {work} IS NOT NULL AND {author} IS NOT NULL AND {inst} IS NOT NULL",
 'work_topic':f"SELECT {work} AS work_id,{topic} AS topic_id,cast(t.score AS real) AS score,coalesce({topic}={num('w.primary_topic.id')},false) AS is_primary FROM raw_works w CROSS JOIN UNNEST(w.topics) AS u(t) WHERE {work} IS NOT NULL AND {topic} IS NOT NULL AND t.score IS NOT NULL",
 'citation_edge':f"SELECT {work} AS citing_work_id,{cited} AS cited_work_id,min({year}) AS citing_year FROM raw_works w CROSS JOIN UNNEST(w.referenced_works) AS u(ref) WHERE {work} IS NOT NULL AND {cited} IS NOT NULL GROUP BY {work},{cited}"
 }
 # Retained source_id is loaded but unused by7queries, so expose itsrawfieldforthisETLonly.
 columns=r.glue.get_table(DatabaseName=r.db,Name='raw_works')['Table']['StorageDescriptor']['Columns']
 if not any(c['Name']=='primary_location' for c in columns):
  from tier_sql import hive_type
  schema=pa.ipc.read_schema(pa.BufferReader((OLD/'schemas/works.arrow').read_bytes()))
  r.query('ALTER TABLE raw_works ADD COLUMNS (`primary_location` '+hive_type(schema.field('primary_location').type)+')')
 for table,sql in specs.items():
  proof=HERE/'results'/('project-'+table+'.json');done=HERE/'results'/('ctas-'+table+'.json')
  if proof.exists() and read(proof).get('state')=='complete':continue
  if shutil.disk_usage(HERE).free<80*(1<<30):raise RuntimeError('Hostfreebelow80GiB')
  print('Server projecting',table,flush=True);start=time.monotonic()
  if done.exists():rec=read(done);loc=rec['location']
  else:
   ctas='CREATE TABLE projected_'+table+" WITH (format='PARQUET',write_compression='ZSTD') AS "+sql
   (HERE/'sql'/('ctas-'+table+'.sql')).write_text(ctas+';\n')
   _,q=r.query(ctas,dml_override=True,timeout=1800)
   loc=r.glue.get_table(DatabaseName=r.db,Name='projected_'+table)['Table']['StorageDescriptor']['Location'];assert loc.startswith('s3://'+r.bucket+'/')
   rec={'query_id':q['id'],'statistics':q['statistics'],'location':loc};dump(done,rec)
  prefix=loc.split('/',3)[3].rstrip('/')+'/';objs=[o for page in r.s3.get_paginator('list_objects_v2').paginate(Bucket=r.bucket,Prefix=prefix) for o in page.get('Contents',[])];assert objs
  folder=HERE/'projected'/(table+'-parts');folder.mkdir(exist_ok=True)
  def download(o):
   path=folder/Path(o['Key']).name
   if not path.exists() or path.stat().st_size!=o['Size']:r.s3.download_file(r.bucket,o['Key'],str(path))
   assert path.stat().st_size==o['Size'];return {'key':o['Key'],'bytes':o['Size'],'sha256':sha(path),'local_path':str(path)}
  with ThreadPoolExecutor(max_workers=8) as pool:files=list(pool.map(download,objs))
  d=duckdb.connect();d.execute("SET memory_limit='4GB'");d.execute('SET threads=8');d.execute('SET temp_directory=?',[str(HERE/'temp')])
  paths=[f['local_path'] for f in files];target=HERE/'projected'/(table+'.parquet')
  if table=='works' and target.exists() and not (HERE/'projected/works-remote-partial.unsealed').exists():target.rename(HERE/'projected/works-remote-partial.unsealed')
  d.execute("COPY (SELECT * FROM read_parquet(?)) TO ? (FORMAT PARQUET,COMPRESSION ZSTD)",[paths,str(target)])
  n=d.execute('SELECT count(*) FROM read_parquet(?)',[str(target)]).fetchone()[0]
  cols=[x[0] for x in d.execute('DESCRIBE SELECT * FROM read_parquet(?)',[str(target)]).fetchall()];assert cols==COLUMNS[table],(cols,COLUMNS[table])
  d.close();assert n>0
  if table=='works':assert n==100087422
  dump(proof,{'state':'complete','table':table,'rows':n,'bytes':target.stat().st_size,'sha256':sha(target),'columns':cols,'method':'AthenaCTASsamepinnedrawobjects;privateflatpartdownload;localflatconcatenation','ctas':rec,'parts':files,'total_ctas_download_consolidation_seconds':time.monotonic()-start})
  print(table,n,round(time.monotonic()-start,2),'seconds',round(target.stat().st_size/1e9,3),'GB',flush=True)
 # Same local fixed dimensions, not remote CTAS; these were fully SHA-verifiedbefore32m.
 for table in ['authors','institutions','sources','topics']:
  proof=HERE/'results'/('project-'+table+'.json')
  if proof.exists() and read(proof).get('state')=='complete':continue
  print('Projecting fixed dimension',table,flush=True);d=duckdb.connect();d.execute("SET memory_limit='4GB'");d.execute('SET threads=8');d.execute('SET temp_directory=?',[str(HERE/'temp')]);target=HERE/'projected'/(table+'.parquet');body=original.projection(table,'stage2_large');sql='COPY (SELECT * FROM ('+body+') AS normalized('+','.join(COLUMNS[table])+')) TO '+original.lit(str(target))+" (FORMAT PARQUET,COMPRESSION ZSTD)";st=time.monotonic();d.execute(sql);n=d.execute('SELECT count(*) FROM read_parquet(?)',[str(target)]).fetchone()[0];d.close();dump(proof,{'state':'complete','table':table,'rows':n,'bytes':target.stat().st_size,'sha256':sha(target),'columns':COLUMNS[table],'method':'DuckDBsameverifiedlocalfixeddimensions','seconds':time.monotonic()-st});print(table,n,flush=True)
 dump(HERE/'results/projection-complete.json',{'at':time.time(),'tables':list(COLUMNS),'all_sealed':True})
 proc=psutil.Process(30968);assert 'project_inputs.py' in ' '.join(proc.cmdline());proc.send_signal(signal.SIGKILL)
 r.benchmark()

if __name__=='__main__':main()
