from pathlib import Path
import json,boto3,hashlib,tarfile
HERE=Path(__file__).resolve().parent;c=json.loads((HERE/'cloud-state.json').read_text());s=boto3.Session(profile_name='certification',region_name='us-east-1');assert s.client('sts').get_caller_identity()['Account']==c['account'];s3=s.client('s3')
p=HERE/'frozen-evidence.tar.gz';s3.download_file(c['bucket'],'run/final/frozen-evidence.json',str(HERE/'frozen-evidence.json'));proof=json.loads((HERE/'frozen-evidence.json').read_text());s3.download_file(c['bucket'],'run/final/frozen-evidence.tar.gz',str(p));assert p.stat().st_size==proof['archive_bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==proof['archive_sha256']
root=HERE/'frozen';root.mkdir(exist_ok=True)
with tarfile.open(p) as tar:
 for f in tar.getmembers():assert f.isfile() and not f.name.startswith('/') and '..' not in Path(f.name).parts
 tar.extractall(root,filter='data')
m=json.loads((root/'results/frozen-manifest.json').read_text())
for f in m['files']:
 path=root/f['path'];assert path.stat().st_size==f['bytes'] and hashlib.sha256(path.read_bytes()).hexdigest()==f['sha256'],f['path']
# All later checks use the frozen tree; replace the earlier incremental cache with a directory link.
cache=HERE/'cloud-results'
if cache.exists() and not cache.is_symlink():cache.rename(HERE/'cloud-results-incremental')
if not cache.exists():cache.symlink_to(root/'results',target_is_directory=True)
print('Verified archive SHA and all',len(m['files']),'frozen artifact hashes')
