from pathlib import Path
import json,gzip,hashlib,statistics,re,datetime
HERE=Path(__file__).resolve().parent
REPO=Path('/Users/yorrickjansen/work/openalex/.claude/worktrees/benchmark-artifact-200m');R=REPO/'results'
S200=Path('/Users/yorrickjansen/work/data/openalex-ec2-200m-20261112');C200=S200/'cloud-results'
def load(p):
 p=Path(p);return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_text())
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def compact_plan(n):
 if isinstance(n,list):return [compact_plan(x) for x in n]
 if not isinstance(n,dict):return n
 keep=['Node Type','Join Type','Relation Name','Index Name','Plan Rows','Actual Rows','Actual Loops','Workers Planned','Workers Launched','Group Key','Sort Key','Presorted Key','Sort Method','Peak Memory Usage','Disk Usage','Temp Read Blocks','Temp Written Blocks','Shared Read Blocks','Shared Hit Blocks','Hash Batches','Original Hash Batches']
 out={k:n[k] for k in keep if k in n}
 if 'Plans' in n:out['Plans']=[compact_plan(x) for x in n['Plans']]
 return out
legacy=load(R/'aws-scaling-2026-11-06/technical-payload.json')
baseurl='https://github.com/yorrick/openalex-clickhouse-spike/blob/964897d49da1402af231a15a2d99d0229508bfc5/'
def link(path):return baseurl+str(path)
P={'built_date':'2026-11-13','artifact_url':'https://claude.ai/artifact/12VD4Wi6EzKtA2mdABXp6H','units':{'GB':1000000000,'GiB':1073741824},'cohorts':{},'setups':{},'records':[],'legacy_tuning':legacy['tuning'],'legacy_source':legacy['source_links'],'field_inventory':legacy['field_inventory'],'historical_full_snapshot':legacy['full_snapshot'],'schemas':{'legacy_clickhouse':legacy['loaded_schema_sql']},'sources':[]}
P['setups']={
 'ec2_legacy':{'label':'EC2, original 2m/10m/32m series','host':'Ubuntu EC2 m7g.8xlarge, 32 vCPU / 128 GiB host RAM','container_cpus':18,'container_memory_gib':50,'scratch':'400 GiB gp3; 3000 IOPS, 500 MiB/s','raw':'120 GiB gp3; 3000 IOPS, 125 MiB/s; read-only during benchmark','note':'Different resource budget and older ClickHouse image/settings from 100m/200m; no isolated growth law.'},
 'local_pg':{'label':'Local PostgreSQL','host':'Apple M5 Max, 18 cores / 128 GiB host RAM','container_cpus':16,'container_memory_gib':32,'disk':'Docker VM bind/VirtioFS; dedicated SSD I/O ceiling not measured','default_settings':load(R/'postgres-local-2026-11-08/settings.json'),'note':'Container cache accounting excludes some macOS host cache. Local physical I/O is not equivalent to native Linux block I/O.'},
 'local_100':{'label':'Local 100m paired run','host':'Apple M5 Max, 18 cores / 128 GiB host RAM','container_cpus':16,'container_memory_gib':32,'disk':'Docker VM / VirtioFS; no dedicated disk bandwidth or IOPS floor','note':'Sequential PostgreSQL and ClickHouse. PostgreSQL only 12 indexes; citation indexes stopped by disk guard. q05/q06/q07 not run in PostgreSQL.'},
 'local_ch_history':{'label':'Historical local ClickHouse','host':'Local laptop; historical setup differs from later paired runs','container_cpus':None,'container_memory_gib':None,'note':'Historical median-only rows from the archived overview. Exact per-case local SQL and repeats are not supplied in this evidence bundle; do not substitute EC2 SQL.'},
 'ec2_200':{'label':'Paired EC2 200m run, 12 November 2026','host':'Ubuntu 24.04 ARM; m7g.4xlarge; 16 Graviton cores / 64 GiB host RAM','region':'us-east-1','account':'certification','container_cpus':16,'container_memory_gib':32,'swap':'disabled','scratch':'1024 GiB encrypted gp3; 6000 IOPS, 500 MiB/s; 32 GiB root','pg':'PostgreSQL 18.6; 8 GiB shared buffers; 8 parallel workers per Gather, 16 global; full 14 indexes; durability on','ch':'ClickHouse 26.3.12.3; 16 query threads; 24 GiB query memory; reverse citation projection','note':'Engines ran sequentially. Allocated resources are matched, selected internal algorithms and worker settings differ.'},
 'athena':{'label':'Raw Parquet Athena','host':'Managed Athena, us-east-1','container_cpus':None,'container_memory_gib':None,'note':'CPU/RAM not exposed. Service total includes queue, planning and result output; repeats use no result reuse. Raw normalization views, not an optimized flattened CTAS layout.'}}
