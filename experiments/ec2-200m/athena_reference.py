"""Bounded raw-S3 Athena reference, immutable versions, no laptop data uploads."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import base64
import hashlib
import json
import math
import time
import uuid

import boto3
import pyarrow as pa
import pyarrow.csv as pc

from helpers import HERE, dump
from tier_sql import PROJECTION, external_table, views, queries, canonical_rows

ACCOUNT = '502425560524'
REGION = 'us-east-1'
PROJECT = 'openalex-ec2-200m'
OLD = HERE
ROOT = Path('/Users/yorrickjansen/work/openalex')
CAP = 128_000_000_000
TOTAL = 1_600_000_000_000


class Reference:
    def __init__(self):
        self.session = boto3.Session(profile_name='certification', region_name=REGION)
        assert self.session.client('sts').get_caller_identity()['Account'] == ACCOUNT
        self.s3 = self.session.client('s3')
        self.athena = self.session.client('athena')
        self.glue = self.session.client('glue')
        path = HERE / 'aws-state.json'
        if path.exists():
            self.state = json.loads(path.read_text())
        else:
            suffix = uuid.uuid4().hex[:8]
            self.state = {'account': ACCOUNT, 'region': REGION, 'project': PROJECT,
                          'created_at': time.time(), 'bucket': f'oapg100-20261109-{suffix}-{ACCOUNT}',
                          'workgroup': f'oapg100-20261109-{suffix}', 'database': f'oapg100_20261109_{suffix}',
                          'bucket_created': False, 'workgroup_created': False, 'database_created': False}
            dump(path, self.state)
        assert self.state['account'] == ACCOUNT and self.state['region'] == REGION
        assert self.state['bucket'].startswith('oa200-') and self.state['bucket'].endswith(ACCOUNT)
        self.bucket = self.state['bucket']
        self.db = self.state['database']
        self.workgroup = self.state['workgroup']
        self.records = json.loads((HERE / 'athena-statements.json').read_text()) if (HERE / 'athena-statements.json').exists() else []

    def save(self):
        dump(HERE / 'aws-state.json', self.state)

    def fresh(self):
        assert 0 <= time.time() - self.state['created_at'] < 12 * 3600, 'Temporary source lease expired'

    def create_bucket(self):
        self.fresh()
        if not self.state['bucket_created']:
            self.s3.create_bucket(Bucket=self.bucket)
            self.state['bucket_created'] = True
            self.save()
            self.s3.put_bucket_tagging(Bucket=self.bucket, Tagging={'TagSet': [{'Key': 'Project', 'Value': PROJECT}]})
        assert {'Key': 'Project', 'Value': PROJECT} in self.s3.get_bucket_tagging(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT)['TagSet']
        self.s3.put_public_access_block(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT,
            PublicAccessBlockConfiguration={k: True for k in ('BlockPublicAcls', 'IgnorePublicAcls', 'BlockPublicPolicy', 'RestrictPublicBuckets')})
        self.s3.put_bucket_ownership_controls(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT,
            OwnershipControls={'Rules': [{'ObjectOwnership': 'BucketOwnerEnforced'}]})
        self.s3.put_bucket_encryption(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT,
            ServerSideEncryptionConfiguration={'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]})
        self.s3.put_bucket_lifecycle_configuration(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT,
            LifecycleConfiguration={'Rules': [{'ID': 'expire-temporary-series', 'Status': 'Enabled', 'Filter': {'Prefix': ''},
                'Expiration': {'Days': 1}, 'AbortIncompleteMultipartUpload': {'DaysAfterInitiation': 1}}]})
        assert all(self.s3.get_public_access_block(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT)['PublicAccessBlockConfiguration'].values())
        assert self.s3.get_bucket_versioning(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT).get('Status') is None
        assert self.s3.get_bucket_location(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT)['LocationConstraint'] is None

    def inputs(self):
        manifest=json.loads((HERE/'input-manifest.json').read_text())
        result=[]
        for f in manifest['inputs']:
            f=dict(f)
            f['key']='raw/'+f['entity']+'/'+hashlib.sha256(f['source_key'].encode()).hexdigest()+'.parquet'
            f['url']='s3://'+self.bucket+'/'+f['key']
            result.append(f)
        assert sum(f['rows'] for f in result if f['entity']=='works')==200313862
        return result

    def restore(self):
        path = HERE / 'remote-inputs.json'
        if path.exists():
            return json.loads(path.read_text())['files']
        self.create_bucket()
        inputs = self.inputs()
        dump(HERE / 'copy-plan.json', {'source_snapshot': '2026-06-26', 'method': 'AWS CopyObject from immutable public versions; no raw laptop upload',
                                     'files': len(inputs), 'bytes': sum(f['bytes'] for f in inputs), 'inputs': inputs})

        def one(f):
            self.fresh()
            response = self.s3.copy_object(Bucket=self.bucket, Key=f['key'], ExpectedBucketOwner=ACCOUNT,
                CopySource={'Bucket': 'openalex', 'Key': f['source_key'], 'VersionId': f['version_id']},
                CopySourceIfMatch=f['source_etag'], ChecksumAlgorithm='SHA256', ServerSideEncryption='AES256',
                MetadataDirective='REPLACE', Metadata={'source-version': f['version_id'], 'rows': str(f['rows']), 'snapshot': '2026-06-26'})
            h = self.s3.head_object(Bucket=self.bucket, Key=f['key'], ExpectedBucketOwner=ACCOUNT, ChecksumMode='ENABLED')
            assert h['ContentLength'] == f['bytes'] and h.get('ChecksumType') == 'FULL_OBJECT'
            assert h.get('ServerSideEncryption') == 'AES256'
            digest = base64.b64decode(h['ChecksumSHA256']).hex()
            if f['known_sha256']:
                assert digest == f['known_sha256'], f['source_key']
            return {**f, 'server_full_sha256': digest, 'verified_against_prior_full_sha256': bool(f['known_sha256'])}

        restored = []
        with ThreadPoolExecutor(max_workers=8) as pool:
            for f in pool.map(one, inputs):
                restored.append(f)
                if len(restored) % 100 == 0:
                    dump(HERE / 'copy-progress.json', {'files_complete': len(restored), 'bytes_complete': sum(x['bytes'] for x in restored)})
                    print('Copied insideAWS', len(restored), 'files', flush=True)
        dump(path, {'snapshot': '2026-06-26', 'files': restored, 'known_sha256_matches': sum(f['verified_against_prior_full_sha256'] for f in restored),
                    'new_object_sha256_recorded': sum(not f['verified_against_prior_full_sha256'] for f in restored)})
        return restored

    def query(self, sql, use_db=True, dml_override=None, timeout=300):
        self.fresh()
        dml = sql.lstrip().upper().startswith(('SELECT', 'WITH')) if dml_override is None else dml_override
        used = sum(r.get('billable_bytes', CAP if r.get('dml') else 0) for r in self.records)
        if dml and used + CAP > TOTAL:
            raise RuntimeError('Athena series scan budget cannot reserve another query')
        record = {'sql': sql, 'dml': dml, 'state': 'starting', 'at': time.time()}
        self.records.append(record)
        dump(HERE / 'athena-statements.json', self.records)
        args = {'QueryString': sql, 'WorkGroup': self.workgroup, 'ClientRequestToken': uuid.uuid4().hex + uuid.uuid4().hex,
                'ResultReuseConfiguration': {'ResultReuseByAgeConfiguration': {'Enabled': False}}}
        if use_db:
            args['QueryExecutionContext'] = {'Database': self.db, 'Catalog': 'AwsDataCatalog'}
        qid = self.athena.start_query_execution(**args)['QueryExecutionId']
        record.update(id=qid, state='started')
        dump(HERE / 'athena-statements.json', self.records)
        start = time.monotonic()
        while True:
            q = self.athena.get_query_execution(QueryExecutionId=qid)['QueryExecution']
            if q['Status']['State'] in ('SUCCEEDED', 'FAILED', 'CANCELLED'):
                break
            if time.monotonic() - start > timeout:
                self.athena.stop_query_execution(QueryExecutionId=qid)
            if time.monotonic() - start > timeout + 60:
                raise RuntimeError('Athena cancellation unresolved; reservation remains held')
            time.sleep(1)
        scanned = q.get('Statistics', {}).get('DataScannedInBytes', 0)
        billed = max(10_000_000, math.ceil(scanned / 1_000_000) * 1_000_000) if dml else 0
        record.update(state=q['Status']['State'], statistics=q.get('Statistics', {}), status=q['Status'],
                      billable_bytes=billed, client_seconds=time.monotonic() - start, engine=q.get('EngineVersion'))
        dump(HERE / 'athena-statements.json', self.records)
        assert q['WorkGroup'] == self.workgroup and q['EngineVersion']['EffectiveEngineVersion'] == 'Athena engine version 3'
        if q['Status']['State'] != 'SUCCEEDED':
            raise RuntimeError('Athena query incomplete: ' + json.dumps(record['status'], default=str))
        if not dml or sql.lstrip().upper().startswith('CREATE TABLE'):
            return [], record
        cols = [c['Name'] for c in self.athena.get_query_results(QueryExecutionId=qid, MaxResults=1)['ResultSet']['ResultSetMetadata']['ColumnInfo']]
        loc = urlparse(q['ResultConfiguration']['OutputLocation'])
        assert loc.netloc == self.bucket and loc.path.startswith('/athena/')
        data = self.s3.get_object(Bucket=self.bucket, Key=loc.path.lstrip('/'), ExpectedBucketOwner=ACCOUNT)['Body'].read()
        table = pc.read_csv(pa.BufferReader(data), parse_options=pc.ParseOptions(newlines_in_values=True),
            convert_options=pc.ConvertOptions(column_types={c: pa.string() for c in cols}, strings_can_be_null=True,
                                               quoted_strings_can_be_null=False, null_values=['']))
        assert table.column_names == cols
        return table.to_pylist(), record

    def setup(self, files):
        if self.state.get('setup_complete'):
            return
        if not self.state['workgroup_created']:
            self.athena.create_work_group(Name=self.workgroup, Tags=[{'Key': 'Project', 'Value': PROJECT}], Configuration={
                'EnforceWorkGroupConfiguration': True, 'BytesScannedCutoffPerQuery': CAP,
                'EngineVersion': {'SelectedEngineVersion': 'Athena engine version 3'},
                'ResultConfiguration': {'OutputLocation': 's3://' + self.bucket + '/athena/', 'ExpectedBucketOwner': ACCOUNT,
                                        'EncryptionConfiguration': {'EncryptionOption': 'SSE_S3'}}})
            self.state['workgroup_created'] = True
            self.save()
        c = self.athena.get_work_group(WorkGroup=self.workgroup)['WorkGroup']['Configuration']
        assert c['BytesScannedCutoffPerQuery'] == CAP and c['EnforceWorkGroupConfiguration']
        if not self.state['database_created']:
            self.query('CREATE DATABASE ' + self.db, use_db=False)
            self.state['database_created'] = True
            self.save()
        sentinel = "SELECT CAST(NULL AS varchar) AS n,'' AS e,true AS b,CAST('9007199254740993' AS bigint) AS i,concat('a',chr(10),'b\"c') AS s,'null' AS literal"
        rows, _ = self.query(sentinel)
        assert rows == [{'n': None, 'e': '', 'b': 'true', 'i': '9007199254740993', 's': 'a\nb"c', 'literal': 'null'}]
        dump(HERE / 'results/athena-csv-probe.json', {'passed': True, 'rows': rows})
        for entity in PROJECTION:
            selected = [f for f in files if f['entity'] == entity]
            key = f'manifests/{entity}/files.txt'
            self.s3.put_object(Bucket=self.bucket, Key=key, ExpectedBucketOwner=ACCOUNT,
                               Body=('\n'.join(f['url'] for f in selected) + '\n').encode(), ServerSideEncryption='AES256')
            schema = pa.ipc.read_schema(pa.BufferReader((OLD / 'schemas' / (entity + '.arrow')).read_bytes()))
            self.query(external_table(entity, schema, f's3://{self.bucket}/manifests/{entity}/'))
            rows, _ = self.query(f'SELECT "$path" AS path,count(*) AS n_rows FROM raw_{entity} GROUP BY "$path"')
            assert {r['path']: int(r['n_rows']) for r in rows} == {f['url']: f['rows'] for f in selected}
        for name, sql in views().items():
            self.query('CREATE VIEW ' + name + ' AS ' + sql)
        self.state['setup_complete'] = True
        self.save()

    def benchmark(self):
        path = HERE / 'athena-cases.json'
        cases = json.loads(path.read_text()) if path.exists() else {}
        catalog = {}
        for seed in (51557542, 24222542, 2003585639):
            for name, sql in queries(seed).items():
                catalog[name + ('-s' + str(seed) if name in ('q05', 'q06') else '')] = sql
        for name, sql in catalog.items():
            result = cases.setdefault(name, {'sql': sql, 'runs': []})
            while len(result['runs']) < 3:
                rows, record = self.query(sql)
                canonical = canonical_rows(name[:3], rows)
                digest = hashlib.sha256('\n'.join(canonical).encode()).hexdigest()
                if result['runs']:
                    assert digest == result['runs'][0]['canonical_sha256'] and len(rows) == result['runs'][0]['rows']
                result['runs'].append({'query_id': record['id'], 'statistics': record['statistics'], 'rows': len(rows), 'canonical_sha256': digest})
                dump(path, cases)
                print('Athena', name, 'run', len(result['runs']), round(record['statistics']['TotalExecutionTimeInMillis'] / 1000, 3), 'seconds', flush=True)
        self.state['athena_complete'] = True
        self.save()


if __name__ == '__main__':
    a = Reference()
    files = a.restore()
    a.setup(files)
    a.benchmark()
