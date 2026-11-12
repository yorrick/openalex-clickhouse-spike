from cli_session import certification
"""Exact-run evidence collection and cleanup. Never touches the previously retained EBS."""
from pathlib import Path
import json,time,gzip,hashlib,datetime,sys,shutil
import boto3
HERE=Path(__file__).resolve().parent
C=json.loads((HERE/'cloud-state.json').read_text());A=json.loads((HERE/'aws-state.json').read_text());S=certification();assert S.client('sts').get_caller_identity()['Account']==C['account']=='502425560524'
EC=S.client('ec2');S3=S.client('s3');ATH=S.client('athena');IAM=S.client('iam');GLUE=S.client('glue');SC=S.client('scheduler')
def dump(p,d):p.write_text(json.dumps(d,indent=2,default=str)+'\n')
def terminal_queries():
 ids=[]
 if A.get('workgroup_created'):
  for page in ATH.get_paginator('list_query_executions').paginate(WorkGroup=A['workgroup']):ids+=page['QueryExecutionIds']
 qs=[]
 for qid in ids:
  q=ATH.get_query_execution(QueryExecutionId=qid)['QueryExecution'];assert q['WorkGroup']==A['workgroup'];assert q['Status']['State'] in ['SUCCEEDED','FAILED','CANCELLED'], 'Active Athena query; settle it before cleanup';qs.append(q)
 return qs

def collect():
 qs=terminal_queries();folder=HERE/'athena-csv';folder.mkdir(exist_ok=True);proof=[]
 for q in qs:
  if q['Status']['State']!='SUCCEEDED' or not q['Query'].lstrip().upper().startswith(('SELECT','WITH')):continue
  loc=q['ResultConfiguration']['OutputLocation'];assert loc.startswith('s3://'+C['bucket']+'/athena/');key=loc.split('/',3)[3];dest=folder/(q['QueryExecutionId']+'.csv.gz');meta=folder/(q['QueryExecutionId']+'.json')
  if meta.exists():
   p=json.loads(meta.read_text());assert dest.stat().st_size==p['gzip_bytes'] and hashlib.sha256(dest.read_bytes()).hexdigest()==p['gzip_sha256'];proof.append(p);continue
  assert shutil.disk_usage(HERE).free>5*2**30
  response=S3.get_object(Bucket=C['bucket'],Key=key,ExpectedBucketOwner=C['account']);digest=hashlib.sha256();n=0
  with gzip.open(dest,'wb',compresslevel=1) as out:
   while b:=response['Body'].read(8<<20):out.write(b);digest.update(b);n+=len(b)
  assert n==response['ContentLength'];p={'query_id':q['QueryExecutionId'],'key':key,'csv_bytes':n,'csv_sha256':digest.hexdigest(),'gzip_bytes':dest.stat().st_size,'gzip_sha256':hashlib.sha256(dest.read_bytes()).hexdigest()};dump(meta,p);proof.append(p)
 dump(HERE/'results/athena-full-csv-archive.json',{'all_succeeded_select_outputs_archived':True,'queries':proof,'terminal_states':{q['QueryExecutionId']:q['Status']['State'] for q in qs}});dump(HERE/'results/athena-full-query-receipts.json',qs);print('Archived',len(proof),'full Athena CSV results')

