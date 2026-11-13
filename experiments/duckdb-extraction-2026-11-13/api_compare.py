"""Anonymous same-requested-ID API retrieval throughput; live data, not snapshot equality."""
from pathlib import Path
import concurrent.futures,threading,time,json,gzip,hashlib,resource,urllib.parse
import urllib3
S=Path(__file__).resolve().parent;ids=json.loads((S/'api-selected-ids.json').read_text());assert len(ids)==len(set(ids))==17644
batches=[ids[i:i+100] for i in range(0,len(ids),100)];probe=json.loads((S/'api-100-id-probe.json').read_text());expected_cost=probe['meta']['cost_usd'];assert expected_cost*len(batches)*3<=.06
lock=threading.Lock();next_start=0.;total_budget=0.
def run(repeat):
 global next_start,total_budget
 folder=S/'api-comparison'/f'run-{repeat}';folder.mkdir(parents=True,exist_ok=True);http=urllib3.PoolManager(num_pools=2,maxsize=4,block=True,cert_reqs='CERT_REQUIRED');next_start=0.;records=[];pages=[];wall=time.perf_counter();u=resource.getrusage(resource.RUSAGE_SELF);fail=None
 def fetch(item):
  global next_start,total_budget
  index,batch=item
  with lock:
   delay=max(0.,next_start-time.perf_counter());start=time.perf_counter()+delay;next_start=start+.21
  if delay:time.sleep(delay)
  query={'filter':'openalex_id:'+'|'.join(x.rsplit('/',1)[-1] for x in batch),'per_page':100,'corpus':'all'};url='https://api.openalex.org/works?'+urllib.parse.urlencode(query);st=time.perf_counter()
  r=http.request('GET',url,headers={'Accept-Encoding':'gzip','User-Agent':'OpenAlex-local-extraction-comparison/1.0'},preload_content=False,decode_content=False,retries=False,timeout=urllib3.Timeout(total=30))
  body=r.read(16*1024*1024+1,decode_content=False);encoding=r.headers.get('Content-Encoding');status=r.status;r.release_conn();assert len(body)<=16*1024*1024
  if status!=200:
   (folder/f'error-{index}.bin').write_bytes(body);raise RuntimeError(f'HTTP {status}, batch {index}; no credential or paid-budget switch')
  raw=gzip.decompress(body) if encoding=='gzip' else body;z=json.loads(raw);cost=z['meta'].get('cost_usd',0)
  with lock:
   total_budget+=cost;assert total_budget<=.061,(total_budget,'free allowance pacing budget exceeded')
  (folder/f'page-{index:03}.body'+Path('.gz') if False else folder/f'page-{index:03}.body').write_bytes(body)
  receipt={'batch':index,'requested_ids':batch,'status':status,'seconds':time.perf_counter()-st,'encoding':encoding,'http_body_bytes':len(body),'decoded_json_bytes':len(raw),'returned_records':len(z['results']),'meta_count':z['meta'].get('count'),'cost_usd_from_api':cost}
  (folder/f'page-{index:03}.json').write_text(json.dumps(receipt,indent=2)+'\n');return receipt,z['results']
 try:
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
   with (folder/'records.jsonl').open('w') as out:
    for page,rows in pool.map(fetch,enumerate(batches)):
     pages.append(page);records.extend(rows)
     for row in rows:out.write(json.dumps(row,separators=(',',':'),ensure_ascii=False)+'\n')
     if len(pages)%30==0:print('API',repeat,'batches',len(pages),'records',len(records),'elapsed',round(time.perf_counter()-wall,2),flush=True)
 except Exception as e:fail=str(e)
 elapsed=time.perf_counter()-wall;v=resource.getrusage(resource.RUSAGE_SELF);http.clear();got=[x['id'] for x in records];wanted=set(ids);unique=set(got)
 result={'repeat':repeat,'requested_count':len(ids),'returned_rows':len(got),'returned_distinct_ids':len(unique),'missing_requested_ids':sorted(wanted-unique),'extra_ids':sorted(unique-wanted),'duplicate_row_count':len(got)-len(unique),'all_returned_publication_year_2018':all(x.get('publication_year')==2018 for x in records),'pages_completed':len(pages),'total_pages':len(batches),'export_wall_seconds':elapsed,'process_cpu_seconds':v.ru_utime+v.ru_stime-u.ru_utime-u.ru_stime,'peak_rss_bytes':v.ru_maxrss,'successful_http_body_bytes':sum(x['http_body_bytes'] for x in pages),'decoded_response_bytes':sum(x['decoded_json_bytes'] for x in pages),'records_jsonl_bytes':(folder/'records.jsonl').stat().st_size,'free_budget_cost_usd_from_api':sum(x['cost_usd_from_api'] for x in pages),'free_budget_total_across_repeats':total_budget,'all_requests_anonymous':True,'concurrency':4,'request_start_spacing_seconds':.21,'connection_pooling':True,'error':fail,'returned_id_multiset_sha256':hashlib.sha256('\n'.join(sorted(got)).encode()).hexdigest(),'field_names':sorted({k for x in records for k in x}),'scope':'Known IDs, no discovery/cursor cost. Current API values and fields differ from fixed snapshot. JSONL output; not the same Parquet schema. Metered cost consumes anonymous free allowance, not paid credits or AWS. Timed path includes HTTP, gzip decompression, JSON parsing and JSONL writing.'}
 (folder/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['repeat','returned_rows','pages_completed','export_wall_seconds','successful_http_body_bytes','free_budget_cost_usd_from_api','error']}),flush=True)
 if fail:raise RuntimeError(fail)
 return result
if __name__=='__main__':
 results=[run(i) for i in range(1,4)];(S/'api-comparison-summary.json').write_text(json.dumps({'runs':results,'snapshot_requested_ids':len(ids),'not_same_snapshot_values':True},indent=2)+'\n')