cohortmap={'stage2_small':'2m','stage2_medium':'10m','stage2_large':'32m'}
for old,cid in cohortmap.items():
 t=legacy['tiers'][old];P['cohorts'][cid]={'id':cid,'label':{'2m':'2.00m','10m':'10.11m','32m':'31.89m'}[cid],'works':t['works'],'raw_bytes':t['selected_raw_bytes'],'columns':42,'seeds':list(map(str,t['seeds'])),'date':('EC2 2026-11-06; PostgreSQL local 2026-11-09; historical local CH' if cid=='32m' else 'EC2 2026-11-06; PostgreSQL local 2026-11-08; historical local CH'),'ch_active_bytes':t['normalized_bytes'],'table_storage':t['table_bytes'],'legacy_athena_views':t['athena_views'],'note':'Nested nonrandom historical June cohort; complete fixed author/institution/source/topic dimensions.'}
sum100=load(R/'postgres-100m-2026-11-09/summary.json');P['cohorts']['100m']={'id':'100m','label':'100.09m','works':sum100['works'],'raw_bytes':sum(x['bytes'] for x in load(R/'postgres-100m-2026-11-09/remote-inputs.json.gz')['files']),'columns':42,'seeds':['51557542','24222542','2003585639'],'date':'2026-11-09','table_counts':sum100['table_counts'],'note':'Local paired native engines; independent raw Athena. PostgreSQL graph/citation families not run because citation-index construction hit the host disk guard.'}
counts200=load(C200/'projection-complete.json');P['cohorts']['200m']={'id':'200m','label':'200.31m','works':200313862,'raw_bytes':341270321934,'raw_work_bytes':288201704857,'columns':42,'date':'2026-11-12','seeds':['51557542','24222542','2003585639'],'table_counts':counts200['counts'],'normalized_bytes':sum(x['bytes'] for x in counts200['tables'].values()),'core_works':127375852,'xpac_works':72938010,'note':'955 Work objects, all 480 prior 100m files preserved; 39.25% of historical 510,372,821-Work June snapshot. Wider final fields/entities not yet validated.'}
GIB=2**30
resource_keys=['window_seconds','cpu_seconds','average_busy_cores','average_busy_cores_in_monitor_window','average_cpu_cores','memory_current_peak_bytes','memory_anon_peak_bytes','memory_file_peak_bytes','memory_shmem_peak_bytes','container_sampled_peak_bytes','container_sampled_peak_anon_bytes','container_sampled_peak_file_bytes','query_peak_bytes','io_delta','average_io_mib_s','physical_read_bytes','physical_write_bytes','physical_iops','physical_await_ms','physical_read_bytes_s','physical_write_bytes_s','io_stall_fraction','external_join_compressed_bytes','external_aggregation_compressed_bytes','spill_compressed_bytes','telemetry_sample_count','telemetry_max_gap_seconds','memory_events_delta','scope']
def res(r):return {k:r[k] for k in resource_keys if k in r}
def record(c,cid,engine_key,setup,selected,source):
 name=c['name'] if 'name' in c else c['variant']
 family=name[:3]
 if family in ['q05','q06']:
  match=re.fullmatch(r'(q0[56])-s([0-9]+)',name)
  assert match,('Unsupported graph profile identity; preserve the seed separately',source,name)
  logical=name
 else:logical=family
 sql=c.get('sql');h=c.get('sql_sha256')
 if sql is not None:
  assert h in [None,sha(sql)],(source,name);h=sha(sql)
 settings={'requested':c.get('requested_settings',{}),'effective':c.get('effective_settings',{})}
 runs=[]
 for i,r in enumerate(c.get('runs',[])):
  ql=r.get('query_log') or {};sec=r.get('execution_seconds',ql.get('seconds'))
  z={'kind':r['kind'],'seconds':sec,'query_id':r.get('query_id'),'resources':res(r.get('resources',{}))}
  if ql:z.update(query_peak_memory_bytes=ql.get('peak_memory_bytes'),exception_code=ql.get('exception_code'),read_rows=ql.get('read_rows'),logical_read_bytes=ql.get('read_bytes'),profile_events={k:v for k,v in ql.get('ProfileEvents',{}).items() if any(t in k.lower() for t in ['cpu','spill','external','elapsed','readbytes','writebytes'])},effective_settings=ql.get('Settings',{}))
  if r.get('plan'):
   pl=r['plan'];z['plan']=compact_plan(pl.get('Plan',{}));z['planning_seconds']=r.get('planning_seconds');z['explain_settings']=pl.get('Settings',{})
  if r.get('error'):z['error']=r['error']
  runs.append(z)
 state=c.get('state','unknown');median=c.get('median_seconds') if state=='complete' else None
 if state=='complete':assert len(c.get('warm_seconds',[]))==3 and abs(statistics.median(c['warm_seconds'])-median)<1e-8,(source,name)
 label=c.get('label',name);pid=label+'-'+sha(json.dumps([sql,settings],sort_keys=True))[:8]
 obj={'cohort':cid,'engine_key':engine_key,'setup':setup,'family':name[:3],'case_key':logical,'seed':logical.split('-s')[1] if '-s' in logical else None,'label':label,'profile_id':pid,'selected':selected,'state':state,'median_seconds':median,'sql':sql,'sql_sha256':h,'sql_status':'exact_executed' if sql and state not in ['not_run','not_measured'] else 'not_executed' if sql else 'not_recorded','settings':settings,'runs':runs,'qa':c.get('qa'),'failure_resources':res(c.get('resources',{})),'error':c.get('error') or c.get('reason'),'source':source}
 for existing in P['records']:
  if all(existing[k]==obj[k] for k in ['cohort','engine_key','case_key','profile_id']):
   assert {k:v for k,v in existing.items() if k not in ['selected','source']}=={k:v for k,v in obj.items() if k not in ['selected','source']},('Same profile identity has distinct evidence; assign a separate series identity',source,name)
   existing['selected']|=selected;return
 P['records'].append(obj)
