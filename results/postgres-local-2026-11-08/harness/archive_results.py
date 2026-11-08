from pathlib import Path
import json,gzip,hashlib,shutil,statistics,subprocess,datetime,os
from pg_helpers import HERE,dump,connect
from index_and_benchmark import ROOT
WT=ROOT/'.claude/worktrees/postgres-local-benchmark';OUT=WT/'results/postgres-local-2026-11-08';OUT.mkdir(parents=True,exist_ok=True)
for name in ('experiment-plan.json','container.json','requirements.lock'):
 shutil.copyfile(HERE/name,OUT/name)
for name in ('settings.json','database-initial.json','small-table-count-qa.json','medium-table-count-qa.json','load-summary-small.json','q03-rewrite-hypothesis.json','q03-medium-rewrite-protocol.json'):
 p=HERE/'results'/name
 if p.exists():shutil.copyfile(p,OUT/name)
case_data={};telemetry={};load={};indexes={};updates={}
for tier in ('stage2_small','stage2_medium'):
 case_data[tier]={};indexes[tier]={}
 for p in sorted((HERE/'results'/tier).glob('*.json')):
  if '-canonical' in p.name:continue
  obj=json.loads(p.read_text())
  if '-telemetry' in p.name:telemetry[tier+'/'+p.name]=obj
  elif p.name.startswith('q'):case_data[tier][p.name]=obj
  else:indexes[tier][p.name]=obj
for p in (HERE/'results').glob('load-*.json'):
 if '-telemetry' in p.name:telemetry[p.name]=json.loads(p.read_text())
 else:load[p.name]=json.loads(p.read_text())
for p in (HERE/'results/update-probes').glob('*.json'):
 if '-telemetry' in p.name:telemetry['update-probes/'+p.name]=json.loads(p.read_text())
 else:updates[p.name]=json.loads(p.read_text())
for name,obj in [('cases.json.gz',case_data),('telemetry.json.gz',telemetry),('indexing-and-storage.json.gz',indexes),('loading.json.gz',load),('update-probes.json.gz',updates)]:
 with gzip.open(OUT/name,'wt',encoding='utf-8') as f:json.dump(obj,f,separators=(',',':'),default=str)
(OUT/'harness').mkdir(exist_ok=True)
for f in ('pg_helpers.py','init_local.py','load_data.py','index_and_benchmark.py','variant_bench.py','update_probe.py','scale_to.py','write_report.py','archive_results.py'):
 shutil.copyfile(HERE/f,OUT/'harness'/f)
(OUT/'sql').mkdir(exist_ok=True)
for f in (HERE/'sql').glob('*.sql'):shutil.copyfile(f,OUT/'sql'/f.name)
qa=[]
for tier,files in case_data.items():
 for name,obj in files.items():
  if obj.get('qa'):
   assert obj['state']=='complete' and obj['qa']['matched'],(tier,name)
   qa.append({'tier':tier,'case_file':name,**obj['qa']})
assert len(qa)==25,len(qa)
dump(OUT/'qa.json',{'full_result_hash_comparisons':qa,'all_25_match':True,'baseline_cases':22,'extra_variant_or_control_exports':3,'oracle':'Existing frozen typed ClickHouse/Athena multiset SHA256 androwcounts fromNov6; integer/bool/string normalization reused unchanged','table_counts':'AllnineactualPGtablecounts equal correspondingCHcohort before/afterupdateprobesandat10m'})
with connect() as pg:
 disk={'database_bytes':pg.execute('SELECT pg_database_size(current_database())').fetchone()[0],'wal_files_bytes':pg.execute('SELECT sum(size) FROM pg_ls_waldir()').fetchone()[0],'host_free_bytes':shutil.disk_usage(HERE).free,'time':datetime.datetime.now(datetime.timezone.utc).isoformat()}
dump(OUT/'final-disk.json',disk)
proof={'date':'2026-11-08','scope':'PostgreSQL localstartercomparison,2m/10mWorks withall119mAuthorrowsandidenticalselectedfields. No31.9mPGorfullcorpustest.','user_no_claude_validation':True,'validation':'ActualstockPGexecutions,3warmrepeatsafterprimer,25typedfull-outputhashmatches,all9tablecountsmatchbothcohorts. NoexternalAIreviewofPostgresinvoked.','commands':['.venv/bin/python init_local.py','.venv/bin/python load_data.py stage2_small','.venv/bin/python index_and_benchmark.py stage2_small queries','.venv/bin/python variant_bench.py stage2_small q03_preaggregate_authors q03 sql/q03_preaggregate_authors.sql','.venv/bin/python update_probe.py','.venv/bin/python scale_to.py stage2_medium','.venv/bin/python load_data.py stage2_medium works work_author work_institution work_topic citation_edge','.venv/bin/python index_and_benchmark.py stage2_medium all --bracket-q03','.venv/bin/python write_report.py','.venv/bin/python archive_results.py'],'initial_harness_corrections':['FirstrawParquetprobeusedURLidintoBIGINTandfailed,correctedtomatchingnumericIDregexbeforefullbulkload;2rowfixtureSQLParquetcopythenwitnessed.','FirstqueryrunnerusedCHcount()syntaxandfailedbeforeanysuccessfultimedquery;adaptedtocount(*). Exceptionhandlerimportpsycopgwasaddedtoavoidmaskingthaterror. No datachangedbytheseerrors,initiallogsretainedinlocalstudy.','Cloudtimingsincludeprimer;artifactpayloadbuilderexcludesprimerexplicitly. Postgresrunnerseparatelylabelsprimer/warm1/2/3.'],'resource_scope':'CgroupCPUoverinstrumentedclientwindow,backgroundPGincluded. Containerfileincludesshmem,donotadd. SharedReadBlocks are PGbuffermisses,notphysicaldisk. HostIOcountershost-wideunisolated;VirtioFScanbypasscgroupblockaccounting. Loadtelemetryincludespostloadvalidationwhilecopysecondsdo not.','update_scope':'SyntheticstagedapplyandreplayinsideoneoutertransactionthenROLLBACK;NOcommitorstagingtime. Notactualnewsnapshotsync,notproductionthroughput. Noformalhours/financialtotalsclaimed.','storage':'HostbindmountPGDATAoutsideDockerVMdue8GBVMfree;hostinitial411GiB. Data/secretpasswordexcludedfromgit;PGimageonimmutablearchiveddigest.','study':str(HERE),'issue':'https://linear.app/yorrick/issue/YOR-68/comparer-postgresql-local-a-clickhouse-et-athena-sur-openalex'}
dump(OUT/'provenance.json',proof)
(OUT/'README.md').write_text('# PostgreSQL local benchmark evidence\n\nThe [report](../../docs/postgres-local-benchmark.md) describes the methods and limits. `summary.json` holds baseline family/case summaries; `cases.json.gz` contains all plans, settings, SQL, timings, resources and QA for the measured cases, including the q03 rewrite and original-SQL control. `telemetry.json.gz` holds the complete cgroup traces. Loading, indexing/storage and synthetic update probes are archived separately.\n\nThe harness expects the historical cached files and local study directory recorded in provenance, not a public reproducible service. Credentials, PGDATA, intermediate temp files, and large canonical-result exports stay in the local study. No benchmark is added to CI. No Claude Code validation was requested or performed for PostgreSQL.\n')
print('Archived',len(qa),'matchedoutputs; gzipproofs andharness;noPGDATAorpassword')
