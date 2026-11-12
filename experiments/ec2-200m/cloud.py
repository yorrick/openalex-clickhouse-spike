from pathlib import Path
import boto3,json,datetime,time,hashlib,sys
HERE=Path(__file__).resolve().parent
SESSION=boto3.Session(profile_name='certification',region_name='us-east-1')
EC=SESSION.client('ec2');IAM=SESSION.client('iam');S3=SESSION.client('s3');SCHED=SESSION.client('scheduler')
P=HERE/'cloud-state.json'
STATE=json.loads(P.read_text()) if P.exists() else {'run_id':'oa200-20261112-'+hashlib.sha256(str(time.time_ns()).encode()).hexdigest()[:6],'account':'502425560524','region':'us-east-1','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
RUN=STATE['run_id'];BUCKET=RUN+'-502425560524';TAGS=[{'Key':'Project','Value':'openalex-200m-comparison'},{'Key':'RunId','Value':RUN}]
def save():
 p=P.with_suffix('.new');p.write_text(json.dumps(STATE,indent=2,default=str)+'\n');p.replace(P)
def check():assert SESSION.client('sts').get_caller_identity()['Account']==STATE['account']
def launch():
 check();assert not STATE.get('instance_id'),'Already launched; inspect existing state instead of duplicating'
 pre=json.loads((HERE/'results/preflight.json').read_text());assert pre['account']==STATE['account'];assert pre['cost']['total_reserved_estimate_usd']<25
 save();S3.create_bucket(Bucket=BUCKET);STATE['bucket']=BUCKET;save()
 S3.put_public_access_block(Bucket=BUCKET,PublicAccessBlockConfiguration=dict(BlockPublicAcls=True,IgnorePublicAcls=True,BlockPublicPolicy=True,RestrictPublicBuckets=True))
 S3.put_bucket_encryption(Bucket=BUCKET,ServerSideEncryptionConfiguration={'Rules':[{'ApplyServerSideEncryptionByDefault':{'SSEAlgorithm':'AES256'}}]})
 S3.put_bucket_lifecycle_configuration(Bucket=BUCKET,LifecycleConfiguration={'Rules':[{'ID':'expire','Status':'Enabled','Filter':{'Prefix':''},'Expiration':{'Days':7},'AbortIncompleteMultipartUpload':{'DaysAfterInitiation':1}}]})
 role=RUN+'-instance';trust={'Version':'2012-10-17','Statement':[{'Effect':'Allow','Principal':{'Service':'ec2.amazonaws.com'},'Action':'sts:AssumeRole'}]}
 IAM.create_role(RoleName=role,AssumeRolePolicyDocument=json.dumps(trust),Tags=TAGS);STATE['role']=role;save()
 IAM.attach_role_policy(RoleName=role,PolicyArn='arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore')
 policy={'Version':'2012-10-17','Statement':[{'Effect':'Allow','Action':['s3:ListBucket'],'Resource':'arn:aws:s3:::'+BUCKET,'Condition':{'StringLike':{'s3:prefix':['run','run/*']}}},{'Effect':'Allow','Action':['s3:PutObject','s3:GetObject','s3:AbortMultipartUpload'],'Resource':'arn:aws:s3:::'+BUCKET+'/run/*'}]}
 IAM.put_role_policy(RoleName=role,PolicyName='run-artifacts',PolicyDocument=json.dumps(policy))
 IAM.create_instance_profile(InstanceProfileName=role,Tags=TAGS);STATE['profile']=role;save();IAM.add_role_to_instance_profile(InstanceProfileName=role,RoleName=role)
 sr=RUN+'-expiry';a=IAM.create_role(RoleName=sr,AssumeRolePolicyDocument=json.dumps({'Version':'2012-10-17','Statement':[{'Effect':'Allow','Principal':{'Service':'scheduler.amazonaws.com'},'Action':'sts:AssumeRole','Condition':{'StringEquals':{'aws:SourceAccount':STATE['account']}}}]}),Tags=TAGS)
 STATE['scheduler_role']=sr;STATE['scheduler_role_arn']=a['Role']['Arn'];save()
 IAM.put_role_policy(RoleName=sr,PolicyName='terminate-owned-run',PolicyDocument=json.dumps({'Version':'2012-10-17','Statement':[{'Effect':'Allow','Action':'ec2:TerminateInstances','Resource':'arn:aws:ec2:us-east-1:502425560524:instance/*','Condition':{'StringEquals':{'ec2:ResourceTag/RunId':RUN}}}]}))
 sg=EC.create_security_group(GroupName=RUN,Description='OpenAlex ephemeral comparison, no inbound ports',VpcId=pre['vpc'],TagSpecifications=[{'ResourceType':'security-group','Tags':TAGS}])['GroupId'];STATE['security_group']=sg;save()
 # Deliberately use default outbound rules for OS packages, Docker registry, S3 and SSM. No inbound rules.
 deadline=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=12);STATE['deadline']=deadline.isoformat();save()
 for attempt in range(30):
  try:
   r=EC.run_instances(ImageId=pre['ami'],InstanceType='m7g.4xlarge',MinCount=1,MaxCount=1,ClientToken=RUN,IamInstanceProfile={'Name':role},InstanceInitiatedShutdownBehavior='terminate',MetadataOptions={'HttpTokens':'required','HttpEndpoint':'enabled','HttpPutResponseHopLimit':1},NetworkInterfaces=[{'DeviceIndex':0,'SubnetId':pre['subnet'],'Groups':[sg],'AssociatePublicIpAddress':True}],BlockDeviceMappings=[{'DeviceName':'/dev/sda1','Ebs':{'VolumeSize':32,'VolumeType':'gp3','Encrypted':True,'DeleteOnTermination':True}},{'DeviceName':'/dev/sdf','Ebs':{'VolumeSize':1024,'VolumeType':'gp3','Iops':6000,'Throughput':500,'Encrypted':True,'DeleteOnTermination':True}}],UserData=(HERE/'bootstrap.sh').read_text(),TagSpecifications=[{'ResourceType':'instance','Tags':TAGS},{'ResourceType':'volume','Tags':TAGS}]);break
  except EC.exceptions.ClientError as e:
   if e.response['Error']['Code'] not in ['InvalidParameterValue','InvalidIamInstanceProfile.NotFound'] or attempt==29:raise
   time.sleep(2)
 instance=r['Instances'][0]['InstanceId'];STATE['instance_id']=instance;STATE['launched_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()
 try:
  SCHED.create_schedule(Name=RUN,ScheduleExpression='at('+deadline.replace(tzinfo=None).isoformat(timespec='seconds')+')',ScheduleExpressionTimezone='UTC',FlexibleTimeWindow={'Mode':'OFF'},ActionAfterCompletion='DELETE',Target={'Arn':'arn:aws:scheduler:::aws-sdk:ec2:terminateInstances','RoleArn':STATE['scheduler_role_arn'],'Input':json.dumps({'InstanceIds':[instance]}),'RetryPolicy':{'MaximumEventAgeInSeconds':3600,'MaximumRetryAttempts':3}})
  STATE['schedule']=RUN;save()
 except BaseException:
  EC.terminate_instances(InstanceIds=[instance]);raise
 print(json.dumps({'instance':instance,'bucket':BUCKET,'deadline':STATE['deadline'],'state_file':str(P)},indent=2))
def status():
 check();print(json.dumps(STATE,indent=2));
 if STATE.get('instance_id'):
  x=EC.describe_instances(InstanceIds=[STATE['instance_id']])['Reservations'][0]['Instances'][0];print(json.dumps({k:x.get(k) for k in ['InstanceId','State','LaunchTime','PublicIpAddress','BlockDeviceMappings']},indent=2,default=str))
if __name__=='__main__':
 {'launch':launch,'status':status}[sys.argv[1]]()
