"""Delete onlythisexperiment's explicitly owned temporary S3/Glue/Athena resources."""
import json,time,math,gzip,hashlib
from urllib.parse import urlparse
from botocore.exceptions import ClientError
from athena_reference import Reference,ACCOUNT,PROJECT
from pg_helpers import HERE,dump

def main():
 r=Reference();assert r.state['project']==PROJECT
 assert r.db.startswith('oapg100_20261109_') and r.workgroup.startswith('oapg100-20261109-')
 assert r.state.get('athena_complete') or (HERE/'results/explicit-stop-cloud.json').exists()
 tags=r.s3.get_bucket_tagging(Bucket=r.bucket,ExpectedBucketOwner=ACCOUNT)['TagSet'];assert {'Key':'Project','Value':PROJECT} in tags
 assert r.s3.get_bucket_versioning(Bucket=r.bucket,ExpectedBucketOwner=ACCOUNT).get('Status') is None
 queries=[]
 for page in r.athena.get_paginator('list_query_executions').paginate(WorkGroup=r.workgroup):
  for qid in page['QueryExecutionIds']:
   q=r.athena.get_query_execution(QueryExecutionId=qid)['QueryExecution']
   if q['Status']['State'] not in ('SUCCEEDED','FAILED','CANCELLED'):
    r.athena.stop_query_execution(QueryExecutionId=qid)
    for _ in range(60):
     q=r.athena.get_query_execution(QueryExecutionId=qid)['QueryExecution']
     if q['Status']['State'] in ('SUCCEEDED','FAILED','CANCELLED'):break
     time.sleep(1)
    else:raise RuntimeError('UnsettledAthenaquery:'+qid)
   assert q['WorkGroup']==r.workgroup;queries.append(q)
 dump(HERE/'results/athena-all-executions-final.json',queries)
 csv_folder=HERE/'results/athena-result-csv';csv_folder.mkdir(exist_ok=True);csv_proofs=[]
 for q in queries:
  if q['Status']['State']=='SUCCEEDED' and q['Query'].lstrip().upper().startswith(('SELECT','WITH')):
   loc=urlparse(q['ResultConfiguration']['OutputLocation']);assert loc.netloc==r.bucket and loc.path.startswith('/athena/')
   body=r.s3.get_object(Bucket=r.bucket,Key=loc.path.lstrip('/'),ExpectedBucketOwner=ACCOUNT)['Body'].read();path=csv_folder/(q['QueryExecutionId']+'.csv.gz')
   with gzip.open(path,'wb') as f:f.write(body)
   csv_proofs.append({'query_id':q['QueryExecutionId'],'raw_csv_bytes':len(body),'raw_csv_sha256':hashlib.sha256(body).hexdigest(),'gzip_bytes':path.stat().st_size,'local_path':str(path)})
 dump(HERE/'results/athena-csv-archives.json',csv_proofs)
 # Reconcile every started statement even if a client was interrupted.
 byid={q['QueryExecutionId']:q for q in queries}
 for x in r.records:
  if x.get('id') in byid:
   q=byid[x['id']];n=q.get('Statistics',{}).get('DataScannedInBytes',0)
   x.update(state=q['Status']['State'],statistics=q.get('Statistics',{}),status=q['Status'],billable_bytes=max(10000000,math.ceil(n/1000000)*1000000) if x['dml'] else 0)
 dump(HERE/'athena-statements.json',r.records)
 tables=[t['Name'] for page in r.glue.get_paginator('get_tables').paginate(DatabaseName=r.db) for t in page['TableList']]
 for i in range(0,len(tables),100):
  res=r.glue.batch_delete_table(DatabaseName=r.db,TablesToDelete=tables[i:i+100]);assert not res.get('Errors'),res
 r.glue.delete_database(Name=r.db)
 r.athena.delete_work_group(WorkGroup=r.workgroup,RecursiveDeleteOption=True)
 objects=[{'Key':o['Key'],'bytes':o['Size']} for page in r.s3.get_paginator('list_objects_v2').paginate(Bucket=r.bucket,ExpectedBucketOwner=ACCOUNT) for o in page.get('Contents',[])]
 for i in range(0,len(objects),1000):
  res=r.s3.delete_objects(Bucket=r.bucket,ExpectedBucketOwner=ACCOUNT,Delete={'Objects':[{'Key':o['Key']} for o in objects[i:i+1000]],'Quiet':True});assert not res.get('Errors'),res
 assert not r.s3.list_objects_v2(Bucket=r.bucket,ExpectedBucketOwner=ACCOUNT,MaxKeys=1).get('Contents')
 r.s3.delete_bucket(Bucket=r.bucket,ExpectedBucketOwner=ACCOUNT)
 checks={}
 for name,call in [('bucket',lambda:r.s3.head_bucket(Bucket=r.bucket,ExpectedBucketOwner=ACCOUNT)),('database',lambda:r.glue.get_database(Name=r.db)),('workgroup',lambda:r.athena.get_work_group(WorkGroup=r.workgroup))]:
  try:call();raise RuntimeError('Resource still exists:'+name)
  except ClientError as e:
   code=e.response['Error']['Code'];assert code in ('404','NoSuchBucket','EntityNotFoundException','InvalidRequestException'),code
   checks[name]=code
 result={'at':time.time(),'account':ACCOUNT,'bucket':r.bucket,'database':r.db,'workgroup':r.workgroup,'deleted_tables':tables,'deleted_objects':len(objects),'deleted_bytes':sum(o['bytes'] for o in objects),'absence_probes':checks,'all_queries_terminal':True,'billable_athena_bytes':sum(x['billable_bytes'] for x in r.records),'no_ec2_resources_created':True,'retained_old_raw_ebs_untouched':True}
 dump(HERE/'results/aws-cleanup.json',result);r.state['cleanup_complete']=True;r.state['cleanup_at']=time.time();r.save();print(json.dumps(result,indent=2))
if __name__=='__main__':main()
