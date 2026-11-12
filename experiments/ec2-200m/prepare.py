from pathlib import Path
import json,sys,datetime,hashlib
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'openalex-postgres-100m-20261109'
ROOT=Path('/Users/yorrickjansen/work/openalex/.claude/worktrees/ec2-200m')
sys.path.insert(0,str(ROOT/'src'))
from openalex_spike.manifest import EntityManifest
from openalex_spike.sampling import _stratify

def dump(p,v):p.write_text(json.dumps(v,indent=2,default=str)+'\n')
m=EntityManifest.from_path(Path('/Users/yorrickjansen/work/openalex/.worktrees/clickhouse-repeatability/.data/manifests/works-manifest.json'))
previous=json.loads((OLD/'works-input-manifest.json').read_text())
candidates=_stratify(m.files,previous['seed']);queues={s:sorted([f for f in candidates if f.stratum==s],key=lambda f:f.rank) for s in range(4)}
files=previous['files'].copy();used={f['url'] for f in files};counts={s:sum(f['content_length'] for f in files if f['stratum']==s) for s in range(4)}
n=sum(f['record_count'] for f in files)
while n<200_000_000:
 s=min((s for s in range(4) if any(f.url not in used for f in queues[s])),key=lambda s:(counts[s],s))
 chosen=next(f for f in queues[s] if f.url not in used);f=vars(chosen).copy();f.update(entity='works',source_key=f['url'].split('s3://openalex/',1)[1]);files.append(f);used.add(f['url']);counts[s]+=f['content_length'];n+=f['record_count']
versions=json.loads((OLD/'public-work-versions.json').read_text())['Versions'];cutoff=datetime.datetime.fromisoformat(previous['cutoff'])
bykey={}
for v in versions:
 if datetime.datetime.fromisoformat(v['LastModified'])<=cutoff:bykey.setdefault(v['Key'],[]).append(v)
known={f['source_key']:f for f in json.loads((OLD/'remote-inputs.json').read_text())['files']}
for f in files:
 if not f.get('version_id'):
  matches=[v for v in bykey.get(f['source_key'],[]) if v['Size']==f['content_length']]
  assert matches, f['source_key'];v=max(matches,key=lambda v:v['LastModified']);f.update(version_id=v['VersionId'],source_etag=v['ETag'],version_modified=v['LastModified'])
 f.pop('read_uri',None)
 if f['source_key'] in known:f['known_full_sha256']=known[f['source_key']]['server_full_sha256']
inputs=[]
for f in json.loads((OLD/'remote-inputs.json').read_text())['files']:
 if f['entity']!='works':inputs.append(dict(entity=f['entity'],source_key=f['source_key'],version_id=f['version_id'],bytes=f['bytes'],rows=f['rows'],known_sha256=f['server_full_sha256']))
for f in files:inputs.append(dict(entity='works',source_key=f['source_key'],version_id=f['version_id'],bytes=f['content_length'],rows=f['record_count'],known_sha256=f.get('known_full_sha256')))
out={'snapshot_date':m.date,'historical_total_works':m.record_count,'selection_algorithm':'Extend historical cumulative-bytes-four-strata-v2 prefix by least-filled byte stratum, same seed, until records>=200m','seed':previous['seed'],'prior_100m_files_preserved':len(previous['files']),'works':n,'works_files':len(files),'raw_work_bytes':sum(f['content_length'] for f in files),'all_raw_bytes':sum(f['bytes'] for f in inputs),'files':files,'inputs':inputs}
dump(HERE/'input-manifest.json',out)
print(json.dumps({k:v for k,v in out.items() if k not in ['files','inputs']}))
assert {f['url'] for f in previous['files']}<=used
assert n>=200_000_000 and n<201_000_000