# Legacy paired EC2/Athena, exact archived SQL; keep historical local timing-only cells separate.
for old,cid in cohortmap.items():
 t=legacy['tiers'][old]
 for name,c in t['cases'].items():
  cr={'name':name,'sql':c['clickhouse_sql'],'sql_sha256':c['clickhouse_sql_sha256'],'state':'complete','requested_settings':t['settings'],'runs':[{'kind':'warm'+str(i+1),'query_log':{'seconds':s},'query_id':c['clickhouse_query_ids'][i],'resources':c['clickhouse_resources'][i]} for i,s in enumerate(c['clickhouse_seconds'])],'warm_seconds':c['clickhouse_seconds'],'median_seconds':c['clickhouse_median_seconds'],'qa':{'matched':c['matched'],'rows':c['result_rows'],'canonical_sha256':c['canonical_sha256']}}
  if c.get('cold_seconds') is not None:cr['runs'].insert(0,{'kind':'separate_cold_observation_as_archived','query_log':{'seconds':c['cold_seconds']},'resources':c.get('cold_resources') or {}})
  record(cr,cid,'clickhouse_ec2','ec2_legacy',True,link('results/aws-scaling-2026-11-06/technical-payload.json'))
  ar={'cohort':cid,'engine_key':'athena','setup':'athena','family':name[:3],'case_key':name,'seed':name.split('-s')[1] if '-s' in name else None,'label':name,'profile_id':name,'selected':True,'state':'complete','median_seconds':c['athena_median_seconds'],'sql':c['athena_sql'],'sql_sha256':c['athena_sql_sha256'],'sql_status':'exact_executed','settings':{'reuse':False},'runs':[dict(r,kind='warm'+str(i+1),seconds=r['total_seconds']) for i,r in enumerate(c['athena_runs'])],'qa':{'matched':c['matched'],'rows':c['result_rows'],'canonical_sha256':c['canonical_sha256']},'source':link('results/aws-scaling-2026-11-06/technical-payload.json')};assert sha(ar['sql'])==ar['sql_sha256'];P['records'].append(ar)
 ov=next(v for v in legacy['benchmark']['tiers'] if v['works']==t['works'])
 for fam,x in ov['queries'].items():P['records'].append({'cohort':cid,'engine_key':'clickhouse_local','setup':'local_ch_history','family':fam,'case_key':fam,'seed':None,'label':'Historical local overview','profile_id':'historical','selected':True,'state':'historical','median_seconds':x['local_s'],'sql':None,'sql_sha256':None,'sql_status':'not_recorded','settings':{},'runs':[],'qa':None,'source':legacy['source_links']['report'],'note':'Timing-only historical overview. Exact local SQL and per-seed repeats were not archived in this payload. Do not substitute the EC2 SQL.'})
