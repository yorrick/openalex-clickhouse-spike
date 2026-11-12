from pathlib import Path
import sys,json,shutil
HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'openalex-postgres-100m-20261109'
sys.path.insert(0,str(OLD));import load_data,load_streaming,project_inputs,benchmark_helpers
columns=project_inputs.COLUMNS
sqls={}
for t,cs in columns.items():
 if t in ['work_author','work_institution','work_topic','citation_edge']:body=load_streaming.projection(t,'stage2_large',"read_parquet('__INPUT__')")
 else:body=load_data.projection(t,'stage2_large').replace(load_data.source('works' if t=='works' else t,'stage2_large'),"read_parquet('__INPUT__')")
 sqls[t]='SELECT * FROM ('+body+') normalized('+','.join(cs)+')'
(HERE/'projection-templates.json').write_text(json.dumps({'columns':columns,'sql':sqls,'pg_schema':load_data.SCHEMA,'indexes':benchmark_helpers.INDEXES},indent=2)+'\n')
# Reuse the selected exact SQL, not a newly inferred equivalent.
for f in OLD.glob('sql/q*-postgres.sql'):shutil.copy2(f,HERE/'sql'/f.name)
