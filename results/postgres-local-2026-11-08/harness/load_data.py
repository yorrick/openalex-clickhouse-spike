from pathlib import Path
import json,hashlib,re,time,shutil,sys,psutil,traceback
from pg_helpers import HERE,connect,duck,dump,Monitor
CACHE=Path('/Users/yorrickjansen/work/openalex/.worktrees/clickhouse-repeatability/.data')
ROOT=Path('/Users/yorrickjansen/work/openalex')
SRC=Path('/Users/yorrickjansen/work/data/openalex-tier-scaling-20261106/source-manifest.json')
manifest=json.loads(SRC.read_text());byurl={f['original_url']:f for f in manifest['files']};allfiles={}
for f in manifest['files']:allfiles.setdefault(f['entity'],[]).append(f['local_path'])
selection=json.loads((CACHE/'selection.json').read_text())
SCHEMA='''CREATE TABLE IF NOT EXISTS authors(author_id bigint,canonical_id text,display_name text,orcid text);
CREATE TABLE IF NOT EXISTS institutions(institution_id bigint,canonical_id text,display_name text,country_code text,institution_type text);
CREATE TABLE IF NOT EXISTS sources(source_id bigint,canonical_id text,display_name text,issn_l text,source_type text);
CREATE TABLE IF NOT EXISTS topics(topic_id bigint,display_name text,subfield_id bigint,field_id bigint,domain_id bigint);
CREATE TABLE IF NOT EXISTS works(work_id bigint,canonical_id text,publication_year integer,work_type text,source_id bigint,is_oa boolean,is_xpac boolean,cited_by_count bigint,primary_topic_id bigint);
CREATE TABLE IF NOT EXISTS work_author(work_id bigint,author_id bigint,author_position text,is_corresponding boolean);
CREATE TABLE IF NOT EXISTS work_institution(work_id bigint,author_id bigint,institution_id bigint);
CREATE TABLE IF NOT EXISTS work_topic(work_id bigint,topic_id bigint,score real,is_primary boolean);
CREATE TABLE IF NOT EXISTS citation_edge(citing_work_id bigint,cited_work_id bigint,citing_year integer);'''
NUM=lambda s:f"try_cast(regexp_extract({s}, '[A-Z]([0-9]+)$', 1) AS BIGINT)"
HIER=lambda s:f"try_cast(regexp_extract({s}, '/([0-9]+)$', 1) AS BIGINT)"
def lit(s):return "'"+s.replace("'","''")+"'"
def source(e,tier):
 fs=[byurl[f['url']]['local_path'] for f in selection['tiers'][tier]['files']] if e=='works' else allfiles[e]
 assert all(Path(f).exists() for f in fs),(e,'missing local cached file')
 return 'read_parquet(['+','.join(map(lit,fs))+'], union_by_name=true)'
