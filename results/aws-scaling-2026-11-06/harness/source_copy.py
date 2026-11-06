"""Temporary, approved, exact-data S3 copy. Defaults to read-only validation."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import uuid

import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError

from controls import validate_manifest, write

HERE = Path(__file__).resolve().parent
ACCOUNT = '502425560524'
REGION = 'us-east-1'
CACHE = Path('/Users/yorrickjansen/work/openalex/.worktrees/clickhouse-repeatability/.data/raw/objects')


class Sources:
    def __init__(self, session=None):
        self.session = session or boto3.Session(profile_name='certification', region_name=REGION)
        if self.session.region_name != REGION or self.session.client('sts').get_caller_identity()['Account'] != ACCOUNT:
            raise RuntimeError('Certification account/us-east-1 guard failed')
        self.s3 = self.session.client('s3')
        approval = json.loads((HERE / 'APPROVAL.json').read_text())
        if approval['account'] != ACCOUNT or approval['total_usd_envelope'] != 15 or not approval['user_confirmation']:
            raise RuntimeError('Recorded user approval is missing')
        self.manifest = json.loads((HERE / 'source-manifest.json').read_text())
        validate_manifest(self.manifest, CACHE)
        self.path = HERE / 'source-state.json'
        self.state = json.loads(self.path.read_text()) if self.path.exists() else {
            'account': ACCOUNT, 'region': REGION,
            'bucket': 'oascale-src-' + datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S') + '-' + uuid.uuid4().hex[:8] + '-' + ACCOUNT,
            'created_at': datetime.now(timezone.utc).isoformat(), 'created': False,
            'uploaded_files': 0, 'uploaded_bytes': 0}
        self.bucket = self.state['bucket']
        if not self.bucket.startswith('oascale-src-') or not self.bucket.endswith('-' + ACCOUNT) or self.state['account'] != ACCOUNT:
            raise RuntimeError('Unexpected source bucket identity')

    def fresh(self):
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(self.state['created_at'])).total_seconds()
        if age < 0 or age > 18 * 3600:
            raise RuntimeError('Source lease expired; no new tier may start')

    def create(self):
        self.fresh()
        write(self.path, self.state)
        if not self.state['created']:
            self.s3.create_bucket(Bucket=self.bucket)
            self.state['created'] = True
            write(self.path, self.state)
            self.s3.put_bucket_tagging(Bucket=self.bucket, Tagging={'TagSet': [{'Key': 'Project', 'Value': 'openalex-tier-scaling'}]})
        self.s3.put_public_access_block(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT,
            PublicAccessBlockConfiguration={k: True for k in ('BlockPublicAcls', 'IgnorePublicAcls', 'BlockPublicPolicy', 'RestrictPublicBuckets')})
        self.s3.put_bucket_ownership_controls(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT,
            OwnershipControls={'Rules': [{'ObjectOwnership': 'BucketOwnerEnforced'}]})
        self.s3.put_bucket_encryption(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT,
            ServerSideEncryptionConfiguration={'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]})
        self.s3.put_bucket_lifecycle_configuration(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT,
            LifecycleConfiguration={'Rules': [{'ID': 'expire-raw-copy', 'Status': 'Enabled', 'Filter': {'Prefix': 'raw/'},
                'Expiration': {'Days': 1}, 'AbortIncompleteMultipartUpload': {'DaysAfterInitiation': 1}}]})
        block = self.s3.get_public_access_block(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT)['PublicAccessBlockConfiguration']
        assert all(block.values()) and len(block) == 4
        assert self.s3.get_bucket_versioning(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT).get('Status') is None
        assert self.s3.get_bucket_location(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT)['LocationConstraint'] is None

    def upload(self):
        raise RuntimeError('Raw laptop uploads are forbidden by the user; use AWS server-side historical-version copies')

    def destroy(self):
        if not self.state['created']:
            return
        tags = self.s3.get_bucket_tagging(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT)['TagSet']
        if {'Key': 'Project', 'Value': 'openalex-tier-scaling'} not in tags:
            raise RuntimeError('Refusing to delete an unrecognized source bucket')
        if self.s3.get_bucket_versioning(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT).get('Status') is not None:
            raise RuntimeError('Unexpected source bucket versions')
        for page in self.s3.get_paginator('list_multipart_uploads').paginate(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT):
            for upload in page.get('Uploads', []):
                self.s3.abort_multipart_upload(Bucket=self.bucket, Key=upload['Key'],
                    UploadId=upload['UploadId'], ExpectedBucketOwner=ACCOUNT)
        for page in self.s3.get_paginator('list_objects_v2').paginate(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT):
            keys = [{'Key': x['Key']} for x in page.get('Contents', [])]
            if keys:
                result = self.s3.delete_objects(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT, Delete={'Objects': keys})
                if result.get('Errors'):
                    raise RuntimeError('Source-object cleanup was incomplete')
        self.s3.delete_bucket(Bucket=self.bucket, ExpectedBucketOwner=ACCOUNT)
        self.state['deleted'] = True
        write(self.path, self.state)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--upload', action='store_true')
    parser.add_argument('--destroy', action='store_true')
    args = parser.parse_args()
    if args.upload:
        raise RuntimeError('Laptop uploads are forbidden; use server_copy.py')
    if args.upload and args.destroy:
        raise RuntimeError('Choose one operation')
    sources = Sources()
    if args.upload:
        try:
            sources.upload()
        except BaseException:
            sources.destroy()
            raise
    elif args.destroy:
        sources.destroy()
    else:
        print(json.dumps({'mode': 'read-only', 'files': len(sources.manifest['files']), 'bytes': sources.manifest['bytes']}))
