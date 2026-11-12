"""Collect static input/storage metadata only after every native timing is settled."""
from pathlib import Path
import json,subprocess,time,collections
import pyarrow.parquet as pq
import run_engines as e
from helpers import HERE,dump
assert (HERE/'results/postgres/repair-complete.json').exists()
assert (HERE/'results/clickhouse/grace16-complete.json').exists()
for name in [e.PG,e.CH]:assert not e.owned(name)['State']['Running']
catalogs={engine:json.loads((HERE/'results'/(engine+'-selected.json')).read_text()) for engine in ['postgres','clickhouse']}
for engine,cases in catalogs.items():
 assert len(cases)==11
 for name,c in cases.items():assert c['state'] in ['complete','failed','timeout','qa_failed'],(engine,name,c['state'])
comparison={}
for name in catalogs['postgres']:
 a=catalogs['postgres'][name];b=catalogs['clickhouse'][name];matched=None
 if a.get('qa') and b.get('qa'):
  matched=a['qa']['rows']==b['qa']['rows'] and a['qa']['canonical_sha256']==b['qa']['canonical_sha256'];assert matched
 comparison[name]={'pg_state':a['state'],'ch_state':b['state'],'full_outputs_matched':matched}
dump(HERE/'results/selected-engine-comparison.json',comparison)
# The codec/schema sample is explicitly one already-downloaded source per entity,
# not a claim that every historical shard has an identical Arrow schema.
examples={}
for p in sorted((HERE/'results/download').glob('*.json')):
 x=json.loads(p.read_text());examples.setdefault(x['entity'],x)
records=[]
for entity,x in sorted(examples.items()):
 p=HERE/x['path'];f=pq.ParquetFile(p);m=f.metadata
 codecs=collections.Counter(m.row_group(i).column(j).compression for i in range(m.num_row_groups) for j in range(m.num_columns))
 records.append({'entity':entity,'source_key':x['source_key'],'version_id':x['version_id'],'rows':m.num_rows,'row_groups':m.num_row_groups,'column_chunk_codecs':dict(codecs),'arrow_schema':str(f.schema_arrow),'top_level_fields':f.schema_arrow.names})
dump(HERE/'results/raw-schema-codec-sample.json',{'scope':'One pinned already-downloaded source file per entity; sample only, not a union over all shard schemas. No raw row values are copied.','entities':records})
usage={}
for name in ['raw','projected','pgdata','chdata']:
 r=subprocess.run(['du','-sb',str(HERE/name)],capture_output=True,text=True,check=True);usage[name]=int(r.stdout.split()[0])
dump(HERE/'results/final-directory-bytes.json',{'at':time.time(),'apparent_directory_bytes':usage,'scope':'Native bind directories include their logs/WAL and filesystem metadata files; database-table sizes in prepared.json have a narrower scope. Final state, not peak temporary-space use.'})
dump(HERE/'results/experiment-settled.json',{'settled':True,'at':time.time(),'selected_states':{e:{k:v['state'] for k,v in c.items()} for e,c in catalogs.items()},'both_engines_stopped':True,'no_additional_volumes_or_tuning':True})
print(json.dumps({'states':{e:{k:v['state'] for k,v in c.items()} for e,c in catalogs.items()},'directory_bytes':usage},indent=2))
