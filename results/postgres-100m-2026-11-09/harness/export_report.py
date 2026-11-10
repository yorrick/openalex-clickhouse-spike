"""Archive verified evidence and write factual100mreport, without changing32mresults."""
from pathlib import Path
import gzip,hashlib,json,shutil,statistics,time
from pg_helpers import HERE,dump
REPO=Path('/Users/yorrickjansen/work/openalex/.claude/worktrees/postgres-scaling')
DEST=REPO/'results/postgres-100m-2026-11-09'
OLD=Path('/Users/yorrickjansen/work/data/openalex-postgres-20261108')
FAMILIES=['q01','q02','q03','q04','q05','q06','q07']
LABELS=['Year/type/open-access counts','Topic/year metrics','Top 1000 authors','International country collaboration','One-hop citations, 3 seeds','Two-hop citations, 3 seeds','Top 1000 citation/year counts']

def read(p):return json.loads(Path(p).read_text())
def gz(path,obj):
 with gzip.open(path,'wt',encoding='utf8') as f:json.dump(obj,f,ensure_ascii=False,default=str)
def groups(cases,athena=False):
 result={}
 for family in FAMILIES:
  xs=[v for k,v in cases.items() if k[:3]==family];times=[]
  for v in xs:
   if athena:
    if len(v.get('runs',[]))==3:times.append(statistics.median(x['statistics']['TotalExecutionTimeInMillis']/1000 for x in v['runs']))
   elif v.get('state')=='complete':times.append(v['median_seconds'])
  result[family]=max(times) if len(times)==len(xs) and xs else None
 return result

