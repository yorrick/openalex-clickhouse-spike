from pathlib import Path
import boto3,json,sys,time,tarfile,hashlib,shlex
HERE=Path(__file__).resolve().parent
STATE=json.loads((HERE/'cloud-state.json').read_text());s=boto3.Session(profile_name='certification',region_name='us-east-1');assert s.client('sts').get_caller_identity()['Account']==STATE['account'];ssm=s.client('ssm');s3=s.client('s3');instance=STATE['instance_id']
def command(cmd):
 r=ssm.send_command(InstanceIds=[instance],DocumentName='AWS-RunShellScript',Parameters={'commands':['/bin/bash -c '+shlex.quote(cmd)],'executionTimeout':['600']});cid=r['Command']['CommandId'];print('CommandId',cid,flush=True)
 for _ in range(90):
  time.sleep(1)
  try:q=ssm.get_command_invocation(CommandId=cid,InstanceId=instance)
  except ssm.exceptions.InvocationDoesNotExist:continue
  if q['Status'] not in ['Pending','InProgress','Delayed']:
   print(q['Status']);print(q.get('StandardOutputContent','')[-12000:]);print(q.get('StandardErrorContent','')[-4000:]);return q
 raise RuntimeError('Control command still running, inspect CommandId; do not repeat mutations')
if __name__=='__main__':
 if sys.argv[1]=='exec':command(sys.argv[2])
 elif sys.argv[1]=='execfile':command(Path(sys.argv[2]).read_text())
 elif sys.argv[1]=='upload':
  dest=HERE/'payload.tar.gz'
  with tarfile.open(dest,'w:gz') as tar:
   for path in HERE.iterdir():
    if path.suffix in ['.py','.sh'] or path.name in ['input-manifest.json','projection-templates.json','plan.md'] or path.name=='sql':tar.add(path,arcname=path.name)
  s3.upload_file(str(dest),STATE['bucket'],'run/code/payload.tar.gz');h=hashlib.sha256(dest.read_bytes()).hexdigest();(HERE/'payload.sha256').write_text(h+'\n');print('payload',dest.stat().st_size,'SHA256',h)
 elif sys.argv[1]=='download':
  folder=HERE/'cloud-results';folder.mkdir(exist_ok=True);n=0
  index_path=HERE/'cloud-download-index.json';index=json.loads(index_path.read_text()) if index_path.exists() else {}
  for page in s3.get_paginator('list_objects_v2').paginate(Bucket=STATE['bucket'],Prefix='run/results/'):
   for f in page.get('Contents',[]):
    path=folder/f['Key'].removeprefix('run/results/');path.parent.mkdir(parents=True,exist_ok=True)
    previous=index.get(f['Key'],{})
    if path.exists() and path.stat().st_size==f['Size'] and previous.get('etag')==f['ETag'] and hashlib.sha256(path.read_bytes()).hexdigest()==previous.get('sha256'):continue
    temp=path.with_suffix(path.suffix+'.download');s3.download_file(STATE['bucket'],f['Key'],str(temp));assert temp.stat().st_size==f['Size'];temp.replace(path);n+=1
    index[f['Key']]={'etag':f['ETag'],'bytes':f['Size'],'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
  index_path.write_text(json.dumps(index,indent=2)+'\n')
  print('downloaded',n)