# PostgreSQL 2m/10m raw profiles. Baseline remains default, rewrites visible in tuning selector.
local=load(R/'postgres-local-2026-11-08/cases.json.gz')
for old,items in local.items():
 cid=cohortmap[old]
 for filename,c in items.items():
  if not isinstance(c,dict) or 'state' not in c or 'sql' not in c:continue
  label=c.get('name',filename.removesuffix('.json'));selected='name' in c
  record(c,cid,'postgres_local','local_pg',selected,link('results/postgres-local-2026-11-08/cases.json.gz'))
# PostgreSQL 32m selected labels from the recorded bounded tuning decision.
s32=load(R/'postgres-scaling-2026-11-09/scaling-decision.json')['selected_best_observed_cases'];cases32=load(R/'postgres-scaling-2026-11-09/cases.json.gz')
for label,c in cases32.items():
 logical=label[:3]+('-s'+label.split('-s',1)[1] if '-s' in label else '')
 if logical[:3] not in ['q05','q06']:logical=logical[:3]
 record(c,'32m','postgres_local','local_pg',s32.get(logical,{}).get('label')==label,link('results/postgres-scaling-2026-11-09/cases.json.gz'))
# 100m paired local profiles and independent Athena SQL.
for file,engine,selected in [('postgres-cases.json.gz','postgres_local',True),('postgres-baseline-aggregates.json.gz','postgres_local',False),('postgres-targeted-trials.json.gz','postgres_local',False),('clickhouse-cases.json.gz','clickhouse_local',True),('clickhouse-initial24-cases.json.gz','clickhouse_local',False)]:
 for name,c in load(R/'postgres-100m-2026-11-09'/file).items():record(dict(c,name=c.get('name',name)),'100m',engine,'local_100',selected,link('results/postgres-100m-2026-11-09/'+file))
