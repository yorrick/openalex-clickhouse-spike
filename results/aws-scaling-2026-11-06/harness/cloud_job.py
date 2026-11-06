"""Bounded EC2 job; extends previously exercised small-study lifecycle."""
from pathlib import Path
from datetime import datetime, timedelta, timezone
from time import monotonic, sleep
import base64
import gzip
import json
import sys

import boto3
from botocore.exceptions import ClientError

HERE = Path(__file__).resolve().parent
LEGACY = HERE.parent / 'openalex-small-spike-20261105'
sys.path.insert(0, str(LEGACY))
from run_experiment import Experiment, ACCOUNT, REGION, COMMIT, write


class Job(Experiment):
    def __init__(self, config, *, instance_type, guest_path, az, raw_volume_id, disk_gib=16, throughput=125):
        super().__init__(config)
        if COMMIT!='0b3d5bcfbb5062aca4d26ae5f813c4659a234b5d' or not 119*60<(self.deadline-datetime.now(timezone.utc)).total_seconds()<=121*60:
            raise RuntimeError('Inherited source commit or two-hour termination deadline differs')
        self.out = HERE / self.name
        self.instance_type = instance_type
        self.guest_path = Path(guest_path)
        self.az = az
        self.raw_volume_id = raw_volume_id
        self.disk_gib = disk_gib
        self.throughput = throughput
        if self.session.region_name != REGION or instance_type not in ('t4g.small', 'm7g.8xlarge'):
            raise RuntimeError('Unapproved instance type or region')
        raw = self.clients['ec2'].describe_volumes(VolumeIds=[raw_volume_id])['Volumes'][0]
        if raw['AvailabilityZone'] != az or raw['State'] != 'available' or raw['Size'] != 120 or not raw['Encrypted']:
            raise RuntimeError('Retained raw volume state differs from the approved disk')
        if {'Key':'Project', 'Value':'openalex-retained-input'} not in raw['Tags']:
            raise RuntimeError('Unrecognized raw volume ownership')

    def create_bucket(self):
        s3 = self.clients['s3']
        s3.create_bucket(Bucket=self.bucket)
        self.record(bucket_created=True)
        s3.put_bucket_tagging(Bucket=self.bucket, Tagging={'TagSet': self.tags})
        s3.put_public_access_block(Bucket=self.bucket, PublicAccessBlockConfiguration={k:True for k in
            ('BlockPublicAcls','IgnorePublicAcls','BlockPublicPolicy','RestrictPublicBuckets')})
        s3.put_bucket_ownership_controls(Bucket=self.bucket, OwnershipControls={'Rules':[{'ObjectOwnership':'BucketOwnerEnforced'}]})
        s3.put_bucket_encryption(Bucket=self.bucket, ServerSideEncryptionConfiguration={'Rules':[
            {'ApplyServerSideEncryptionByDefault':{'SSEAlgorithm':'AES256'}}]})
        s3.put_bucket_lifecycle_configuration(Bucket=self.bucket, LifecycleConfiguration={'Rules':[
            {'ID':'expire-evidence','Status':'Enabled','Filter':{'Prefix':''},'Expiration':{'Days':7},
             'AbortIncompleteMultipartUpload':{'DaysAfterInitiation':1}}]})
        if not all(s3.get_public_access_block(Bucket=self.bucket)['PublicAccessBlockConfiguration'].values()):
            raise RuntimeError('Result bucket privacy check failed')

    def finish_primary(self, reason):
        # The primary artifact is canonical and was sealed before optional work.
        # A failed optional phase stays explicitly inconclusive in its own state.
        self.fetch()
        path=self.out/'cloud/summary.json'
        if not path.exists():
            raise RuntimeError(reason+'; primary measurements were not completed')
        primary=json.loads(path.read_text())
        if primary.get('primary_complete') is not True or primary.get('state')!='complete':
            raise RuntimeError(reason+'; primary measurements were not completed')
        primary.update(optional_phase='INCONCLUSIVE_OPTIONAL',controller_stop_reason=reason)
        write(self.out/'controller-summary.json',primary)
        return primary

    def wait(self):
        started=monotonic();last=None
        while monotonic()-started<110*60:
            try:
                status=json.loads(self.clients['s3'].get_object(Bucket=self.bucket,Key='run/cloud/status.json')['Body'].read())
                if status!=last:
                    print(json.dumps(status),flush=True);last=status
                if status['state']=='complete':
                    self.fetch()
                    return json.loads((self.out/'cloud/summary.json').read_text())
                if status['state']=='failed':
                    return self.finish_primary('Guest failed: '+status.get('error','unknown'))
            except ClientError as exc:
                if exc.response['Error']['Code'] not in ('NoSuchKey','404'):
                    raise
            work=datetime.fromisoformat(self.selection['work_deadline_at'])
            if datetime.now(timezone.utc)>work+timedelta(minutes=5):
                return self.finish_primary('Work deadline plus five-minute teardown grace exceeded')
            state=self.clients['ec2'].describe_instances(InstanceIds=[self.state['instance_id']])['Reservations'][0]['Instances'][0]['State']['Name']
            if state in ('shutting-down','terminated','stopping','stopped'):
                try:
                    write(self.out/'console-output.json',self.clients['ec2'].get_console_output(InstanceId=self.state['instance_id'],Latest=True))
                except Exception as exc:
                    write(self.out/'console-capture-error.json',{'error':str(exc)})
                return self.finish_primary('Instance exited before optional phase completion')
            sleep(10)
        return self.finish_primary('Cloud controller deadline exceeded')

    def fetch(self):
        s3=self.clients['s3']
        for page in s3.get_paginator('list_objects_v2').paginate(Bucket=self.bucket,Prefix='run/cloud/'):
            for item in page.get('Contents',[]):
                name=item['Key'].removeprefix('run/cloud/')
                if '/' in name or item['Size'] > 2000*(1<<20):
                    raise RuntimeError('Unexpected cloud artifact scope')
                path=self.out/'cloud'/name
                path.parent.mkdir(parents=True,exist_ok=True)
                s3.download_file(self.bucket,item['Key'],str(path))

    def launch(self):
        if (self.deadline - datetime.now(timezone.utc)).total_seconds() < 3600:
            raise RuntimeError('Insufficient time remains for the bounded instance run')
        iam, ec2 = self.clients['iam'], self.clients['ec2']
        role, role_arn = self.create_role('guest', 'ec2.amazonaws.com')
        iam.put_role_policy(RoleName=role, PolicyName='results-only', PolicyDocument=json.dumps({
            'Version': '2012-10-17', 'Statement': [{'Effect': 'Allow',
            'Action': ['s3:PutObject', 's3:AbortMultipartUpload'],
            'Resource': f'arn:aws:s3:::{self.bucket}/run/cloud/*'},
            {'Effect': 'Allow', 'Action': 's3:GetObject',
             'Resource': f'arn:aws:s3:::{self.bucket}/config/selection.json'}]}))
        iam.create_instance_profile(InstanceProfileName=role, Tags=self.tags)
        self.record(instance_profile=role)
        iam.add_role_to_instance_profile(InstanceProfileName=role, RoleName=role)
        vpcs = ec2.describe_vpcs(Filters=[{'Name': 'is-default', 'Values': ['true']}])['Vpcs']
        if len(vpcs) != 1:
            raise RuntimeError('No unique default VPC; no automatic network substitution')
        subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpcs[0]['VpcId']]},
            {'Name': 'default-for-az', 'Values': ['true']}])['Subnets']
        zones = {x['Location'] for x in ec2.describe_instance_type_offerings(LocationType='availability-zone',
            Filters=[{'Name': 'instance-type', 'Values': [self.instance_type]}])['InstanceTypeOfferings']}
        subnet = sorted((x for x in subnets if x['AvailabilityZone'] in zones and x['AvailabilityZone'] == self.az), key=lambda x: x['AvailabilityZone'])[0]
        sg = ec2.create_security_group(GroupName=self.name, Description='No inbound access for one small OpenAlex test',
                                      VpcId=vpcs[0]['VpcId'], TagSpecifications=[{'ResourceType': 'security-group', 'Tags': self.tags}])['GroupId']
        self.record(security_group=sg)
        ami = self.clients['ssm'].get_parameter(Name='/aws/service/canonical/ubuntu/server/24.04/stable/current/arm64/hvm/ebs-gp3/ami-id')['Parameter']['Value']
        if 'expected_ami' in self.selection and ami!=self.selection['expected_ami']:
            raise RuntimeError('Ubuntu AMI differs from the matched baseline')
        image = ec2.describe_images(ImageIds=[ami])['Images'][0]
        if (image.get('OwnerId') != '099720109477' or image.get('Architecture') != 'arm64'
            or image.get('RootDeviceName') != '/dev/sda1' or image.get('State') != 'available'
            or 'ubuntu-noble-24.04-arm64-server-' not in image.get('Name', '')):
            raise RuntimeError('Ubuntu image does not meet the reviewed platform constraints')
        self.selection['work_deadline_at']=(self.deadline-timedelta(minutes=20)).isoformat()
        encoded_scope=base64.b64encode(gzip.compress((HERE/'scope.py').read_bytes())).decode()
        encoded_runner = base64.b64encode(gzip.compress(self.guest_path.read_bytes())).decode()
        self.clients['s3'].put_object(Bucket=self.bucket, Key='config/selection.json',
                                      Body=json.dumps(self.selection).encode())
        userdata = f'''#!/bin/bash
set -Eeuo pipefail
TASK_BASE=/root/work/data/openalex-small-spike
mkdir -p "$TASK_BASE"
exec > >(tee -a "$TASK_BASE/bootstrap.log") 2>&1
shutdown -P +110
trap 'shutdown -P now' EXIT
export DEBIAN_FRONTEND=noninteractive
apt-get -o DPkg::Lock::Timeout=300 update
apt-get -o DPkg::Lock::Timeout=300 install -y --no-install-recommends ca-certificates docker.io docker-compose-v2 git python3-venv fio
systemctl enable --now docker
python3 -m venv "$TASK_BASE/tools"
"$TASK_BASE/tools/bin/pip" install uv==0.5.9
git clone --no-checkout https://github.com/yorrick/openalex-clickhouse-spike.git "$TASK_BASE/repo"
git -C "$TASK_BASE/repo" checkout --detach {COMMIT}
test "$(git -C "$TASK_BASE/repo" rev-parse HEAD)" = {COMMIT}
echo '{encoded_scope}' | base64 -d | gzip -d > "$TASK_BASE/scope.py"
echo '{encoded_runner}' | base64 -d | gzip -d > "$TASK_BASE/cloud_runner.py"
export SPIKE_BUCKET='{self.bucket}' SPIKE_PREFIX=''
cd "$TASK_BASE/repo"
"$TASK_BASE/tools/bin/uv" sync --frozen
"$TASK_BASE/tools/bin/uv" pip install --python .venv/bin/python boto3==1.40.0 pytest==8.3.5
.venv/bin/python -c 'import boto3,os; boto3.client("s3", region_name="us-east-1").download_file(os.environ["SPIKE_BUCKET"], "config/selection.json", "/root/work/data/openalex-small-spike/selection.json")'
.venv/bin/python "$TASK_BASE/cloud_runner.py"
'''
        # The bucket object keys have no leading slash.
        userdata = userdata.replace("SPIKE_PREFIX=''", "SPIKE_PREFIX='run'")
        (self.out / 'user-data.sh').write_text(userdata)
        if len(userdata.encode()) > 16384:
            raise RuntimeError('EC2 user data exceeds the service limit')
        deadline = monotonic() + 45
        while True:
            try:
                response = ec2.run_instances(ImageId=ami, InstanceType=self.instance_type, MinCount=1, MaxCount=1,
                    ClientToken=self.name, IamInstanceProfile={'Name': role}, UserData=userdata,
                    InstanceInitiatedShutdownBehavior='terminate',
                    MetadataOptions={'HttpTokens': 'required', 'HttpPutResponseHopLimit': 1},
                    NetworkInterfaces=[{'DeviceIndex': 0, 'SubnetId': subnet['SubnetId'], 'Groups': [sg], 'AssociatePublicIpAddress': True}],
                    BlockDeviceMappings=[{'DeviceName': '/dev/sda1', 'Ebs': {'VolumeType': 'gp3', 'VolumeSize': self.disk_gib, 'Iops': 3000, 'Throughput': self.throughput, 'Encrypted': True, 'DeleteOnTermination': True}}],
                    TagSpecifications=[{'ResourceType': t, 'Tags': self.tags} for t in ('instance', 'volume')])
                break
            except ClientError as exc:
                if exc.response['Error']['Code'] != 'InvalidParameterValue' or 'instance profile' not in str(exc).lower() or monotonic() > deadline:
                    raise
                sleep(3)
        instance = response['Instances'][0]['InstanceId']
        self.record(source_commit=COMMIT,run_deadline=self.deadline,instance_id=instance, instance_type=self.instance_type, ami=ami, launched_at=datetime.now(timezone.utc))
        expiry_role, expiry_arn = self.create_role('expiry', 'scheduler.amazonaws.com')
        iam.put_role_policy(RoleName=expiry_role, PolicyName='terminate-exact-instance', PolicyDocument=json.dumps({
            'Version': '2012-10-17', 'Statement': [{'Effect': 'Allow', 'Action': 'ec2:TerminateInstances',
            'Resource': f'arn:aws:ec2:{REGION}:{ACCOUNT}:instance/{instance}'}]}))
        sleep(10)
        decision = iam.simulate_principal_policy(PolicySourceArn=expiry_arn,
            ActionNames=['ec2:TerminateInstances'],
            ResourceArns=[f'arn:aws:ec2:{REGION}:{ACCOUNT}:instance/{instance}'])
        if not decision['EvaluationResults'] or any(x['EvalDecision'] != 'allowed' for x in decision['EvaluationResults']):
            raise RuntimeError('Scheduler role cannot terminate this exact instance')
        self.clients['scheduler'].create_schedule(Name=self.name, FlexibleTimeWindow={'Mode': 'OFF'},
            ScheduleExpression='at(' + self.deadline.strftime('%Y-%m-%dT%H:%M:%S') + ')',
            ScheduleExpressionTimezone='UTC', ActionAfterCompletion='DELETE',
            Target={'Arn': 'arn:aws:scheduler:::aws-sdk:ec2:terminateInstances', 'RoleArn': expiry_arn,
                    'Input': json.dumps({'InstanceIds': [instance]})})
        self.record(schedule_created=True)
        target = self.clients['scheduler'].get_schedule(Name=self.name)['Target']
        schedule=self.clients['scheduler'].get_schedule(Name=self.name)
        if schedule['State']!='ENABLED' or schedule['ScheduleExpression']!='at('+self.deadline.strftime('%Y-%m-%dT%H:%M:%S')+')' or target['Arn']!='arn:aws:scheduler:::aws-sdk:ec2:terminateInstances':
            raise RuntimeError('Termination schedule state/expression/API differs')
        if json.loads(target['Input']) != {'InstanceIds': [instance]} or target['RoleArn'] != expiry_arn:
            raise RuntimeError('Independent termination schedule failed verification')
        ec2.get_waiter('instance_running').wait(InstanceIds=[instance], WaiterConfig={'Delay': 5, 'MaxAttempts': 48})
        behavior = ec2.describe_instance_attribute(InstanceId=instance, Attribute='instanceInitiatedShutdownBehavior')
        if behavior['InstanceInitiatedShutdownBehavior']['Value'] != 'terminate':
            raise RuntimeError('Guest shutdown would not terminate its instance')
        ec2.attach_volume(InstanceId=instance, VolumeId=self.raw_volume_id, Device='/dev/sdf')
        ec2.get_waiter('volume_in_use').wait(VolumeIds=[self.raw_volume_id], WaiterConfig={'Delay': 3, 'MaxAttempts': 40})
        attached = ec2.describe_instances(InstanceIds=[instance])['Reservations'][0]['Instances'][0]
        mapping = [b for b in attached['BlockDeviceMappings'] if b.get('Ebs', {}).get('VolumeId') == self.raw_volume_id]
        if len(mapping) != 1 or mapping[0]['Ebs']['DeleteOnTermination'] is not False:
            raise RuntimeError('Raw input EBS retention was not verified')
        self.record(raw_attachment_verified=True, raw_delete_on_termination=False)
        return instance