def val(x):return f'{x:.6f}' if x is not None else 'Incomplete/timeout'
def main():
 verification=read(HERE/'results/verification.json');assert verification['pass']
 pg=read(HERE/'postgres-cases.json');ch=read(HERE/'clickhouse-cases.json') if (HERE/'clickhouse-cases.json').exists() else {};ath=read(HERE/'athena-cases.json');decision=read(HERE/'postgres-decision-final.json');clean=read(HERE/'results/aws-cleanup.json');resources=read(HERE/'results/resources.json')
 DEST.mkdir(exist_ok=True);(DEST/'sql').mkdir(exist_ok=True);(DEST/'harness').mkdir(exist_ok=True)
 for f in HERE.glob('*.py'):shutil.copy2(f,DEST/'harness'/f.name)
 for f in (HERE/'sql').glob('*.sql'):shutil.copy2(f,DEST/'sql'/f.name)
 for name in ['experiment-plan.json','experiment-plan-original.json','requirements.lock','postgres-decision-initial.json','postgres-decision-final.json','aws-state.json']:
  if (HERE/name).exists():shutil.copy2(HERE/name,DEST/name)
 gz(DEST/'postgres-cases.json.gz',pg);gz(DEST/'postgres-baseline-aggregates.json.gz',read(HERE/'postgres-aggregate-cases.json'));gz(DEST/'postgres-targeted-trials.json.gz',read(HERE/'postgres-targeted-trials.json'));shutil.copy2(HERE/'targeted-tuning-plan.json',DEST/'targeted-tuning-plan.json');gz(DEST/'clickhouse-cases.json.gz',ch);gz(DEST/'clickhouse-initial24-cases.json.gz',read(HERE/'clickhouse-cases-before-author-tune.json')); gz(DEST/'athena-cases.json.gz',ath)
 for name in ['works-input-manifest.json','remote-inputs.json','athena-statements.json']:
  gz(DEST/(name+'.gz'),read(HERE/name))
 proofs={};telemetry={}
 for f in (HERE/'results').rglob('*.json'):
  relative=str(f.relative_to(HERE/'results'))
  if f.name.endswith('-telemetry.json'):telemetry[relative]=read(f)
  elif not relative.startswith(('postgres/q','clickhouse/q')):proofs[relative]=read(f)
 gz(DEST/'proofs.json.gz',proofs);gz(DEST/'telemetry.json.gz',telemetry)
 shutil.copy2(HERE/'results/verification.json',DEST/'verification.json')
 events=HERE/'results/postgres/memory-events.jsonl'
 if events.exists():
  with events.open('rb') as src,gzip.open(DEST/'postgres-memory-events.jsonl.gz','wb') as dst:shutil.copyfileobj(src,dst)
 for name in ['server-project.log','projection.log','postgres.log','athena.log','athena-resume.log','clickhouse.log','projection-initial-error.log','postgres-first-driver.log','postgres-resumed.log','validation-recovery.log','aggregate.log','targeted.log','aws-cleanup.log','normalization-qa.log','clickhouse-profile24-resumed.log','ch-profile-switch.log','clickhouse-author-tuning.log']:
  if (HERE/name).exists():shutil.copy2(HERE/name,DEST/name)
 p=groups(pg);c=groups(ch);a=groups(ath,True);oldcases=read(OLD/'scaling-decision.json')['selected_best_observed_cases'];old={f:max(v['median_seconds'] for k,v in oldcases.items() if k[:3]==f and v.get('median_seconds') is not None) for f in FAMILIES}
 summary={'date':'2026-11-09','works':100087422,'columns':42,'table_counts':verification['table_counts'],'total_rows':verification['total_rows'],'postgres_family_medians':p,'clickhouse_family_medians':c,'athena_family_service_medians':a,'decision':decision,'verification':verification,'athena_billable_bytes':clean['billable_athena_bytes'],'athena_scan_cost_estimate_usd_at_5_per_decimal_tb':clean['billable_athena_bytes']/1e12*5}
 dump(DEST/'summary.json',summary)
 rows=[]
 for fam,label in zip(FAMILIES,LABELS):rows.append(f'| {fam}: {label} | {val(old[fam])} | {('Not run (storage limit)' if fam in ('q05','q06','q07') else val(p[fam]))} | {val(c.get(fam))} | {val(a[fam])} |')
 table='\n'.join(rows)
 countrows='\n'.join(f'| `{k}` | {v:,} |' for k,v in verification['table_counts'].items())
 resource_rows=[]
 for fam in FAMILIES:
  for engine,cases in [('PostgreSQL',pg),('ClickHouse',ch)]:
   xs=[v for k,v in cases.items() if k[:3]==fam and v.get('state')=='complete']
   if not xs:continue
   worst=max(xs,key=lambda v:v['median_seconds']);runs=worst['runs'][1:];cores=statistics.median(r['resources']['average_busy_cores_in_monitor_window'] for r in runs);peak=max(r['resources']['memory_current_peak_bytes'] for r in runs)/(1<<30)
   resource_rows.append(f'| {fam} | {engine} | {cores:.2f} | {peak:.2f} |')
 storage=read(HERE/'results/postgres/storage-after-aggregates.json');pgbytes=storage['database_bytes'];indexbytes=sum(t['indexes_bytes'] for t in storage['tables']);chstore=read(HERE/'results/clickhouse/storage-before-queries.json') if ch else [];compressed=sum(int(t['data_compressed_bytes']) for t in chstore);chdisk=sum(int(t['bytes_on_disk']) for t in chstore)
 normalized=sum(read(HERE/'results'/('project-'+t+'.json'))['bytes'] for t in verification['table_counts'])
 raw=sum(f['bytes'] for f in read(HERE/'remote-inputs.json')['files'])
 failed=decision.get('missed_60_seconds',[])
 conclusion=('PostgreSQL did not establish the sub60secondwarmmedian target at100mWorks for '+', '.join(failed)+'. Volume growth stopped atthiscohort.' if failed else 'All requiredPostgreSQLwarmmediansmetthe60secondtarget at100mWorks. No fullcorpus performanceclaimismade.')
 costrows=[]
 for family in FAMILIES:
  xs=[v for k,v in ath.items() if k[:3]==family]
  if xs and all(len(v['runs'])==3 for v in xs):
   scanned=max(statistics.median(run['statistics']['DataScannedInBytes'] for run in v['runs']) for v in xs)
   import math
   billed=max(10000000,math.ceil(scanned/1000000)*1000000)
   costrows.append(f'| {family} | {scanned/1e9:.3f} | ${billed/1e12*5:.4f} |')
 text=f'''# OpenAlex: PostgreSQL at 100 million Works

{conclusion} This describes the tested laptop configuration and selected analytical schema. It does not establish a universal PostgreSQL limit or prove that the full corpus needs a cluster.

## Query measurements

All values are seconds. PostgreSQL and ClickHouse report the median of three warm native executions after one first observation. Athena reports the median of three service total times, including queue, planning and result output, with result reuse disabled. For q05/q06, each family reports the largest of the three fixed seed medians. Incomplete cases have no fabricated median.

| Query family | PG 31.89m, selected profile | PG 100.09m, selected profile | Local CH 100.09m | Athena 100.09m, raw Parquet |
|---|---:|---:|---:|---:|
{table}

PostgreSQL starts with the selected 32m profiles: `work_mem=128MB` for q01/q05/q06, `512MB` for q02/q03/q04/q07, and author preaggregation with `enable_nestloop=off` for q03. The final decision JSON records any bounded 100m trial and every selected case label. ClickHouse uses 16 threads. q01 was measured with a 12 GiB query limit and automatic join selection. q02-q07 use a 24 GiB query limit, explicit hash joins and 4 GiB external aggregation/sort thresholds, within the unchanged 32 GiB container. q02 aggregates numeric topic/year statistics before joining names. Its initial 12 GiB profile used an external join and took 228.282 s for the first observation; that interrupted profile has no three-warm median or full-result QA. The original q03 reached its 24 GiB query limit and has no completed timing; the selected variant filters valid Author IDs, aggregates numeric statistics and ranks 1000 IDs before fetching names. All completed selected variants pass full-result QA. These are selected observed profiles, not controlled estimates of the speedup caused by one setting.

[Exact SQL](../results/postgres-100m-2026-11-09/sql) and [full evidence](../results/postgres-100m-2026-11-09/) include every native observation, PostgreSQL plan, requested/effective setting, full-result fingerprint and resource trace. PostgreSQL native time excludes planning and output fetching; ClickHouse uses `FORMAT Null`. Athena service total time is an operational latency measure, not the same timing boundary.

## Data and storage

The nested historical cohort contains 480 pinned Work files, including all 154 from the previous cohort: **100,087,422 Works**, or 19.61% of the 510,372,821 Works in the June snapshot. That denominator is historical. All 119,129,660 Authors and the same complete historical Institutions, Sources and Topics are retained. Only 42 normalized columns across 9 tables are loaded, not every OpenAlex field or entity type.

| Table | Exact loaded rows |
|---|---:|
{countrows}

The raw Work objects total 141.981 GB; all selected raw objects including fixed dimensions total {raw/1e9:.3f} GB. The 9 normalized local Parquet payloads total {normalized/1e9:.3f} GB. PostgreSQL occupies {pgbytes/1e9:.3f} GB for the database, including {indexbytes/1e9:.3f} GB of its 12 completed indexes; this excludes WAL and the two citation indexes that were not completed. All 9 tables are loaded. At 100m, only q01-q04 were measured in PostgreSQL: citation-index creation hit the host disk guard, and the aggregate families already missed the one-minute target. PG citation cells are unmeasured, not timeouts or zeroes. ClickHouse active parts occupy {chdisk/1e9:.3f} GB on disk, including {compressed/1e9:.3f} GB of compressed column data. These describe different physical layouts and are labelled separately. GB means 10^9 bytes; GiB means 2^30 bytes.

## CPU, memory and I/O

Both local engines have **16 CPU / 32 GiB container limits**, with no container swap, on an Apple M5 Max laptop with 18 physical cores and 128 GiB host RAM. Athena on-demand CPU and RAM allocation are not exposed by this test. Queries run one at a time; concurrency was not tested. The Docker VM has 16 CPUs and approximately 47 GiB RAM. PostgreSQL uses 8 GiB shared buffers, up to 8 workers per Gather and 16 global parallel workers. Data uses host bind mounts through VirtioFS, with host file caching outside container accounting. The engines run sequentially; unrelated laptop/VM activity is not isolated.

| Family | Engine | Median average busy cores, warm window | Largest sampled container RAM, warm GiB |
|---|---|---:|---:|
{chr(10).join(resource_rows)}

CPU is cgroup CPU time divided by the instrumented client window. Memory includes shared buffers and file cache; it is not the allocation of just one query. File/shmem counters overlap. Graph queries are too short for reliable CPU/RAM attribution at this sampling interval. Traces include cgroup I/O/pressure and unisolated host disk counters. PostgreSQL plans include logical shared/temp blocks and I/O timings; ClickHouse logs include read bytes and ProfileEvents.

VirtioFS may leave cgroup block I/O empty. Logical reads and shared host counters do not establish physical SSD bandwidth or minimum provisioned IOPS. Allocating 16 CPUs does not mean 16 cores are busy. These measurements do not prove a minimum native Linux hardware configuration or that adding CPUs alone would remove serial or spill bottlenecks.

## Preparation and result QA

Raw objects were copied directly from immutable public S3 versions into a private temporary bucket in certification account 502425560524, `us-east-1`. No raw laptop data was uploaded. The initial 80 GiB host reserve stopped a citation-index build; aggregate measurements then used a protected 40 GiB reserve. Existing backups and historical databases were preserved. All 480 Work footer counts match the pinned manifest. AWS recorded full-object SHA256 for every copied object: 2771 existing objects also match prior full SHA256, while 326 new historical objects have newly recorded server checksums.

The first laptop remote-column projection was interrupted while incomplete because the observed preparation was network-bound. After a real CTAS value/codec probe, Athena produced 5 normalized Work/relationship payloads in AWS. Those flat files were downloaded and consolidated locally. Fixed dimensions came from the existing verified local cache. Bulk COPY, index creation and vacuum timings are archived separately. Citation COPY committed, but its first validation count hit the five-minute deadline before its exact COPY duration was saved; the recovered full count matched 622,671,173 rows without reloading. That COPY duration is unavailable. Index maintenance used a separate 30-minute deadline, 8 GiB maintenance memory and up to 8 maintenance workers, within the same container limits. Incomplete preparation attempts and their costs remain in the evidence, rather than being presented as completed load performance.

Heap insertion order and preparation differ from the 32m test. Growth ratios are therefore descriptive observations, not an isolated asymptotic scaling law. With the same q01 profile, Work count grows 3.139 times and its median grows 3.019 times, consistent with approximately linear scanning over this interval. With the same selected 32m author profile, q03 grows from 25.192 to 102.889 s, a 4.084-fold increase; the retuned 100m result is 81.338 s. The topic and collaboration plans hit the 300 s deadline before retuning. These observations show plan and sort-memory thresholds, not a single smooth scaling curve. There are too few controlled scale points to certify a linear or nonlinear model.

Native queries use pre-flattened, indexed data; raw Athena repeats normalization per query. This does not test an optimized Athena CTAS layout. Citation edges originate from selected citing Works, and targets may lie outside the cohort.

Timed Athena queries still use views over the exact 480 raw Work files and fixed raw dimensions, rather than the normalized CTAS output. Full result sets are canonicalized with explicit integer, boolean, string and NULL types, preserving duplicate multiplicity. Every completed local case is compared against the full raw Athena result fingerprint. The verification file reports exact QA counts and independently reparses the archived full Athena CSV results. The CTAS transformation was also compared with the independent DuckDB normalizer on two real raw files (290,149 Works), with exact symmetric EXCEPT ALL equality across retained Work-derived fields. This is a sample transformation audit, not an independent transformation audit of all 100m Works.

Timed queries have a 300 second deadline. Where needed, the exact same raw Athena SQL is run once with a longer validation-only deadline and excluded from the timed median. Timeout and validation records remain distinct.

## Cost and cleanup

All Athena statements, including preparation, QA, interrupted work and repeats, total **{clean['billable_athena_bytes']/1e9:.3f} GB** of rounded billable scan. At $5 per decimal TB, that is an estimated **${clean['billable_athena_bytes']/1e12*5:.4f}** in scan charges, not a final invoice.

The following costs describe one timed invocation, using the median scan volume and the largest seed median for graph families. They exclude S3 storage, requests and downloads.

| Family | Scanned GB per invocation | Estimated Athena scan cost |
|---|---:|---:|
{chr(10).join(costrows)}

S3 charges are additional. About 10.093 GB of private S3 payload downloads are estimated, including normalized data and repeated result downloads. Assuming $0.09 per GiB, that adds $0 to $0.846 depending on the account-wide free allowance; the final invoice is not available. A conservative full-bucket-for-entire-lease storage estimate is $0.012, and the 3097 known COPY requests add about $0.0155 at $0.005 per 1000. Other S3 request charges were not metered separately. These rates are explicit estimate assumptions, not a complete invoice reconciliation. No EC2 instance was provisioned for this extension. Local hardware and electricity are excluded, and the previously retained raw EBS volume remains separate and unchanged. Pricing sources: [Athena](https://aws.amazon.com/athena/pricing/) and [S3](https://aws.amazon.com/s3/pricing/).

The private temporary bucket and its objects, Glue tables/database and Athena workgroup were deleted. API absence probes and terminal query receipts are archived. Normalized local payloads and full CSV results remain in the durable study directory. Repeating raw Athena QA later depends on continued availability of the pinned public versions.

This study does not establish full-corpus latency, a hardware minimum, or production incremental-update throughput. The prior results remain in [the 32m report](postgres-scaling-benchmark.md). External CLI review remains incomplete: the prior DeepSeek v4.1 Flash and GLM 5.3 Flash attempts through opencode hit the key's hard quota. Exact commands, models and failure output are retained in [the review status](../results/postgres-scaling-2026-11-09/scaling-review-status.json). No completed external review is claimed, and Claude Code validation was not requested.
'''
 # Human-readable typography, preserve exact code/file names and standard tokens.
 replacements={'sub60secondwarmmedian':'sub-60-second warm median','at100mWorks':'at 100m Works','atthiscohort':'at this cohort','requiredPostgreSQLwarmmediansmetthe60secondtarget':'required PostgreSQL warm medians met the 60-second target','fullcorpus performanceclaimismade':'full-corpus performance claim is made','selectedprofile':'selected profile','PG31.89m':'PG 31.89m','PG100.09m':'PG 100.09m','LocalCH100.09m':'Local CH 100.09m','Athena100.09m':'Athena 100.09m','rawParquet':'raw Parquet','largest sampledcontainerRAM':'largest sampled container RAM','Exactloadedrows':'Exact loaded rows'}
 for k,v in replacements.items():text=text.replace(k,v)
 (REPO/'docs/postgres-100m-benchmark.md').write_text(text)
 print('Wrote',REPO/'docs/postgres-100m-benchmark.md')
if __name__=='__main__':main()
