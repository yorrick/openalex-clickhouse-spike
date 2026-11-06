"""Throwaway USD-3 resource envelope for one small EC2/Athena comparison.

Default mode is read-only preparation. Execution requires the separate approval
marker after external review succeeds or the user explicitly waives that review.
"""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from time import monotonic, sleep
import argparse
import base64
import gzip
import hashlib
import json
import os
import statistics
import subprocess
import traceback
import uuid

import boto3
from botocore.exceptions import ClientError
import httpx
import pyarrow as pa

from athena_sql import PROJECTION, canonical_rows, clickhouse_result_columns, external_table, queries, views


HERE = Path(__file__).resolve().parent
ACCOUNT = '502425560524'
REGION = 'us-east-1'
COMMIT = '0b3d5bcfbb5062aca4d26ae5f813c4659a234b5d'
GIB = 1 << 30
MAX_QUERY_BYTES = 3 * GIB
MAX_DML = 25  # Four source-file probes and three executions of seven queries.


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.writing')
    temporary.write_text(json.dumps(value, indent=2, default=str) + '\n')
    temporary.replace(path)


def objects(selection):
    out = [('works', x) for x in selection['works']]
    for entity, manifest in selection['dimensions'].items():
        out.extend((entity, x) for x in manifest['files'])
    return out


def validate_selection(selection):
    items = objects(selection)
    if not 0 < len(items) <= 300:
        raise RuntimeError('Source file-count limit exceeded')
    total = sum(int(f.get('content_length', f.get('meta', {}).get('content_length', 0)))
                for _, f in items)
    if not 0 < total <= 3 * GIB or total != selection['total_bytes']:
        raise RuntimeError('Sample byte limit or manifest reconciliation failed')
    if len({f['url'] for _, f in items}) != len(items):
        raise RuntimeError('Duplicate source files')
    for entity, f in items:
        if entity not in PROJECTION or not f['url'].startswith(f's3://openalex/data/parquet/{entity}/'):
            raise RuntimeError('Unapproved source dataset')


def pin_sources(selection):
    validate_selection(selection)
    def head(item):
        entity, f = item
        if not f['url'].startswith('s3://openalex/data/parquet/'):
            raise RuntimeError('Unexpected source bucket')
        expected = int(f.get('content_length', f.get('meta', {}).get('content_length', 0)))
        url = f['url'].replace('s3://openalex/', 'https://openalex.s3.amazonaws.com/')
        r = client.head(url)
        r.raise_for_status()
        if int(r.headers['content-length']) != expected or not r.headers.get('etag'):
            raise RuntimeError('Source object does not match manifest')
        return entity, f['url'], r.headers['etag']
    lookup = {}
    with httpx.Client(timeout=20, limits=httpx.Limits(max_connections=8, max_keepalive_connections=8)) as client:
        with ThreadPoolExecutor(max_workers=8) as pool:
            for entity, url, etag in pool.map(head, objects(selection)):
                lookup[url] = etag
    for _, f in objects(selection):
        if 'observed_etag' in f and f['observed_etag'] != lookup[f['url']]:
            raise RuntimeError('Pinned source changed during experiment')
        f['observed_etag'] = lookup[f['url']]
    return selection


