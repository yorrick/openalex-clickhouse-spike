"""Small independent PyArrow/Python value audit, separate from DuckDB ETL and SQL timing."""
from pathlib import Path
from collections import Counter
import json,hashlib,random,struct,time
import pyarrow.parquet as pq
from helpers import HERE,duck,dump
M=json.loads((HERE/'input-manifest.json').read_text());T=json.loads((HERE/'projection-templates.json').read_text())
def num(x):
 if x is None:return None
 tail=x.rsplit('/',1)[-1]
 return int(tail[1:]) if len(tail)>1 and tail[0].isupper() and tail[1:].isdigit() else None
def hier(x):
 if not x:return None
 tail=x.rsplit('/',1)[-1];return int(tail) if tail.isdigit() else None
def fp32(x):return struct.unpack('f',struct.pack('f',float(x)))[0]
def yr(x):return x if x is not None and 0<=x<=65535 else None
def nullif(x):return None if x=='' else x
def get(x,*keys):
 for k in keys:
  if x is None:return None
  x=x.get(k)
 return x

def expected(entity,rows):
 out={t:[] for t in (['works','work_author','work_institution','work_topic','citation_edge'] if entity=='works' else [entity])}
 for r in rows:
  ident=num(r['id'])
  if ident is None:continue
  if entity=='authors':out[entity].append((ident,r['id'],r['display_name'],nullif(r['orcid'])))
  elif entity=='institutions':out[entity].append((ident,r['id'],r['display_name'],nullif(r['country_code']),r['type']))
  elif entity=='sources':out[entity].append((ident,r['id'],r['display_name'],nullif(r['issn_l']),r['type']))
  elif entity=='topics':
   hs=[hier(get(r,k,'id')) for k in ['subfield','field','domain']]
   if all(x is not None for x in hs):out[entity].append((ident,r['display_name'],*hs))
  else:
   y=yr(r['publication_year']);primary=num(get(r,'primary_topic','id'))
   out['works'].append((ident,r['id'],y,r['type'],num(get(r,'primary_location','source','id')),get(r,'open_access','is_oa') or False,r.get('is_xpac') or False,r['cited_by_count'],primary))
   wi=set()
   for a in r['authorships'] or []:
    author=num(get(a,'author','id'))
    if author is None:continue
    out['work_author'].append((ident,author,a['author_position'],a.get('is_corresponding') or False))
    for ins in a.get('institutions') or []:
     i=num(ins.get('id'))
     if i is not None:wi.add((ident,author,i))
   out['work_institution'].extend(wi)
   for t in r['topics'] or []:
    i=num(t['id'])
    if i is not None and t.get('score') is not None:out['work_topic'].append((ident,i,fp32(t['score']),i==primary if primary is not None else False))
   out['citation_edge'].extend((ident,cited,y) for cited in {num(x) for x in (r['referenced_works'] or [])} if cited is not None)
 return out

def main():
 st=time.monotonic();random.seed(200);works=[f for f in M['inputs'] if f['entity']=='works'];newkeys={f['source_key'] for f in M['files'][480:]};new=[f for f in works if f['source_key'] in newkeys]
 selected=random.sample(new,12)+random.sample([f for f in works if f['source_key'] not in newkeys],8)
 for e in ['authors','institutions','sources','topics']:
  fs=[f for f in M['inputs'] if f['entity']==e and f['rows']>0];selected+=random.sample(fs,min(4,len(fs)))
 d=duck('4GB');checks=[];sample_counts=Counter()
 for f in selected:
  tag=hashlib.sha256(f['source_key'].encode()).hexdigest();raw=HERE/'raw'/f['entity']/(tag+'.parquet');batch=next(pq.ParquetFile(raw).iter_batches(batch_size=128));rows=batch.to_pylist();sample_counts[f['entity']]+=len(rows)
  ref=expected(f['entity'],rows);ids=[num(r['id']) for r in rows if num(r['id']) is not None]
  for t,want in ref.items():
   keycol='citing_work_id' if t=='citation_edge' else 'work_id' if f['entity']=='works' else T['columns'][t][0]
   actual=d.execute(f"SELECT * FROM read_parquet('{HERE}/projected/{t}/{tag}.parquet') WHERE {keycol} IN (SELECT unnest(?))",[ids]).fetchall()
   assert Counter(actual)==Counter(want),(t,f['source_key'],len(actual),len(want))
   checks.append({'table':t,'source_key':f['source_key'],'sample_source_rows':len(rows),'retained_rows':len(want),'exact_typed_multiset_match':True})
 d.close();dump(HERE/'results/normalization-sample-qa.json',{'passed':True,'method':'Independent PyArrow reader and Python scalar/list normalization vs actual retained Parquet; duplicate-aware Counter equality','sample_source_rows':dict(sample_counts),'files':len(selected),'checks':checks,'seconds':time.monotonic()-st,'scope':'Sample audit, not independent row-by-row audit of entire corpus; raw Athena full-result QA covers benchmark outputs'})
 print('INDEPENDENT NORMALIZATION SAMPLE PASS',dict(sample_counts),flush=True)
if __name__=='__main__':main()
