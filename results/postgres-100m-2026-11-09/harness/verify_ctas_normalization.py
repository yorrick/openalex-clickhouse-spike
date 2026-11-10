"""Compare newAthenaCTAS payloads toindependentDuckDB normalizer on2realrawfiles."""
from pathlib import Path
import json,time,hashlib
import duckdb
from pg_helpers import HERE,dump
import load_data as original
from load_streaming import projection
from project_inputs import COLUMNS

def main():
 m=json.loads((HERE/'works-input-manifest.json').read_text());fs=[f for f in m['files'] if not f['read_uri'].startswith('http')][:2];assert len(fs)==2
 source='read_parquet(['+','.join(original.lit(f['read_uri']) for f in fs)+'],union_by_name=true)'
 d=duckdb.connect();d.execute("SET memory_limit='2GB'");d.execute('SET threads=2');folder=HERE/'temp/sample-normalization';folder.mkdir(exist_ok=True);d.execute('SET temp_directory=?',[str(folder)])
 d.execute('CREATE TEMP TABLE ids AS SELECT '+original.NUM('id')+' AS work_id FROM '+source);n=d.execute('SELECT count(*) FROM ids').fetchone()[0];assert n==sum(f['record_count'] for f in fs)
 records=[]
 for table in ['works','work_author','work_institution','work_topic','citation_edge']:
  if table=='works':body=original.projection(table,'stage2_large');old=original.source('works','stage2_large');assert body.count(old)==1;body=body.replace(old,source)
  else:body=projection(table,'sample',source)
  d.execute('CREATE TEMP TABLE e AS SELECT * FROM ('+body+') AS normalized('+','.join(COLUMNS[table])+')')
  key='citing_work_id' if table=='citation_edge' else 'work_id'
  d.execute('CREATE TEMP TABLE a AS SELECT a.* FROM read_parquet(?) a SEMI JOIN ids ON a.'+key+'=ids.work_id',[str(HERE/'projected'/(table+'.parquet'))])
  expected=d.execute('SELECT count(*) FROM e').fetchone()[0];actual=d.execute('SELECT count(*) FROM a').fetchone()[0]
  diff=d.execute('SELECT count(*) FROM ((SELECT * FROM e EXCEPT ALL SELECT * FROM a) UNION ALL (SELECT * FROM a EXCEPT ALL SELECT * FROM e))').fetchone()[0]
  assert expected==actual and diff==0,(table,expected,actual,diff)
  records.append({'table':table,'expected_rows':expected,'actual_rows':actual,'full_symmetric_except_all_rows':diff,'expected_sql_sha256':hashlib.sha256(body.encode()).hexdigest()});d.execute('DROP TABLE e');d.execute('DROP TABLE a');print(table,'sample exactmultisetMATCH',expected,flush=True)
 dump(HERE/'results/ctas-independent-normalization-qa.json',{'pass':True,'scope':'Exactfullmultisetcomparisonofall23Work-derivedretainedcolumnson2realpriorrawfilesversuscorrespondingrowsin100mAthenaCTASpayloads;notafull100mtransformationaudit','sample_works':n,'sources':[{k:f.get(k) for k in ['source_key','version_id','known_full_sha256','record_count']} for f in fs],'tables':records})
 d.close()
if __name__=='__main__':main()
