"""Restore exact historical object versions inside AWS for Athena and EBS prep."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import base64
import json

from botocore.exceptions import ClientError

from controls import write
from source_copy import Sources, ACCOUNT

HERE = Path(__file__).resolve().parent


def main():
    source = Sources()
    if source.state.get('complete'):
        print('Historical copy already complete; no mutation requested.', flush=True)
        return
    versioned = json.loads((HERE / 'historical-versions.json').read_text())
    if versioned['missing'] or len(versioned['files']) != 2771:
        raise RuntimeError('Historical version resolution is incomplete')
    source.create()
    tags = source.s3.get_bucket_tagging(Bucket=source.bucket, ExpectedBucketOwner=ACCOUNT)['TagSet']
    if {'Key': 'Project', 'Value': 'openalex-tier-scaling'} not in tags:
        raise RuntimeError('Source bucket identity is unrecognized')
    if source.manifest['source_date'] != '2026-06-26':
        raise RuntimeError('Unexpected source snapshot')

    def one(f):
        source.fresh()
        try:
            h = source.s3.head_object(Bucket=source.bucket, Key=f['key'],
                                     ExpectedBucketOwner=ACCOUNT, ChecksumMode='ENABLED')
        except ClientError as exc:
            if exc.response['Error']['Code'] not in ('404', 'NoSuchKey'):
                raise
            h = None
        selected = None
        if h is None:
            for candidate in f['candidates']:
                response = source.s3.copy_object(
                    Bucket=source.bucket, Key=f['key'], ExpectedBucketOwner=ACCOUNT,
                    CopySource={'Bucket': 'openalex', 'Key': f['source_key'], 'VersionId': candidate['version_id']},
                    CopySourceIfMatch=candidate['etag'], ChecksumAlgorithm='SHA256',
                    ServerSideEncryption='AES256', MetadataDirective='REPLACE',
                    Metadata={'sha256': f['sha256'], 'rows': str(f['rows']),
                              'source-version': candidate['version_id'], 'original-url': f['original_url']})
                h = source.s3.head_object(Bucket=source.bucket, Key=f['key'],
                                         ExpectedBucketOwner=ACCOUNT, ChecksumMode='ENABLED')
                digest = base64.b64decode(h['ChecksumSHA256']).hex()
                if h.get('ChecksumType') != 'FULL_OBJECT':
                    raise RuntimeError('Server checksum does not cover the full object')
                if digest == f['sha256']:
                    selected = candidate
                    break
                source.s3.delete_object(Bucket=source.bucket, Key=f['key'], ExpectedBucketOwner=ACCOUNT)
                h = None
            if h is None:
                raise RuntimeError('No historical version matches the original full-object SHA256: ' + f['original_url'])
        else:
            version_id = h.get('Metadata', {}).get('source-version')
            selected = next((v for v in f['candidates'] if v['version_id'] == version_id), None)
        if (selected is None or h['ContentLength'] != f['bytes'] or h.get('ServerSideEncryption') != 'AES256'
            or h.get('ChecksumType') != 'FULL_OBJECT'
            or base64.b64decode(h['ChecksumSHA256']).hex() != f['sha256']):
            raise RuntimeError('Restored object failed cryptographic identity verification')
        return {k: v for k, v in f.items() if k != 'candidates'} | {
            'version_id': selected['version_id'], 'source_etag': selected['etag'],
            'etag': h['ETag'], 'url': f"s3://{source.bucket}/{f['key']}",
            'server_full_sha256_verified': True}

    restored = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for f in pool.map(one, versioned['files']):
            restored.append(f)
            if len(restored) % 50 == 0:
                source.state.update(copied_files=len(restored), copied_bytes=sum(x['bytes'] for x in restored), method='AWS CopyObject with pinned public version IDs')
                write(source.path, source.state)
                print(json.dumps({'copied_files': len(restored), 'copied_bytes': source.state['copied_bytes']}), flush=True)
    if len(restored) != 2771 or sum(f['bytes'] for f in restored) != 98_301_763_421:
        raise RuntimeError('Restored dataset totals differ')
    write(HERE / 'remote-manifest.json', {'bucket': source.bucket,
          'files': restored, 'tiers': source.manifest['tiers'],
          'source_date': '2026-06-26', 'created_at': source.state['created_at'],
          'origin': 'OpenAlex S3 historical object versions, AWS server-side copy only'})
    source.state.update(complete=True, copied_files=len(restored), copied_bytes=sum(x['bytes'] for x in restored),
                        raw_laptop_upload=False, all_server_sha256_match=True)
    write(source.path, source.state)
    print(json.dumps({'complete': True, 'files': len(restored), 'bytes': source.state['copied_bytes'], 'all_sha256_verified': True}), flush=True)


if __name__ == '__main__':
    main()