for cid,where,cases,ledger in [('100m',R/'postgres-100m-2026-11-09',load(R/'postgres-100m-2026-11-09/athena-cases.json.gz'),load(R/'postgres-100m-2026-11-09/athena-statements.json.gz')),('200m',S200,load(S200/'athena-cases.json'),load(S200/'results/athena-full-query-receipts.json'))]:
 lookup={x.get('QueryExecutionId',x.get('id')):x for x in ledger};views=[]
 for item in ledger:
  sql=item.get('Query',item.get('sql',''))
  if sql.lstrip().upper().startswith(('CREATE VIEW','CREATE EXTERNAL TABLE')):views.append({'sql':sql,'sha256':sha(sql)})
 P['cohorts'][cid]['athena_views']=views
 for name,c in cases.items():
  sqls=[lookup[x['query_id']].get('Query',lookup[x['query_id']].get('sql')) for x in c['runs']];assert len(set(sqls))==1
  sql=sqls[0];runs=[dict(x,kind='warm'+str(i+1),seconds=x['statistics']['TotalExecutionTimeInMillis']/1000,data_scanned_bytes=x['statistics']['DataScannedInBytes']) for i,x in enumerate(c['runs'])]
  P['records'].append({'cohort':cid,'engine_key':'athena','setup':'athena','family':name[:3],'case_key':name,'seed':name.split('-s')[1] if '-s' in name else None,'label':name,'profile_id':name,'selected':True,'state':'complete','median_seconds':statistics.median(x['seconds'] for x in runs),'sql':sql,'sql_sha256':sha(sql),'sql_status':'exact_executed','settings':{'reuse':False},'runs':runs,'qa':c.get('reference') or {'rows':runs[0]['rows'],'canonical_sha256':runs[0]['canonical_sha256']},'source':(link('results/postgres-100m-2026-11-09/athena-statements.json.gz') if cid=='100m' else 'https://github.com/yorrick/openalex-clickhouse-spike/blob/7dc30e093afd189cd03a706f8abf203ff1ccd1c5/results/benchmark-artifact-2026-11-13/athena-200m-executions.json')})
# 200m native baseline and selected profiles, both matched budgets.
for eng in ['postgres','clickhouse']:
 for selected,suffix in [(False,'cases'),(True,'selected')]:
  for name,c in load(C200/(eng+'-'+suffix+'.json')).items():record(c,'200m',eng+'_ec2','ec2_200',selected,link('results/ec2-200m-2026-11-12/frozen-evidence.tar.gz'))