def cleanup():
 # This proof is created only after full local/native/Athena result verification and final freeze/download.
 proof=json.loads((HERE/'results/evidence-verified.json').read_text());assert proof['ready_for_cleanup'] is True
 assert (HERE/'results/athena-full-csv-archive.json').exists();terminal_queries()
 before=EC.describe_instances(InstanceIds=[C['instance_id']])['Reservations'][0]['Instances'][0];tags={x['Key']:x['Value'] for x in before.get('Tags',[])};assert tags.get('RunId')==C['run_id'] and tags.get('Project')=='openalex-200m-comparison'
 # A scheduled termination may have removed live mappings before this collector
 # reconnects. Use the volume IDs sealed at launch as the deletion receipt scope.
 volumes=C['volume_ids'];live_volumes=[x['Ebs']['VolumeId'] for x in before.get('BlockDeviceMappings',[])]
 assert len(volumes)==2 and 'vol-039919b5eb12aeb46' not in volumes
 assert set(live_volumes).issubset(volumes)
 assert all(x['Ebs']['DeleteOnTermination'] for x in before.get('BlockDeviceMappings',[]))
 EC.terminate_instances(InstanceIds=[C['instance_id']]);EC.get_waiter('instance_terminated').wait(InstanceIds=[C['instance_id']],WaiterConfig={'Delay':5,'MaxAttempts':60})
 if A.get('database_created'):
  tables=[]
  for page in GLUE.get_paginator('get_tables').paginate(DatabaseName=A['database']):tables += [x['Name'] for x in page['TableList']]
  for t in tables:GLUE.delete_table(DatabaseName=A['database'],Name=t)
  GLUE.delete_database(Name=A['database'])
 if A.get('workgroup_created'):ATH.delete_work_group(WorkGroup=A['workgroup'],RecursiveDeleteOption=True)
 try:SC.delete_schedule(Name=C['schedule'])
 except SC.exceptions.ResourceNotFoundException:pass
 # Instance is gone, so it cannot write more artifacts. Bucket identity is bound to the exact recorded run.
 assert C['bucket'].startswith(C['run_id']+'-') and C['bucket']==A['bucket']
 for page in S3.get_paginator('list_objects_v2').paginate(Bucket=C['bucket'],ExpectedBucketOwner=C['account']):
  items=[{'Key':x['Key']} for x in page.get('Contents',[])]
  if items:
   response=S3.delete_objects(Bucket=C['bucket'],ExpectedBucketOwner=C['account'],Delete={'Objects':items,'Quiet':True});assert not response.get('Errors')
 S3.delete_bucket(Bucket=C['bucket'],ExpectedBucketOwner=C['account'])
 role=C['role'];IAM.remove_role_from_instance_profile(InstanceProfileName=C['profile'],RoleName=role);IAM.delete_instance_profile(InstanceProfileName=C['profile']);IAM.detach_role_policy(RoleName=role,PolicyArn='arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore');IAM.delete_role_policy(RoleName=role,PolicyName='run-artifacts');IAM.delete_role(RoleName=role)
 IAM.delete_role_policy(RoleName=C['scheduler_role'],PolicyName='terminate-owned-run');IAM.delete_role(RoleName=C['scheduler_role'])
 for _ in range(30):
  try:EC.delete_security_group(GroupId=C['security_group']);break
  except EC.exceptions.ClientError as e:
   if e.response['Error']['Code']!='DependencyViolation':raise
   time.sleep(2)
 else:raise RuntimeError('Owned SG still attached; verify cleanup')
 absent=[]
 for v in volumes:
  for attempt in range(60):
   try:found=EC.describe_volumes(VolumeIds=[v])['Volumes']
   except EC.exceptions.ClientError as e:
    assert e.response['Error']['Code']=='InvalidVolume.NotFound';absent.append(v);break
   assert all(x['State'] in ['deleting','in-use','available'] for x in found)
   time.sleep(2)
  else:raise AssertionError(('Ephemeral volume remains',v))
 # The old explicitly retained volume must remain present and is never part of deletion.
 old=EC.describe_volumes(VolumeIds=['vol-039919b5eb12aeb46'])['Volumes'][0];assert old['VolumeId']=='vol-039919b5eb12aeb46'
 try:S3.head_bucket(Bucket=C['bucket'],ExpectedBucketOwner=C['account']);raise AssertionError('bucket still exists')
 except S3.exceptions.ClientError as e:assert e.response['Error']['Code'] in ['404','NoSuchBucket','NotFound']
 # A successful delete request is not the absence check.
 def absent_call(call,kwargs,codes):
  try:call(**kwargs)
  except Exception as e:
   assert hasattr(e,'response') and e.response['Error']['Code'] in codes;return True
  raise AssertionError(('Resource still exists',kwargs))
 absence={'bucket':True,'ephemeral_volumes':True,
  'glue_database':absent_call(GLUE.get_database,{'Name':A['database']},['EntityNotFoundException']),
  'athena_workgroup':absent_call(ATH.get_work_group,{'WorkGroup':A['workgroup']},['InvalidRequestException']),
  'schedule':absent_call(SC.get_schedule,{'Name':C['schedule']},['ResourceNotFoundException']),
  'security_group':absent_call(EC.describe_security_groups,{'GroupIds':[C['security_group']]},['InvalidGroup.NotFound']),
  'instance_profile':absent_call(IAM.get_instance_profile,{'InstanceProfileName':C['profile']},['NoSuchEntity']),
  'instance_role':absent_call(IAM.get_role,{'RoleName':C['role']},['NoSuchEntity']),
  'scheduler_role':absent_call(IAM.get_role,{'RoleName':C['scheduler_role']},['NoSuchEntity'])}
 final={'cleanup_complete':True,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'instance_id':C['instance_id'],'instance_state':'terminated','deleted_ephemeral_volumes_absent':absent,'bucket_absent':C['bucket'],'workgroup_deleted':A['workgroup'],'database_deleted':A['database'],'absence_checks':absence,'retained_prior_raw_volume_preserved':old['VolumeId'],'launch_at':C['launched_at']};dump(HERE/'results/aws-cleanup.json',final);C['cleanup_complete']=True;dump(HERE/'cloud-state.json',C);print(json.dumps(final,indent=2))
if __name__=='__main__':{'collect':collect,'cleanup':cleanup}[sys.argv[1]]()
