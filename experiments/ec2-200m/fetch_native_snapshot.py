"""Read-only bounded progress snapshot; final evidence uses the frozen archive."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,hashlib
from cli_session import certification
HERE=Path(__file__).resolve().parent
c=json.loads((HERE/'cloud-state.json').read_text());s3=certification().client('s3');out=HERE/'native-snapshot';out.mkdir(exist_ok=True)
keys=[]
for engine in ['postgres','clickhouse']:
 for name in ['prepared.json','container.json','storage-after-queries.json','q01.json','q02.json','q03.json','q04.json','q07.json']:
  keys.append(engine+'/'+name)
 for seed in [51557542,24222542,2003585639]:
  for q in ['q05','q06']:keys.append(engine+'/'+q+'-s'+str(seed)+'.json')
 for table in ['works','work_author','work_institution','work_topic','citation_edge','authors','institutions','sources','topics']:keys.append(engine+'/load-'+table+'.json')
for name in ['postgres-cases.json','clickhouse-cases.json','engine-error.json','postgres-selected.json','engines-complete.json']:keys.append(name)
def one(key):
 try:r=s3.get_object(Bucket=c['bucket'],Key='run/results/'+key,ExpectedBucketOwner=c['account'])
 except s3.exceptions.NoSuchKey:return {'key':key,'pending':True}
 data=r['Body'].read();json.loads(data);p=out/key;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 return {'key':key,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
with ThreadPoolExecutor(max_workers=12) as pool:records=list(pool.map(one,keys))
(out/'snapshot-index.json').write_text(json.dumps(records,indent=2)+'\n')
for engine in ['postgres','clickhouse']:
 for name in ['q01','q02','q03','q04','q07','q05-s51557542','q06-s51557542']:
  p=out/engine/(name+'.json')
  if p.exists():
   x=json.loads(p.read_text());print(engine,name,x.get('state'),x.get('median_seconds'),[(r.get('execution_seconds') or (r.get('query_log') or {}).get('seconds')) for r in x.get('runs',[])])