class Experiment:
    def __init__(self, selection):
        self.selection = selection
        self.session = boto3.Session(profile_name='certification', region_name=REGION)
        self.clients = {n: self.session.client(n) for n in ('sts', 'ec2', 'iam', 's3', 'ssm', 'athena', 'glue', 'scheduler')}
        if self.clients['sts'].get_caller_identity()['Account'] != ACCOUNT:
            raise RuntimeError('AWS account mismatch')
        self.name = 'oaspike-' + datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S') + '-' + uuid.uuid4().hex[:6]
        self.bucket = self.name + '-' + ACCOUNT
        self.db = self.name.replace('-', '_')
        self.out = HERE / self.name
        self.state = {'run_id': self.name, 'account': ACCOUNT, 'region': REGION, 'bucket': self.bucket}
        self.dml = 0
        self.query_records = []
        self.statement_ledger = []
        self.running_queries = set()
        self.deadline = datetime.now(timezone.utc) + timedelta(hours=2)
        self.tags = [{'Key': 'Project', 'Value': 'openalex-small-spike'}, {'Key': 'RunId', 'Value': self.name}]

    def record(self, **values):
        self.state.update(values)
        write(self.out / 'state.json', self.state)

    def query(self, sql, *, use_db=True):
        is_dml = sql.lstrip().upper().startswith(('SELECT', 'WITH'))
        if is_dml:
            self.dml += 1
            if self.dml > MAX_DML:
                raise RuntimeError('Athena query-count budget exhausted')
        if datetime.now(timezone.utc) >= self.deadline:
            raise RuntimeError('Experiment deadline reached')
        args = {'QueryString': sql, 'WorkGroup': self.name,
                'ClientRequestToken': uuid.uuid4().hex + uuid.uuid4().hex,
                'ResultReuseConfiguration': {'ResultReuseByAgeConfiguration': {'Enabled': False}}}
        if use_db:
            args['QueryExecutionContext'] = {'Database': self.db, 'Catalog': 'AwsDataCatalog'}
        a = self.clients['athena']
        ledger = {'client_token': args['ClientRequestToken'], 'is_dml': is_dml,
                  'dml_ordinal': self.dml, 'sql': sql, 'state': 'starting'}
        self.statement_ledger.append(ledger)
        write(self.out / 'statement-ledger.json', self.statement_ledger)
        started = monotonic()
        qid = a.start_query_execution(**args)['QueryExecutionId']
        ledger.update(query_id=qid, state='started')
        write(self.out / 'statement-ledger.json', self.statement_ledger)
        self.running_queries.add(qid)
        write(self.out / 'active-query.json', {'query_id': qid, 'sql': sql})
        timed_out = False
        while True:
            q = a.get_query_execution(QueryExecutionId=qid)['QueryExecution']
            status = q['Status']['State']
            if status in ('SUCCEEDED', 'FAILED', 'CANCELLED'):
                break
            if monotonic() - started > 240 and not timed_out:
                a.stop_query_execution(QueryExecutionId=qid)
                timed_out = True
            if monotonic() - started > 300:
                break
            sleep(1)
        if status in ('SUCCEEDED', 'FAILED', 'CANCELLED'):
            self.running_queries.remove(qid)
        if q.get('WorkGroup') != self.name:
            raise RuntimeError('Athena execution did not use the isolated capped workgroup')
        ledger.update(state=status, statistics=q.get('Statistics', {}))
        write(self.out / 'statement-ledger.json', self.statement_ledger)
        record = {'id': qid, 'sql': sql, 'status': q['Status'],
                  'statistics': q.get('Statistics', {}), 'client_seconds': monotonic() - started,
                  'is_dml': is_dml, 'statement_type': q.get('StatementType'), 'timed_out': timed_out}
        self.query_records.append(record)
        write(self.out / 'athena-query-records.json', self.query_records)
        if status != 'SUCCEEDED' or timed_out:
            raise RuntimeError('Athena failed: ' + q['Status'].get('StateChangeReason', status))
        if not is_dml:
            return [], record
        # The API preserves NULL versus empty string, unlike a plain CSV reader.
        rows = []
        columns = None
        first = True
        for page in a.get_paginator('get_query_results').paginate(QueryExecutionId=qid):
            result = page['ResultSet']
            columns = columns or [x['Name'] for x in result['ResultSetMetadata']['ColumnInfo']]
            for row in result.get('Rows', []):
                if first:
                    first = False
                    continue
                values = [x.get('VarCharValue') for x in row['Data']]
                if len(values) != len(columns):
                    raise RuntimeError('Athena result column count mismatch')
                rows.append(dict(zip(columns, values)))
        return rows, record

    def setup_athena(self):
        s3 = self.clients['s3']
        s3.create_bucket(Bucket=self.bucket)
        self.record(bucket_created=True)
        s3.put_bucket_tagging(Bucket=self.bucket, Tagging={'TagSet': self.tags})
        s3.put_public_access_block(Bucket=self.bucket, PublicAccessBlockConfiguration={k: True for k in
            ('BlockPublicAcls', 'IgnorePublicAcls', 'BlockPublicPolicy', 'RestrictPublicBuckets')})
        s3.put_bucket_ownership_controls(Bucket=self.bucket, OwnershipControls={'Rules': [{'ObjectOwnership': 'BucketOwnerEnforced'}]})
        s3.put_bucket_encryption(Bucket=self.bucket, ServerSideEncryptionConfiguration={'Rules': [
            {'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]})
        s3.put_bucket_lifecycle_configuration(Bucket=self.bucket, LifecycleConfiguration={'Rules': [
            {'ID': 'expire-test-artifacts', 'Status': 'Enabled', 'Filter': {'Prefix': ''},
             'Expiration': {'Days': 7}, 'AbortIncompleteMultipartUpload': {'DaysAfterInitiation': 1}}]})
        a = self.clients['athena']
        a.create_work_group(Name=self.name, Tags=self.tags, Configuration={
            'EnforceWorkGroupConfiguration': True, 'BytesScannedCutoffPerQuery': MAX_QUERY_BYTES,
            'EngineVersion': {'SelectedEngineVersion': 'Athena engine version 3'},
            'ResultConfiguration': {'OutputLocation': f's3://{self.bucket}/athena/', 'ExpectedBucketOwner': ACCOUNT,
                                    'EncryptionConfiguration': {'EncryptionOption': 'SSE_S3'}}})
        self.record(workgroup_created=True)
        observed = a.get_work_group(WorkGroup=self.name)['WorkGroup']['Configuration']
        if (observed.get('BytesScannedCutoffPerQuery') != MAX_QUERY_BYTES
            or observed.get('EnforceWorkGroupConfiguration') is not True
            or observed.get('ResultConfiguration', {}).get('OutputLocation') != f's3://{self.bucket}/athena/'):
            raise RuntimeError('Athena workgroup controls did not match the planned limits')
        self.query('CREATE DATABASE ' + self.db, use_db=False)
        self.record(database_created=True)
        by_entity = {}
        for entity, item in objects(self.selection):
            by_entity.setdefault(entity, []).append(item)
        for entity, items in by_entity.items():
            s3.put_object(Bucket=self.bucket, Key=f'manifests/{entity}/files.txt',
                          Body=('\n'.join(x['url'] for x in items) + '\n').encode())
            schema = pa.ipc.read_schema(pa.BufferReader((HERE / (entity + '-schema.arrow')).read_bytes()))
            ddl = external_table(entity, schema, f's3://{self.bucket}/manifests/{entity}/')
            (self.out / (entity + '-table.sql')).write_text(ddl)
            self.query(ddl)
            projected = ', '.join('"' + name + '"' for name in PROJECTION[entity])
            # Decode the projected values, not only Parquet row-count metadata.
            # GROUPING SETS adds a global ID-uniqueness check without a second scan.
            probe = f'''SELECT "$path" AS path, count(*) AS n_rows,
                count(DISTINCT id) AS distinct_ids,
                sum(length(json_format(CAST(ROW({projected}) AS JSON)))) AS decoded_bytes,
                CAST(NULL AS varchar) AS null_probe, '' AS empty_probe,
                true AS boolean_probe, CAST('9007199254740993' AS bigint) AS bigint_probe
                FROM raw_{entity} GROUP BY GROUPING SETS (("$path"), ())'''
            actual, record = self.query(probe)
            for row in actual:
                if (row['null_probe'] is not None or row['empty_probe'] != ''
                    or row['boolean_probe'] != 'true' or row['bigint_probe'] != '9007199254740993'):
                    raise RuntimeError('Athena result decoding did not preserve required value types')
                if int(row['n_rows']) != int(row['distinct_ids']) or int(row['decoded_bytes']) <= 0:
                    raise RuntimeError('Raw source IDs are not unique or projected values were not decoded')
            totals = [row for row in actual if row['path'] is None]
            if len(totals) != 1 or int(totals[0]['n_rows']) != sum(int(x.get('record_count', x.get('meta', {}).get('record_count', -1))) for x in items):
                raise RuntimeError('Raw source global row count does not reconcile')
            got = {x['path']: int(x['n_rows']) for x in actual if x['path'] is not None}
            expected = {x['url']: int(x.get('record_count', x.get('meta', {}).get('record_count', -1))) for x in items}
            if got != expected:
                raise RuntimeError('Athena did not read exactly the selected files and row counts')
        for name, sql in views().items():
            self.query(f'CREATE VIEW {name} AS {sql}')
        for name, sql in queries(1).items():
            _, explanation = self.query('EXPLAIN (TYPE VALIDATE) ' + sql)
            if explanation['statistics'].get('DataScannedInBytes', 0) != 0:
                raise RuntimeError('EXPLAIN unexpectedly scanned data')
        self.record(athena_source_probe='passed')

    def create_role(self, suffix, service):
        iam = self.clients['iam']
        name = self.name + '-' + suffix
        response = iam.create_role(RoleName=name, Tags=self.tags, AssumeRolePolicyDocument=json.dumps({
            'Version': '2012-10-17', 'Statement': [{'Effect': 'Allow',
            'Principal': {'Service': service}, 'Action': 'sts:AssumeRole'}]}))
        self.record(**{suffix + '_role': name})
        return name, response['Role']['Arn']

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
            Filters=[{'Name': 'instance-type', 'Values': ['m7g.xlarge']}])['InstanceTypeOfferings']}
        subnet = sorted((x for x in subnets if x['AvailabilityZone'] in zones), key=lambda x: x['AvailabilityZone'])[0]
        sg = ec2.create_security_group(GroupName=self.name, Description='No inbound access for one small OpenAlex test',
                                      VpcId=vpcs[0]['VpcId'], TagSpecifications=[{'ResourceType': 'security-group', 'Tags': self.tags}])['GroupId']
        self.record(security_group=sg)
        ami = self.clients['ssm'].get_parameter(Name='/aws/service/canonical/ubuntu/server/24.04/stable/current/arm64/hvm/ebs-gp3/ami-id')['Parameter']['Value']
        image = ec2.describe_images(ImageIds=[ami])['Images'][0]
        if (image.get('OwnerId') != '099720109477' or image.get('Architecture') != 'arm64'
            or image.get('RootDeviceName') != '/dev/sda1' or image.get('State') != 'available'
            or 'ubuntu-noble-24.04-arm64-server-' not in image.get('Name', '')):
            raise RuntimeError('Ubuntu image does not meet the reviewed platform constraints')
        encoded_runner = base64.b64encode(gzip.compress((HERE / 'cloud_runner.py').read_bytes())).decode()
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
apt-get -o DPkg::Lock::Timeout=300 install -y --no-install-recommends ca-certificates docker.io docker-compose-v2 git python3-venv
systemctl enable --now docker
python3 -m venv "$TASK_BASE/tools"
"$TASK_BASE/tools/bin/pip" install uv==0.5.9
git clone --no-checkout https://github.com/yorrick/openalex-clickhouse-spike.git "$TASK_BASE/repo"
git -C "$TASK_BASE/repo" checkout --detach {COMMIT}
test "$(git -C "$TASK_BASE/repo" rev-parse HEAD)" = {COMMIT}
echo '{encoded_runner}' | base64 -d | gzip -d > "$TASK_BASE/cloud_runner.py"
export SPIKE_BUCKET='{self.bucket}' SPIKE_PREFIX=''
cd "$TASK_BASE/repo"
"$TASK_BASE/tools/bin/uv" sync --frozen
"$TASK_BASE/tools/bin/uv" pip install --python .venv/bin/python boto3==1.40.0
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
                response = ec2.run_instances(ImageId=ami, InstanceType='m7g.xlarge', MinCount=1, MaxCount=1,
                    ClientToken=self.name, IamInstanceProfile={'Name': role}, UserData=userdata,
                    InstanceInitiatedShutdownBehavior='terminate',
                    MetadataOptions={'HttpTokens': 'required', 'HttpPutResponseHopLimit': 1},
                    NetworkInterfaces=[{'DeviceIndex': 0, 'SubnetId': subnet['SubnetId'], 'Groups': [sg], 'AssociatePublicIpAddress': True}],
                    BlockDeviceMappings=[{'DeviceName': '/dev/sda1', 'Ebs': {'VolumeType': 'gp3', 'VolumeSize': 50, 'Encrypted': True, 'DeleteOnTermination': True}}],
                    TagSpecifications=[{'ResourceType': t, 'Tags': self.tags} for t in ('instance', 'volume')])
                break
            except ClientError as exc:
                if exc.response['Error']['Code'] != 'InvalidParameterValue' or 'instance profile' not in str(exc).lower() or monotonic() > deadline:
                    raise
                sleep(3)
        instance = response['Instances'][0]['InstanceId']
        self.record(instance_id=instance, instance_type='m7g.xlarge', ami=ami, launched_at=datetime.now(timezone.utc))
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
        if json.loads(target['Input']) != {'InstanceIds': [instance]} or target['RoleArn'] != expiry_arn:
            raise RuntimeError('Independent termination schedule failed verification')
        return instance

    def wait_cloud(self):
        s3 = self.clients['s3']
        started = monotonic()
        while monotonic() - started < 45 * 60:
            try:
                response = s3.get_object(Bucket=self.bucket, Key='run/cloud/status.json')
                status = json.loads(response['Body'].read())
                if status['state'] in ('complete', 'failed'):
                    for page in s3.get_paginator('list_objects_v2').paginate(Bucket=self.bucket, Prefix='run/cloud/'):
                        for item in page.get('Contents', []):
                            name = item['Key'].removeprefix('run/cloud/')
                            if '/' in name or not name.endswith('.json') or item['Size'] > 100 * (1 << 20):
                                raise RuntimeError('Unexpected cloud artifact')
                            target = self.out / 'cloud' / name
                            target.parent.mkdir(parents=True, exist_ok=True)
                            s3.download_file(self.bucket, item['Key'], str(target))
                    if status['state'] == 'failed':
                        raise RuntimeError('Cloud run failed: ' + status['error'])
                    return json.loads((self.out / 'cloud/summary.json').read_text())
            except ClientError as exc:
                if exc.response['Error']['Code'] not in ('NoSuchKey', '404'):
                    raise
            instance = self.clients['ec2'].describe_instances(InstanceIds=[self.state['instance_id']])['Reservations'][0]['Instances'][0]
            if instance['State']['Name'] in ('shutting-down', 'terminated', 'stopping', 'stopped'):
                console = self.clients['ec2'].get_console_output(InstanceId=self.state['instance_id'], Latest=True)
                write(self.out / 'console-output.json', console)
                raise RuntimeError('Instance exited before producing a complete result')
            sleep(10)
        raise RuntimeError('Cloud readiness deadline exceeded')

    def compare(self, cloud):
        if cloud.get('source_bytes') != self.selection['total_bytes'] or cloud.get('work_rows') != self.selection['record_count']:
            raise RuntimeError('Guest summary does not match the selected sample')
        if len(cloud.get('rebuild_hashes', [])) != 2 or len(set(cloud['rebuild_hashes'])) != 1:
            raise RuntimeError('Guest rebuild hashes did not agree')
        if sorted(cloud.get('timings', {})) != sorted(queries(cloud['seed_work_id'])):
            raise RuntimeError('Guest did not execute the complete query suite')
        comparisons = {}
        for name, sql in queries(cloud['seed_work_id']).items():
            expected = json.loads((self.out / 'cloud' / (name + '-rows.json')).read_text())
            expected_rows = canonical_rows(name, clickhouse_result_columns(name, expected))
            runs = []
            for repetition in range(3):
                rows, record = self.query(sql)
                actual = canonical_rows(name, rows)
                if actual != expected_rows:
                    write(self.out / (name + '-mismatch.json'), {'clickhouse_only': sorted(set(expected_rows) - set(actual))[:20],
                          'athena_only': sorted(set(actual) - set(expected_rows))[:20],
                          'clickhouse_rows': len(expected_rows), 'athena_rows': len(actual)})
                    raise RuntimeError(name + ' result mismatch')
                runs.append(record)
            comparisons[name] = {'matched': True, 'rows': len(expected_rows), 'athena_runs': runs,
                                 'clickhouse_runs': cloud['timings'][name]}
            write(self.out / 'comparisons.json', comparisons)
        return comparisons

    def cleanup(self):
        errors = []
        def attempt(label, fn):
            try:
                fn()
            except Exception as exc:
                errors.append({'action': label, 'error': str(exc)})
        for query in self.running_queries:
            attempt('stop Athena query ' + query, lambda q=query: self.clients['athena'].stop_query_execution(QueryExecutionId=q))
        instance = self.state.get('instance_id')
        if not instance and self.state.get('instance_profile'):
            # Reconcile a lost RunInstances response using this exact request's
            # idempotency token before deciding that no instance was launched.
            try:
                reservations = self.clients['ec2'].describe_instances(Filters=[
                    {'Name': 'client-token', 'Values': [self.name]},
                    {'Name': 'tag:RunId', 'Values': [self.name]},
                ])['Reservations']
                matches = [i['InstanceId'] for r in reservations for i in r['Instances']]
                if len(matches) > 1:
                    raise RuntimeError('Unexpected multiple instances for one launch token')
                if matches:
                    instance = matches[0]
                    self.record(instance_id=instance, recovered_launch_response=True)
            except Exception as exc:
                errors.append({'action': 'reconcile uncertain instance launch', 'error': str(exc)})
        terminated = False
        if instance:
            try:
                self.clients['ec2'].terminate_instances(InstanceIds=[instance])
                self.clients['ec2'].get_waiter('instance_terminated').wait(InstanceIds=[instance], WaiterConfig={'Delay': 5, 'MaxAttempts': 48})
                terminated = True
                volumes = self.clients['ec2'].describe_volumes(Filters=[
                    {'Name': 'tag:RunId', 'Values': [self.name]},
                    {'Name': 'tag:Project', 'Values': ['openalex-small-spike']},
                ])['Volumes']
                if volumes:
                    raise RuntimeError('Owned EBS volumes still exist after instance termination')
            except Exception as exc:
                errors.append({'action': 'terminate instance', 'error': str(exc)})
        # Keep the independent termination path intact if termination is uncertain.
        if self.state.get('schedule_created') and (terminated or not instance):
            attempt('delete schedule', lambda: self.clients['scheduler'].delete_schedule(Name=self.name))
        if self.state.get('database_created'):
            def delete_database():
                g = self.clients['glue']
                for page in g.get_paginator('get_tables').paginate(DatabaseName=self.db):
                    for table in page['TableList']:
                        g.delete_table(DatabaseName=self.db, Name=table['Name'])
                g.delete_database(Name=self.db)
            attempt('delete experiment catalog', delete_database)
        if self.state.get('workgroup_created'):
            attempt('delete workgroup', lambda: self.clients['athena'].delete_work_group(WorkGroup=self.name, RecursiveDeleteOption=True))
        if terminated or not instance:
            iam = self.clients['iam']
            if self.state.get('instance_profile'):
                role = self.state['guest_role']
                attempt('remove role from instance profile', lambda: iam.remove_role_from_instance_profile(InstanceProfileName=role, RoleName=role))
                attempt('delete instance profile', lambda: iam.delete_instance_profile(InstanceProfileName=role))
            for suffix, policy in (('guest', 'results-only'), ('expiry', 'terminate-exact-instance')):
                role = self.state.get(suffix + '_role')
                if role:
                    attempt('delete role policy ' + role, lambda r=role, p=policy: iam.delete_role_policy(RoleName=r, PolicyName=p))
                    attempt('delete role ' + role, lambda r=role: iam.delete_role(RoleName=r))
            if self.state.get('security_group'):
                attempt('delete security group', lambda: self.clients['ec2'].delete_security_group(GroupId=self.state['security_group']))
        self.record(cleanup_errors=errors, instance_termination_verified=terminated,
                    retained_bucket_reason='Only tiny manifests and query evidence, seven-day expiration')
        return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', action='store_true')
    args = parser.parse_args()
    selection = json.loads((HERE / 'proposed-sample-selection.json').read_text())
    validate_selection(selection)
    if not args.run:
        print(json.dumps({'mode': 'read-only preparation', 'source_bytes': selection['total_bytes'],
            'work_rows': selection['record_count'], 'instance': 'm7g.xlarge', 'hours_maximum': 2,
            'region': REGION, 'account': ACCOUNT, 'raw_s3_mirror': False}, indent=2))
        return
    if os.environ.get('OPENALEX_SMALL_SPIKE_APPROVAL') != 'SAMPLE-ONLY-US-EAST-1-USD3':
        raise RuntimeError('Execution approval marker is missing')
    for statefile in HERE.glob('oaspike-*/state.json'):
        previous = json.loads(statefile.read_text())
        if previous.get('instance_profile') and not previous.get('instance_termination_verified'):
            raise RuntimeError('An earlier run requires cleanup before a new instance may be launched: ' + str(statefile))
    selection = pin_sources(selection)
    write(HERE / 'pinned-sample-selection.json', selection)
    experiment = Experiment(selection)
    experiment.record(scope='small sample only, stop after first figures')
    try:
        experiment.setup_athena()
        experiment.launch()
        cloud = experiment.wait_cloud()
        # Stop compute immediately, while Athena comparisons run independently.
        experiment.clients['ec2'].terminate_instances(InstanceIds=[experiment.state['instance_id']])
        pin_sources(selection)
        comparisons = experiment.compare(cloud)
        pin_sources(selection)
        write(experiment.out / 'final-summary.json', {'cloud': cloud, 'comparisons': comparisons,
              'athena_bytes_scanned': sum(r['statistics'].get('DataScannedInBytes', 0) for r in experiment.query_records),
              'actual_billing': 'Not yet available; AWS billing is delayed',
              'scope': 'No full snapshot, no tuning or larger experiment'})
        experiment.record(outcome='passed')
    except BaseException as exc:
        experiment.record(outcome='failed', error=str(exc), traceback=traceback.format_exc())
        raise
    finally:
        errors = experiment.cleanup()
        print(json.dumps({'results': str(experiment.out), 'outcome': experiment.state.get('outcome'),
                          'cleanup_errors': errors}))
        if errors:
            raise RuntimeError('Experiment cleanup needs attention; see state.json')


if __name__ == '__main__':
    main()
