"""Cheap EC2 input staging, direct from immutable public OpenAlex S3 versions."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime, timezone
from scope import validate_scope, manifest_identity
from time import monotonic, sleep
import errno
import hashlib
import json
import os
import re
import subprocess
import traceback

import boto3
from botocore import UNSIGNED
from botocore.config import Config
import pyarrow.parquet as pq

BASE = Path('/root/work/data/openalex-small-spike')
MOUNT = Path('/mnt/openalex-input')
OUT = BASE / 'prep-results'
BUCKET = os.environ['SPIKE_BUCKET']
ACCOUNT = '502425560524'
S3 = boto3.client('s3', region_name='us-east-1')
PUBLIC = boto3.client('s3', region_name='us-east-1', config=Config(signature_version=UNSIGNED, max_pool_connections=8))
DEADLINE = monotonic() + 100 * 60


def run(args, *, check=True):
    p = subprocess.run(args, text=True, capture_output=True)
    if check and p.returncode:
        raise RuntimeError(str(args) + ': ' + p.stderr[-4000:])
    return p


def save(name, value):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    path.write_text(json.dumps(value, indent=2) + '\n')
    S3.upload_file(str(path), BUCKET, 'run/cloud/' + name)


def find_device(volume_id):
    if not re.fullmatch('vol-[0-9a-f]{8,17}', volume_id):
        raise RuntimeError('Invalid data-volume ID')
    serial = volume_id.replace('-', '')
    for _ in range(120):
        devices = json.loads(run(['lsblk', '-J', '-p', '-o', 'NAME,SERIAL,TYPE,MOUNTPOINT']).stdout)['blockdevices']
        matches = [d for d in devices if str(d.get('serial', '')).strip() == serial and d['type'] == 'disk']
        if len(matches) == 1:
            d = matches[0]
            if d.get('mountpoint') or any(c.get('mountpoint') for c in d.get('children', [])):
                raise RuntimeError('Target data volume is already mounted, refusing format')
            return d['name']
        sleep(1)
    raise RuntimeError('Expected EBS NVMe serial did not appear')


def mount_and_test(device, series_id, *, fresh_volume):
    MOUNT.mkdir(parents=True, exist_ok=True)
    # This preparation path formats ONLY a newly created, controller-owned volume.
    # Existing/partial disks are retained and require a separate recovery path.
    if fresh_volume is not True:
        raise RuntimeError('Formatting requires explicit newly-created-volume proof')
    fs=run(['blkid','-p','-o','export',device],check=False)
    signatures=run(['wipefs','--no-act','--json',device])
    if fs.returncode!=2 or fs.stdout.strip() or json.loads(signatures.stdout).get('signatures'):
        raise RuntimeError('Disk is not blank; refusing to mount writable or format')
    size=int(run(['blockdev','--getsize64',device]).stdout)
    if size!=120*(1<<30):
        raise RuntimeError('Fresh input disk size differs')
    # Fresh EBS is logically empty but raw reads may be pseudorandom, not zero.
    # Creation ownership + exact NVMe identity + no signatures authorize format.
    # AWS: https://docs.aws.amazon.com/ebs/latest/userguide/data-protection.html
    run(['mkfs.ext4','-m','0','-L','OPENALEX_RAW',device])
    run(['mount', '-t', 'ext4', device, str(MOUNT)])
    marker = MOUNT / 'owner.json'
    if marker.exists():
        if json.loads(marker.read_text())['series_id'] != series_id:
            raise RuntimeError('Existing raw volume belongs to another dataset')
    else:
        if any(x.name != 'lost+found' for x in MOUNT.iterdir()):
            raise RuntimeError('Unrecognized populated data volume')
        marker.write_text(json.dumps({'series_id': series_id}) + '\n')
    probe = MOUNT / '.readonly-probe'
    probe.write_bytes(b'read-only-input-control')
    run(['sync'])
    run(['umount', str(MOUNT)])
    run(['blockdev', '--setro', device])
    run(['mount', '-t', 'ext4', '-o', 'ro,noload', device, str(MOUNT)])
    if run(['blockdev', '--getro', device]).stdout.strip() != '1' or not (os.statvfs(MOUNT).f_flag & os.ST_RDONLY):
        raise RuntimeError('Read-only mount control failed')
    if probe.read_bytes() != b'read-only-input-control':
        raise RuntimeError('Read-only input contents changed')
    try:
        (MOUNT / '.must-not-write').write_bytes(b'x')
    except OSError as exc:
        if exc.errno != errno.EROFS:
            raise
    else:
        raise RuntimeError('Read-only volume accepted a write')
    run(['umount', str(MOUNT)])
    run(['blockdev', '--setrw', device])
    run(['mount', '-t', 'ext4', device, str(MOUNT)])
    probe.unlink()
    return {'serial_matched': True, 'read_only_mount_verified': True,
            'write_attempt_errno': 'EROFS', 'device': device}


def main():
    if os.geteuid() != 0:
        raise RuntimeError('Preparation requires root on its dedicated instance')
    config = json.loads((BASE / 'selection.json').read_text())
    global DEADLINE
    DEADLINE=monotonic()+max(0,(datetime.fromisoformat(config['work_deadline_at'])-datetime.now(timezone.utc)).total_seconds())
    if DEADLINE-monotonic()<85*60:
        raise RuntimeError('Insufficient fresh preparation window, refusing disk operations')
    validate_scope(config)
    files = config['files']
    if len(files) != 2771 or sum(f['bytes'] for f in files) != 98_301_763_421:
        raise RuntimeError('Preparation input scope differs from approval')
    save('status.json', {'state': 'waiting_for_raw_volume'})
    device = find_device(config['raw_volume_id'])
    proof = mount_and_test(device, config['series_id'],fresh_volume=config.get('fresh_volume'))
    save('mount-control.json', proof)
    raw = MOUNT / 'raw'
    objects = raw / 'objects'
    objects.mkdir(parents=True, exist_ok=True)
    started = monotonic()

    def one(f):
        if monotonic() > DEADLINE:
            raise RuntimeError('Preparation deadline reached')
        if not f['source_key'].startswith('data/parquet/') or not re.fullmatch('[0-9a-f]{64}', f['sha256']):
            raise RuntimeError('Unrecognized source identity')
        filename = hashlib.sha256(f['original_url'].encode()).hexdigest() + '.parquet'
        target = objects / filename
        if target.exists():
            digest = hashlib.sha256()
            with target.open('rb') as stream:
                for chunk in iter(lambda: stream.read(4 << 20), b''):
                    digest.update(chunk)
            if target.stat().st_size != f['bytes'] or digest.hexdigest() != f['sha256']:
                raise RuntimeError('Existing raw file differs; no replacement fallback')
        else:
            r = PUBLIC.get_object(Bucket='openalex', Key=f['source_key'],
                                  VersionId=f['version_id'], IfMatch=f['source_etag'])
            if r['ContentLength'] != f['bytes']:
                raise RuntimeError('Historical object length differs')
            temporary = target.with_suffix('.partial')
            digest = hashlib.sha256()
            count = 0
            with temporary.open('wb') as output:
                for chunk in r['Body'].iter_chunks(4 << 20):
                    count += len(chunk)
                    if count > f['bytes'] or monotonic() > DEADLINE:
                        raise RuntimeError('Download exceeded byte/time bound')
                    digest.update(chunk)
                    output.write(chunk)
                output.flush()
                os.fsync(output.fileno())
            if count != f['bytes'] or digest.hexdigest() != f['sha256']:
                raise RuntimeError('Historical object checksum differs from original dataset')
            temporary.replace(target)
        readback=hashlib.sha256()
        with target.open('rb') as stream:
            for chunk in iter(lambda:stream.read(4<<20),b''):
                readback.update(chunk)
        if readback.hexdigest()!=f['sha256']:
            raise RuntimeError('Filesystem SHA256 readback differs')
        if pq.read_metadata(target).num_rows != f['rows']:
            raise RuntimeError('Parquet row count differs')
        return {'key': f['key'], 'filename': filename, 'entity': f['entity'],
                'bytes': target.stat().st_size, 'rows': pq.read_metadata(target).num_rows, 'sha256': readback.hexdigest(), 'original_url':f['original_url']}

    downloaded = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for f in pool.map(one, files):
            downloaded.append(f)
            if len(downloaded) % 20 == 0:
                save('status.json', {'state': 'downloading_direct_from_openalex',
                     'files': len(downloaded), 'bytes': sum(x['bytes'] for x in downloaded),
                     'elapsed_seconds': monotonic() - started})
    validate_scope(config,downloaded)
    indexed = {f['key']: f for f in downloaded}
    for tier, description in config['tiers'].items():
        for key in description['keys']:
            f = indexed[key]
            target = raw / 'tiers' / tier / f['entity'] / f['filename']
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                os.link(objects / f['filename'], target)
    summary = {'state': 'complete', 'series_id': config['series_id'],
               'raw_volume_id': config['raw_volume_id'], 'manifest_identity':manifest_identity(config), 'files': len(downloaded),
               'bytes': sum(f['bytes'] for f in downloaded),
               'elapsed_seconds': monotonic() - started, 'all_sha256_match': True, 'filesystem_readback_sha256_verified':True,
               'filesystem_uuid': run(['blkid', '-o', 'value', '-s', 'UUID', device]).stdout.strip(),
               'mount_control': proof, 'tiers': config['tiers']}
    (MOUNT/'verified-files.json').write_text(json.dumps(downloaded,indent=2)+'\n')
    (MOUNT / 'dataset.json').write_text(json.dumps(summary, indent=2) + '\n')
    run(['sync'])
    run(['umount', str(MOUNT)])
    save('summary.json', summary)
    save('status.json', {'state': 'complete', 'raw_volume_unmounted': True})


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        save('status.json', {'state': 'failed', 'error': str(exc), 'traceback': traceback.format_exc()})
        run(['sync'], check=False)
        run(['umount', str(MOUNT)], check=False)
        raise
