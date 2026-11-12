from pathlib import Path
import shutil,json,subprocess,sys
HERE=Path(__file__).resolve().parent
P=HERE/'smoke';P.mkdir(exist_ok=True)
for name in ['helpers.py','run_engines.py','tier_sql.py','projection-templates.json']:
 shutil.copy2(HERE/name,P/name)
f=P/'run_engines.py';f.write_text(f.read_text().replace("PG='oa200-pg';CH='oa200-ch'","PG='oa200-pg-smoke';CH='oa200-ch-smoke'"))
shutil.copytree(HERE/'sql',P/'sql',dirs_exist_ok=True);(P/'results').mkdir(exist_ok=True);(P/'temp').mkdir(exist_ok=True);(P/'duckdbhome').mkdir(exist_ok=True)
# Both runs use the same tiny fixture. This tests the harness, not OpenAlex performance.
import duckdb
T=json.loads((P/'projection-templates.json').read_text());d=duckdb.connect();d.execute(T['pg_schema'].replace('text','VARCHAR').replace('real','FLOAT'))
fixture={
'works':[(51557542,'https://openalex.org/W51557542',2020,'article',1,True,False,10,1),(24222542,'https://openalex.org/W24222542',2021,'article',1,False,False,5,2),(2003585639,'https://openalex.org/W2003585639',2020,'book',1,False,False,0,1)],
'authors':[(1,'https://openalex.org/A1','One',None),(2,'https://openalex.org/A2','Two','https://orcid.org/0000-0000-0000-0000')],
'institutions':[(1,'https://openalex.org/I1','Canada','CA','education'),(2,'https://openalex.org/I2','USA','US','education')],
'sources':[(1,'https://openalex.org/S1','Journal','1234-5678','journal')],
 'topics':[(1,'Climate',11,1,1),(2,'Medicine',22,2,2)],
'work_author':[(51557542,1,'first',True),(51557542,2,'last',False),(24222542,1,'first',True),(2003585639,2,'first',False)],
'work_institution':[(51557542,1,1),(51557542,2,2),(24222542,1,1),(2003585639,2,2)],
'work_topic':[(51557542,1,.75,True),(24222542,2,.9,True),(2003585639,1,.8,True)],
'citation_edge':[(51557542,24222542,2020),(24222542,2003585639,2021),(2003585639,51557542,2020)]}
for t,rows in fixture.items():
 d.executemany('INSERT INTO '+t+' VALUES ('+','.join('?' for _ in rows[0])+')',rows);folder=P/'projected'/t;folder.mkdir(parents=True,exist_ok=True);
 if not (folder/'fixture.parquet').exists():d.execute(f"COPY {t} TO '{folder}/fixture.parquet' (FORMAT PARQUET)")
 else:assert d.execute(f"SELECT count(*) FROM read_parquet('{folder}/fixture.parquet')").fetchone()[0]==len(rows)
# Same signed extensions installed by bootstrap, not downloaded during timings.
shutil.copytree(HERE/'duckdbhome',P/'duckdbhome',dirs_exist_ok=True)
(P/'results/projection-complete.json').write_text(json.dumps({'counts':{t:len(v) for t,v in fixture.items()}}))
r=subprocess.run([sys.executable,str(P/'run_engines.py')],cwd=P)
if r.returncode:raise SystemExit(r.returncode)
x=json.loads((P/'results/engine-comparison.json').read_text());assert len(x)==11 and all(v['matched'] is True for v in x.values()),x
for name in ['oa200-pg-smoke','oa200-ch-smoke']:subprocess.run(['docker','rm',name],check=True)
(HERE/'results/smoke-pass.json').write_text(json.dumps({'all11_full_results_match':True,'cases':x,'fixture_only':True},indent=2))
print('SMOKE PASS: 11 full typed result comparisons',flush=True)