P['schemas']['postgres_200m']=load(S200/'projection-templates.json')['pg_schema'];P['schemas']['postgres_200m_indexes']=load(S200/'projection-templates.json')['indexes'];P['schemas']['clickhouse_200m']=(S200/'sql/clickhouse-schema.sql').read_text();P['schemas']['clickhouse_projection']='ALTER TABLE citation_edge ADD PROJECTION by_cited (SELECT * ORDER BY (cited_work_id,citing_work_id))'
P['storage']={'observed_200m':load(C200/'clickhouse/prepared.json'),'postgres_200m':load(C200/'postgres/prepared.json'),'final_directories':load(C200/'final-directory-bytes.json'),'projection_basis':'200m active parts including reverse citation projection; fixed dimension tables stay constant; Work-related tables scale by Work count. Width and relationship density assumed unchanged. Not all fields, not a RAM/latency forecast.'}
fixed=sum(x['bytes_on_disk'] for x in P['storage']['observed_200m']['storage'] if x['table'] in ['authors','institutions','sources','topics']);total=sum(x['bytes_on_disk'] for x in P['storage']['observed_200m']['storage']);full=510372821;factor=full/200313862
P['storage'].update(fixed_dimension_bytes=fixed,variable_bytes_200m=total-fixed,reference_works=200313862,historical_full_works=full,conditional_full_bytes=fixed+(total-fixed)*factor)
P['costs']={'legacy_ec2_2m_to_32m':load(R/'aws-scaling-2026-11-06/costs.json'),'200m':load(S200/'results/cost-estimate.json'),'100m_athena':{'bytes':sum100['athena_billable_bytes'],'estimate_usd':sum100['athena_scan_cost_estimate_usd_at_5_per_decimal_tb'],'other_costs':'Not reconciled in this comparison; laptop hardware/electricity not measured.'}}
P['verification_200m']=load(S200/'results/verification.json');P['cleanup_200m']=load(S200/'results/aws-cleanup.json')
P['retention']={'observed':'The 200m raw/projected/database volumes were deleted without snapshots. Only the prior raw-data volume was preserved.','future_policy':'Keep the largest verified raw/normalized corpus and snapshots of prepared databases; retire the smaller retained copy only after validating the replacement. Use saved cohort manifests for exact smaller subsets. A clean 100m scaling test still needs a database physically built from that subset.'}
P['rationale']={'openalex':[{'claim':'CC0 open data, public S3 snapshots available without an AWS account.','source':'https://help.openalex.org/access/snapshot/'},{'claim':'Works link authors, institutions, sources, topics and citation references, matching the bibliometrics workload.','source':'https://help.openalex.org/data/'},{'claim':'Quarterly public snapshots are free; daily updates are a separate paid service. Production sync/deletions/merges were not benchmarked.','source':'https://help.openalex.org/access/sync/'}],'clickhouse':'Selected analytical workload: 6/7 families meet a warm median below 60 s at 200m, versus 3/7 PostgreSQL at matched caps. PostgreSQL wins the indexed graph lookups; q03 remains unvalidated in both engines at 200m. No universal PostgreSQL limit is established.','single_machine':'Observed 200m database fits one host. Full selected-schema storage looks plausible on one larger single machine, based on explicitly conditional arithmetic; full-corpus latency, RAM need, richer fields and concurrent workloads remain unvalidated. Storage size does not equal peak join memory.'}
P['review_status']={'underlying_200m':'Draft: prescribed DeepSeek/GLM external CLI attempts were quota-blocked. No underlying PostgreSQL validation by Claude is requested.','artifact':'New artifact authorship and review are recorded separately.'}
P['sources']=[{'label':'200m report and all caveats','url':link('docs/ec2-200m-benchmark.md')},{'label':'100m report','url':link('docs/postgres-100m-benchmark.md')},{'label':'32m PostgreSQL scaling report','url':link('docs/postgres-scaling-benchmark.md')},{'label':'2m/10m PostgreSQL report','url':link('docs/postgres-local-benchmark.md')},{'label':'Original 2m/10m/32m EC2 and local ClickHouse series','url':legacy['source_links']['report']},{'label':'Field inventory','url':legacy['source_links']['field_inventory']},{'label':'200m full frozen evidence','url':link('results/ec2-200m-2026-11-12/frozen-evidence.tar.gz')}]
# Explicit presentation-only QA relationship: compare stored fingerprints,
# not a rerun or a review of any underlying PostgreSQL benchmark.
refs={(r['cohort'],r['case_key']):r for r in P['records'] if r['engine_key']=='athena' and r['selected']}
for r in P['records']:
 if r['engine_key']=='athena' or r['state']!='complete':continue
 ref=refs.get((r['cohort'],r['case_key']));q=r.get('qa') or {};rh=((ref or {}).get('qa') or {}).get('canonical_sha256')
 if q.get('canonical_sha256') and rh:
  assert q['canonical_sha256']==rh
  q['recorded_fingerprint_matches_raw_athena']=True

# Dataset-wide integrity checks; every populated native/managed SQL is literally preserved.
for r in P['records']:
 if r.get('sql'):assert sha(r['sql'])==r['sql_sha256']
 if r['state'] not in ['complete','historical']:assert r['median_seconds'] is None
for cid in P['cohorts']:
 selected=[r for r in P['records'] if r['cohort']==cid and r['selected']];keys=[(r['engine_key'],r['case_key']) for r in selected];assert len(keys)==len(set(keys)),(cid,'duplicate selected record')
out=HERE/'artifact-payload.json';out.write_text(json.dumps(P,ensure_ascii=False,separators=(',',':'))+'\n')
report={'payload_bytes':out.stat().st_size,'payload_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'records':len(P['records']),'exact_sql_records':sum(bool(r.get('sql')) for r in P['records']),'exact_executed_sql_records':sum(r['sql_status']=='exact_executed' for r in P['records']),'unexecuted_sql_definitions':sum(r['sql_status']=='not_executed' for r in P['records']),'conditional_full_gb':P['storage']['conditional_full_bytes']/1e9,'cohorts':{c:{e:sum(r['cohort']==c and r['engine_key']==e and r['selected'] for r in P['records']) for e in ['postgres_local','clickhouse_local','postgres_ec2','clickhouse_ec2','athena']} for c in P['cohorts']}}
(HERE/'payload-integrity.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
