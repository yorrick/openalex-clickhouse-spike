"""Publish complete query evidence and preparation summaries, excluding raw datasets."""
from pathlib import Path
import json,gzip,hashlib,shutil
HERE=Path(__file__).resolve().parent;root=HERE/'cloud-results'
out=Path('/Users/yorrickjansen/work/openalex/.claude/worktrees/ec2-200m/results/ec2-200m-2026-11-12');out.mkdir(exist_ok=True)
assert json.loads((HERE/'results/verification.json').read_text())['verified'] is True
files={}
for p in root.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(root)
 if p.suffix=='.json':
  # Keep every query trace. Preparation has separately retained full traces in
  # the frozen local archive, while this public bundle keeps their summaries.
  if p.name.endswith('-telemetry.json') and not p.name.startswith('q0'):continue
  if 'projection' in rel.parts:continue
  files[str(rel)]=json.loads(p.read_text())
 elif p.name in ['runtime.log','runtime-repair.log','version.txt']:files[str(rel)]=p.read_text()
encoded=json.dumps({'scope':'All native query traces and case profiles, source receipts, normalization QA and preparation summaries. Full preparation traces and host telemetry remain in the frozen archive. Raw OpenAlex datasets and database files are excluded.','files':files},separators=(',',':'),ensure_ascii=False).encode()
dest=out/'benchmark-evidence.json.gz'
with gzip.GzipFile(filename=str(dest),mode='wb',compresslevel=6,mtime=0) as f:f.write(encoded)
with gzip.open(dest,'rb') as f:assert f.read()==encoded
for name in ['verification.json','native-summary.json','cost-estimate.json','aws-cleanup.json','athena-full-csv-archive.json']:
 shutil.copy2(HERE/'results'/name,out/name)
shutil.copy2(HERE/'frozen-evidence.json',out/'frozen-evidence.json')
shutil.copy2(HERE/'frozen-evidence.tar.gz',out/'frozen-evidence.tar.gz')
proof={'bundle_bytes':dest.stat().st_size,'bundle_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'json_bytes':len(encoded),'included_files':len(files),'frozen_full_archive':str(HERE/'frozen-evidence.tar.gz'),'frozen_archive_sha256':json.loads((HERE/'frozen-evidence.json').read_text())['archive_sha256']}
(out/'evidence-bundle.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