def projection(table,tier):
 if table in ('authors','institutions','sources','topics'):
  s=source(table,tier);n=NUM('id');good=f'{n} IS NOT NULL'
  if table=='authors':return f"SELECT {n},id,display_name,nullif(orcid,'') FROM {s} WHERE {good}"
  if table=='institutions':return f"SELECT {n},id,display_name,nullif(country_code,''),type FROM {s} WHERE {good}"
  if table=='sources':return f"SELECT {n},id,display_name,nullif(issn_l,''),type FROM {s} WHERE {good}"
  h=[HIER(x+'.id') for x in ('subfield','field','domain')];return f"SELECT {n},display_name,{','.join(h)} FROM {s} WHERE {good} AND "+' AND '.join(x+' IS NOT NULL' for x in h)
 s=source('works',tier);w=NUM('w.id');year='CASE WHEN w.publication_year BETWEEN 0 AND 65535 THEN CAST(w.publication_year AS INTEGER) ELSE NULL END';valid=f'{w} IS NOT NULL'
 if table=='works':return f"SELECT {w},w.id,{year},w.type,{NUM('w.primary_location.source.id')},coalesce(w.open_access.is_oa,false),coalesce(w.is_xpac,false),CAST(w.cited_by_count AS BIGINT),{NUM('w.primary_topic.id')} FROM {s} w WHERE {valid}"
 if table in ('work_author','work_institution'):
  a=NUM('au.a.author.id');base=f'{s} w CROSS JOIN UNNEST(w.authorships) AS au(a)';good=f'{valid} AND {a} IS NOT NULL'
  if table=='work_author':return f'SELECT {w},{a},au.a.author_position,coalesce(au.a.is_corresponding,false) FROM {base} WHERE {good}'
  i=NUM('inst.i.id');return f'SELECT DISTINCT {w},{a},{i} FROM {base} CROSS JOIN UNNEST(au.a.institutions) AS inst(i) WHERE {good} AND {i} IS NOT NULL'
 if table=='work_topic':
  t=NUM('t.topic.id');primary=NUM('w.primary_topic.id');return f'SELECT {w},{t},CAST(t.topic.score AS FLOAT),coalesce({t}={primary},false) FROM {s} w CROSS JOIN UNNEST(w.topics) AS t(topic) WHERE {valid} AND {t} IS NOT NULL AND t.topic.score IS NOT NULL'
 if table=='citation_edge':
  c=NUM('ref.id');return f'SELECT {w},{c},min({year}) FROM {s} w CROSS JOIN UNNEST(w.referenced_works) AS ref(id) WHERE {valid} AND {c} IS NOT NULL GROUP BY 1,2'
 raise ValueError(table)

def main():
 tier=sys.argv[1] if len(sys.argv)>1 else 'stage2_small';tables=sys.argv[2:] or ['authors','institutions','sources','topics','works','work_author','work_institution','work_topic','citation_edge']
 with connect() as pg:pg.execute(SCHEMA)
 d=duck();(HERE/'sql/schema.sql').write_text(SCHEMA+'\n')
 for table in tables:
  log=HERE/'results'/f'load-{tier}-{table}.json'
  if log.exists() and json.loads(log.read_text()).get('state')=='complete':print(table,'already complete',flush=True);continue
  if shutil.disk_usage(HERE).free < 80*(1<<30):raise RuntimeError('Host free disk below80GiB guard')
  sql='INSERT INTO pg.public.'+table+' '+projection(table,tier)
  (HERE/'sql'/f'load-{tier}-{table}.sql').write_text(sql+';\n')
  with connect() as pg:
   n=pg.execute(f'SELECT count(*) FROM {table}').fetchone()[0]
   if n:raise RuntimeError(f'Nonempty target {table}: manual explicit reset needed, not silently appending')
  print('Loading',table,flush=True);m=Monitor().start();st=time.monotonic();host_before=psutil.disk_io_counters()._asdict();proof={'table':table,'tier':tier,'state':'running','start':time.time(),'sql_sha256':hashlib.sha256(sql.encode()).hexdigest()};dump(log,proof)
  try:
   d.execute(sql)
   elapsed=time.monotonic()-st
   with connect() as pg:
    rows=pg.execute(f'SELECT count(*) FROM {table}').fetchone()[0];size=pg.execute('SELECT pg_relation_size(%s)',[table]).fetchone()[0]
   samples=m.stop();dump(HERE/'results'/f'load-{tier}-{table}-telemetry.json',samples)
   proof.update(state='complete',seconds=elapsed,rows=rows,heap_bytes=size,host_disk_before=host_before,host_disk_after=psutil.disk_io_counters()._asdict(),host_free_after=shutil.disk_usage(HERE).free,telemetry_samples=len(samples));dump(log,proof);print(table,rows,round(elapsed,3),'seconds',round(size/1e9,3),'GB heap',flush=True)
  except BaseException as e:
   samples=m.stop();dump(HERE/'results'/f'load-{tier}-{table}-telemetry.json',samples);pw=(HERE/'secrets/password').read_text();proof.update(state='failed',error=(type(e).__name__+': '+str(e)).replace(pw,'[REDACTED]'),seconds=time.monotonic()-st);dump(log,proof);print(proof['error'],flush=True);raise SystemExit(1)
 d.close()
if __name__=='__main__':main()
