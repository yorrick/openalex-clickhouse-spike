"""Bounded one-shard, one-pass publication-year repartitioning experiment."""
import json,time,sys,resource,subprocess,hashlib
from pathlib import Path
import psutil
import pyarrow.parquet as pq
import run_spike as probe
S=probe.S

def digest(paths,columns=None):
 hashes=[];names=None;rows=0
 for path in paths:
  f=pq.ParquetFile(path);names=columns or f.schema_arrow.names
  for batch in f.iter_batches(batch_size=512,columns=columns):
   for row in batch.to_pylist():
    hashes.append(hashlib.sha256(json.dumps(probe.canonical(row),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).digest());rows+=1
 return {'rows':rows,'canonical_multiset_sha256':hashlib.sha256(b''.join(sorted(hashes))).hexdigest(),'columns':sorted(names)}

if len(sys.argv)>1:
 run=int(sys.argv[1]);folder=S/f'year-partitions-{run}';c=probe.connection(S/f'year-partitions-{run}-profile.json');c.execute("SET max_temp_directory_size='4GB'")
 sql=f"COPY (SELECT * FROM read_parquet({probe.lit(S/'raw.parquet')},hive_partitioning=false)) TO {probe.lit(folder)} (FORMAT PARQUET, COMPRESSION ZSTD, PARTITION_BY (publication_year), WRITE_PARTITION_COLUMNS true)"
 (S/f'year-partitions-{run}.sql').write_text(sql+';\n');t=time.perf_counter();u=probe.cpu();n=c.execute(sql).fetchone()[0];wall=time.perf_counter()-t;cpu=probe.cpu()-u;c.execute('PRAGMA disable_profiling');files=sorted(folder.rglob('*.parquet'));selected=sorted((folder/'publication_year=2018').glob('*.parquet'));record={'run':run,'copy_seconds':wall,'cpu_seconds':cpu,'average_busy_cores':cpu/wall,'peak_process_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'rows_copied':n,'files':len(files),'year_partitions':len(list(folder.glob('publication_year=*'))),'output_bytes':sum(f.stat().st_size for f in files),'year2018_files':len(selected),'year2018_bytes':sum(f.stat().st_size for f in selected),'http_requests':c.execute("SELECT count(*) FROM duckdb_logs_parsed('HTTP')").fetchone()[0],'scope':'Cached local source, one pass copying all400000records/all51columns; no remote reads. Partition column is also stored in each Parquet file.'};assert n==400000 and record['http_requests']==0;probe.dump(f'year-partitions-{run}.json',record);c.close();print(json.dumps(record),flush=True)
else:
 assert (S/'default-cache-summary.json').exists(),'Finish remote timing before local repartition job'
 cases=[]
 for run in range(1,4):
  p=subprocess.Popen([sys.executable,__file__,str(run)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);t=time.monotonic()
  while p.poll() is None:
   try:
    if psutil.Process(p.pid).memory_info().rss>12*2**30 or time.monotonic()-t>240:p.kill();raise RuntimeError('Resource guard')
   except psutil.NoSuchProcess:pass
   time.sleep(.1)
  out,err=p.communicate();(S/f'year-partitions-{run}.stderr').write_text(err);assert p.returncode==0,err[-2000:];print(out.strip(),flush=True);cases.append(json.loads((S/f'year-partitions-{run}.json').read_text()))
 print('Verifying partitioned output values',flush=True);expected=json.loads((S/'summary.json').read_text())['reference']['full'];source_ids=digest([S/'raw.parquet'],['id','publication_year']);source_full=None
 for run in range(1,4):
  folder=S/f'year-partitions-{run}';allfiles=sorted(folder.rglob('*.parquet'));selected=sorted((folder/'publication_year=2018').glob('*.parquet'));idqa=digest(allfiles,['id','publication_year']);assert idqa==source_ids
  qa=digest(selected);assert qa['rows']==expected['rows'] and qa['canonical_multiset_sha256']==expected['canonical_multiset_sha256'] and qa['columns']==sorted(expected['column_names'])
  if run==1:
   source_full=digest([S/'raw.parquet']);assert digest(allfiles)==source_full
  cases[run-1]['all_id_year_values_match']=True;cases[run-1]['all_2018_record_values_match']=True
 probe.dump('partition-local-summary.json',{'runs':cases,'source_id_year_qa':source_ids,'all_source_full_value_qa_run1':source_full,'all_id_year_values_match_all3':True,'all_2018_record_values_match_all3':True,'full400000_record_values_checked_in_run1_only':True})
