from pathlib import Path
import json,statistics,math
H=Path(__file__).resolve().parent;R=H/'cloud-results';OUT=Path('/Users/yorrickjansen/work/openalex/.claude/worktrees/ec2-200m/docs/ec2-200m-benchmark.md')
def read(p):return json.loads(p.read_text())
pg=read(R/'postgres-selected.json');ch=read(R/'clickhouse-selected.json');ath=read(H/'athena-cases.json');summary=read(H/'results/native-summary.json');cost=read(H/'results/cost-estimate.json');verify=read(H/'results/verification.json');cleanup=read(H/'results/aws-cleanup.json');prep=read(R/'projection-complete.json')
labels=['Year/type/OA counts','Topic/year metrics','Top 1000 authors','International collaboration','One-hop citations','Two-hop citations','Citation/year top 1000']
queries=['q01','q02','q03','q04','q05','q06','q07']
past_pg=[16.836854,84.083428,81.338434,74.583536,None,None,None];past_ch=[.186,13.601,18.140,34.348,.029,.193,18.867]
def family(cases,q):
 xs=[v for k,v in cases.items() if k.startswith(q)]
 if any(v['state']!='complete' for v in xs):return 'Timeout (300 s)' if any(v['state']=='timeout' for v in xs) else 'Memory failure; no median'
 x=max(v['median_seconds'] for v in xs);return f'{x:.6f}' if x<.01 else f'{x:.3f}'
def sql_link(engine,name):
 c=(pg if engine=='postgres' else ch)[name];label=c.get('label',name)
 return f'[{"PG" if engine=="postgres" else "CH"}](../experiments/ec2-200m/sql/executed-{engine}-{label}.sql)'
qtable=['| Query family and exact SQL | Local PG 100.09m s | Local CH 100.09m s | EC2 PG 200.31m s | EC2 CH 200.31m s | Raw Athena 200.31m s |','|---|---:|---:|---:|---:|---:|']
for i,q in enumerate(queries):
 name=q+'-s51557542' if q in ['q05','q06'] else q
 av=max(statistics.median(r['statistics']['TotalExecutionTimeInMillis']/1000 for r in c['runs']) for k,c in ath.items() if k.startswith(q))
 qtable.append(f'| {q} {labels[i]} ({sql_link("postgres",name)}, {sql_link("clickhouse",name)}) | '+(f'{past_pg[i]:.3f}' if past_pg[i] is not None else 'Not run')+f' | {past_ch[i]:.3f} | {family(pg,q)} | {family(ch,q)} | {av:.3f} |')
pgstorage=read(R/'postgres/prepared.json')['storage'];cs=read(R/'clickhouse/prepared.json');pgt={t['table']:t for t in pgstorage['tables']};cht={t['table']:t for t in cs['storage']}
fields={'works':'work_id, canonical_id, publication_year, work_type, source_id, is_oa, is_xpac, cited_by_count, primary_topic_id','work_author':'work_id, author_id, author_position, is_corresponding','work_institution':'work_id, author_id, institution_id','work_topic':'work_id, topic_id, score, is_primary','citation_edge':'citing_work_id, cited_work_id, citing_year','authors':'author_id, canonical_id, display_name, orcid','institutions':'institution_id, canonical_id, display_name, country_code, institution_type','sources':'source_id, canonical_id, display_name, issn_l, source_type','topics':'topic_id, display_name, subfield_id, field_id, domain_id'}
dtable=['| Loaded table | Exact rows | Selected columns | PG table + indexes GB | CH active parts GB |','|---|---:|---|---:|---:|']
for t,n in prep['counts'].items():dtable.append(f'| `{t}` | {n:,} | {fields[t]} | {pgt[t]["total_bytes"]/1e9:.3f} | {cht[t]["bytes_on_disk"]/1e9:.3f} |')
resource=['| Engine / family (seed for graph rows) | Avg busy cores / 16 | Peak container GiB | Peak anon / shmem GiB | Median read / write GiB | Avg read / write MiB/s | Avg read / write IOPS |','|---|---:|---:|---:|---:|---:|---:|']
for engine,cases in [('postgres',pg),('clickhouse',ch)]:
 for q in queries:
  xs=[v for k,v in cases.items() if k.startswith(q)]
  if any(c['state']!='complete' for c in xs):continue
  c=max(xs,key=lambda x:x['median_seconds']);rs=[r['resources'] for r in c['runs'][1:]];dt=sum(r['window_seconds'] for r in rs)
  cpu=sum(r['cpu_seconds'] for r in rs)/dt;mem=max(r['memory_current_peak_bytes'] for r in rs)/2**30;anon=max(r['memory_anon_peak_bytes'] for r in rs)/2**30;shmem=max(r['memory_shmem_peak_bytes'] for r in rs)/2**30
  readg=statistics.median(r['io_delta']['rbytes']/2**30 for r in rs);writeg=statistics.median(r['io_delta']['wbytes']/2**30 for r in rs);rb=sum(r['io_delta']['rbytes'] for r in rs)/dt/2**20;wb=sum(r['io_delta']['wbytes'] for r in rs)/dt/2**20;ri=sum(r['io_delta']['rios'] for r in rs)/dt;wi=sum(r['io_delta']['wios'] for r in rs)/dt
  resource.append(f'| {engine} {c["name"]} | {cpu:.2f} | {mem:.2f} | {anon:.2f} / {shmem:.2f} | {readg:.3f} / {writeg:.3f} | {rb:.1f} / {wb:.1f} | {ri:.1f} / {wi:.1f} |')
failed=['| Incomplete selected profile | Observation | Resource window s | Avg busy cores | Peak container GiB | Read / write GiB |','|---|---|---:|---:|---:|---:|']
for engine,cases in [('postgres',pg),('clickhouse',ch)]:
 for name,c in cases.items():
  if c['state']=='complete':continue
  r=c.get('resources') or c['runs'][-1]['resources'];kind='first attempt, timeout' if engine=='postgres' else 'second warm attempt, memory failure'
  failed.append(f'| {engine} {c.get("label",name)} | {kind} | {r["window_seconds"]:.3f} | {r["average_busy_cores"]:.2f} | {r["memory_current_peak_bytes"]/2**30:.2f} | {r["io_delta"]["rbytes"]/2**30:.3f} / {r["io_delta"]["wbytes"]/2**30:.3f} |')
scantable=['| Family | Timed runs | Observed scan GB range per run | Estimated cost of all timed runs USD |','|---|---:|---:|---:|']
for q in queries:
 xs=[r for k,c in ath.items() if k.startswith(q) for r in c['runs']];bs=[r['statistics']['DataScannedInBytes'] for r in xs];bill=sum(max(10_000_000,math.ceil(b/1e6)*1_000_000) for b in bs)
 scantable.append(f'| {q} | {len(xs)} | {min(bs)/1e9:.3f} - {max(bs)/1e9:.3f} | {bill/1e12*5:.4f} |')
infra=sum(v for k,v in cost['estimated_usd'].items() if k!='athena')
text=f'''# PostgreSQL and ClickHouse at 200 million Works on EC2

Measured 12 November 2026 on **200,313,862 Works**. ClickHouse established a warm median below 60 seconds for **six of seven query families**, PostgreSQL for **three of seven**. ClickHouse author aggregation remains unvalidated at the 24 GiB query limit: two executions completed around 58 seconds, then another failed for memory, leaving no valid three-warm median.

Both engines ran sequentially on one EC2 host with the same **16 CPU / 32 GiB container budget**. The results favor ClickHouse for this selected analytical workload, while PostgreSQL was faster for the indexed graph lookups. They do not rule out other PostgreSQL configurations, establish full-corpus latency, or validate the separately requested richer final schema. The required external AI CLI review is still blocked by the personal OpenRouter quota, so this report and PR remain drafts.

## Performance and the earlier laptop run

Seconds below are medians of three warm executions after one first observation. q05/q06 use the largest of the three fixed-seed medians, independently for each engine. A timeout is an incomplete observation, not a measured 300-second median. The author failure is also incomplete, not a 58-second result.

{chr(10).join(qtable)}

The [100m laptop report](postgres-100m-benchmark.md) and [32m report, including 2m/10m history](postgres-scaling-benchmark.md) contain the earlier profiles. The laptop was an Apple M5 Max (18 cores, 128 GiB host RAM), with 16 CPU / 32 GiB containers in a Docker VM and VirtioFS data mounts. EC2 used native Linux ARM and gp3. PostgreSQL 100m had 12 indexes because the host disk guard stopped citation-index creation; 200m has all 14. SQL and selected profiles also changed. This table compares observed setups and cannot isolate a volume growth law.

The 200m run exposed memory thresholds: the unchanged ClickHouse hash-join profiles for q02/q03/q04 failed before tuning. q02 then completed at 37.630 s with partitioned joins, and the q04 country-set rewrite completed at 6.986 s. PostgreSQL q01 became faster on EC2 despite more rows, while q04 became slower. These observations do not support fitting a single linear latency curve across the two machines. No controlled minimum-CPU, minimum-RAM, cold-cache, concurrency or full-corpus SLA was measured.

Native timings exclude result transfer. PostgreSQL reports EXPLAIN execution time, excluding planning; ClickHouse reports query-log duration with FORMAT Null. Sub-millisecond PostgreSQL graph values are not application response times. Athena uses service total time, including queue, planning and output, with result reuse disabled. Its independent raw-Parquet views repeat normalization and are not an optimized flattened/CTAS lake layout, so this is a workflow comparison rather than a pure engine-only comparison.

## Data volume, entities and fields

The pinned historical June 2026 snapshot contains 510,372,821 Works. This cohort is **39.25%** of it, with 127,375,852 core Works and 72,938,010 XPAC Works. Its 955 Work files preserve all 480 files in the earlier 100m selection. The four complete historical dimensions below remain fixed. Referenced Works outside the selected cohort can be target IDs, but their outgoing edges are not added; graph queries operate on the selected edge cohort.

{chr(10).join(dtable)}

The nine tables contain **2,546,445,961 rows and 42 selected columns**. PostgreSQL database contents total **326.477 GB**, including **{sum(t['indexes_bytes'] for t in pgt.values())/1e9:.3f} GB of indexes**; this excludes WAL and temporary files. ClickHouse active parts total **31.837 GB**, including the **9.453 GB reverse citation projection**. Main compressed column data is 22.380 GB, a narrower measure than total stored parts. Final bind-directory sizes, including engine logs/WAL, are 330.797 GB for PostgreSQL and 32.015 GB for ClickHouse. Compressed disk size does not equal query working memory, as the hash-join failures demonstrate.

Raw Works total 288.202 GB. The full provenance catalog has 3,572 objects and 341.270 GB across 20 entity types; the five loaded source entities account for 3,179 objects and 341.240 GB. The other 393 lookup files total 30.131 MB and are not loaded into this benchmark schema. Shared normalized Parquet totals **20.284 GB in 6,999 fragments**. GB means 10^9 bytes; GiB means 2^30 bytes. A footer sample of one pinned source file per entity showed SNAPPY compression; this is a sample, not an assertion about every shard.

Raw data was downloaded directly from public historical S3 VersionIds onto EC2, with size, full SHA256 and footer-count verification. No raw data was uploaded from or downloaded to the laptop. Athena used a separate server-side copy of those exact source versions. Both native engines consumed identical sealed normalized payloads. The wider set of useful final fields/entities remains pending and is not silently included in these measurements.

## Configured and observed resources

| Item | Observed configuration |
|---|---|
| AWS account / region | Certification 502425560524 / us-east-1 |
| Host | Ubuntu 24.04 ARM, m7g.4xlarge, 16 Graviton cores / 64 GiB RAM |
| Each database | Sequential Docker execution, 16 CPU / 32 GiB memory limits, no swap |
| PostgreSQL | 18.6, pinned image; 8 GiB shared buffers; 8 workers per Gather / 16 global parallel workers; durability enabled |
| ClickHouse | 26.3.12.3 pinned image; 16 query threads; 24 GiB query cap |
| EBS | Encrypted 1,024 GiB gp3 scratch, 6,000 IOPS / 500 MiB/s; 32 GiB root; both deleted |
| Timing collection | Native Linux cgroup CPU, memory, events and block I/O at about 0.5 s; host iostat/vmstat at 1 s |

The following completed-family rows use the selected profile and, for graph families, the seed with the largest median. CPU is total cgroup CPU time divided by the combined three warm windows. RAM is the maximum sampled container usage across those windows. Read/write volumes are medians; bandwidth and IOPS use total counters divided by total windows. All per-seed traces are retained.

{chr(10).join(resource)}

Memory includes already resident server state and file cache; these values are not incremental RAM required by a query. Anonymous memory omits shared buffers, and shmem overlaps file accounting. Peaks can occur at different times and must not be added. Short graph resource windows have coarse attribution. The OS page cache was dropped before each main engine query phase, while internal database caches were not reset; the first observation is therefore not guaranteed cold. The reported repetitions are warm. Near-zero warm physical reads do not establish a minimum EBS bandwidth for loading or cold execution.

Incomplete selected attempts have their own telemetry, without a fabricated warm median:

{chr(10).join(failed)}

PostgreSQL collaboration averaged 1.69 busy cores out of 16; its ordered citation trial averaged about one. ClickHouse collaboration averaged 14.08 and citation aggregation 15.20. This identifies substantial utilization differences in these selected plans, not proof that more vCPUs alone would fix PostgreSQL. Athena does not expose an equivalent per-query CPU/RAM allocation through this experiment; scan and service metrics are retained instead.

## Tuning, loading and QA

PostgreSQL had the full 14-index design, including both citation directions. Topic and author SQL preaggregate numeric IDs and fetch names late; collaboration uses distinct country sets. The original 2 GiB work_mem q02/q03 attempts exhausted Docker's separate 8 GiB shared-memory filesystem. A repair recreated only the stopped container against the same PGDATA, raised the tmpfs ceiling to 32 GiB within the unchanged 32 GiB total memory limit, and used 512 MB work_mem per operation. Both then reached the 300-second deadline without a shared-memory failure. q07 also timed out with grouping reordered to use the existing cited-work-leading index, incremental sort and enable_hashagg=off. The baseline failures and all repaired profiles are preserved.

ClickHouse began with 16 threads, explicit hash joins, a 24 GiB query cap, 4 GiB aggregation/sort spill thresholds and the reverse citation projection. Its three initial large-join failures attempted a 16 GiB hash-table growth. q02/q03 received one explicit grace-hash profile with 16 initial buckets and a 3 GiB per-join bound, retaining the SQL and overall allocation. A real miniature join probe passed before the full trials. This partitioning behavior is described in [ClickHouse's join implementation article](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2); actual results here were witnessed on the pinned image.

q04 received one country-set rewrite: form unique country arrays per Work, retain international Works, generate each unordered pair once, then count. PostgreSQL's successful Work primary key proves the Work join does not multiply rows. The array-function probe and the full 325,177-row output comparison passed. q03's grace profile completed a 58.747 s primer and one 58.056 s warm execution, then failed during the next warm execution with query-log code 241 while reading an intermediate stream at the 24 GiB limit. Its stderr also contains a container-hostname DNS warning; the server query log establishes that the measured failure was the memory exception. No second performance candidate was tried for that family. Author aggregation and the richer final schema still need validation before claiming all required queries meet the target.

| Preparation scope | PostgreSQL | ClickHouse |
|---|---:|---:|
| Nine-table COPY / INSERT execution totals | 1,113.456 s | 442.471 s |
| Index creation | 2,974.801 s, 14 indexes | Reverse projection maintained during inserts/merges |
| Maintenance | VACUUM ANALYZE 453.534 s | Nine OPTIMIZE FINAL statements, 319.255 s |

These are scoped operation totals, not complete end-to-end preparation times; count checks, shared normalization, downloads and other validation add time. The shared direct download/hash/footer phase took 859.252 s. The DuckDB bulk PostgreSQL loader avoids a per-row application insertion loop, but both engines still need the shared normalization for this nine-table schema. Production incremental updates and refresh costs were not benchmarked.

All **18 completed selected native cases** match the independent raw-Athena full typed result multisets. Incomplete author and timeout cases do not receive a QA claim. An independent Python/PyArrow raw-value audit passed for 36 files, including 2,322 Works, plus dimension samples. Every normalized fragment footer was checked for selected-column NULL counts and integer ranges. All 3,572 server-copy/EC2 full source hashes and footer counts match. The verifier independently recomputed **72 completed native observations, 94 resource traces including failed/baseline/QA attempts, and all 33 timed Athena CSV fingerprints**. Fixture checks passed all eleven logical cases before the real data run. Duplicate and NULL semantics are preserved.

## Athena scan and experiment cost

{chr(10).join(scantable)}

There were 33 timed executions and six additional successful SELECT probes, with 14 DDL statements. Using a 10 MB minimum for the zero-scan SELECTs and rounding each charged query to MB gives **775.650 GB**, or **USD 3.87825 at the explicit USD 5 per decimal TB assumption**. Scan volumes vary between repetitions; the total uses each actual receipt. Complete outputs from all 39 successful SELECTs are archived locally and the timed fingerprints were reparsed.

| Cost scope | Estimated USD |
|---|---:|
| EC2, {cost['hours']:.4f} h at $0.6528/h | {cost['estimated_usd']['ec2']:.4f} |
| gp3 storage + provisioned extra IOPS/throughput | {sum(v for k,v in cost['estimated_usd'].items() if k.startswith('ebs_')):.4f} |
| Public IPv4 | {cost['estimated_usd']['public_ipv4']:.4f} |
| Athena, including probes | 3.8783 |
| Subtotal | {cost['subtotal_usd']:.4f} |
| Unreconciled S3 requests/storage/other allowance | 1.0000 |
| Estimate including allowance | **{cost['estimate_with_reserve_usd']:.2f}** |

This is an estimate, not a reconciled AWS invoice. The official Price List API supplied the EC2/gp3 rates; EBS is prorated using November's 720 hours. The estimate uses launch to verified cleanup, within the USD 25 envelope. Taxes, laptop hardware/electricity and the older retained raw EBS are excluded. The latter was explicitly preserved and continues its separate storage charge.

## Evidence, cleanup and remaining limits

At **{cleanup['at']}**, the instance was terminated and both ephemeral EBS volumes were verified absent. The private bucket, Athena workgroup, Glue database, expiry schedule, security group, instance profile and both study IAM roles were deleted and checked absent. The previous retained volume `vol-039919b5eb12aeb46` remains present. No study compute or temporary bucket remains running.

The [result directory](../results/ec2-200m-2026-11-12/) contains the selected-case summaries, scan receipts, exact cleanup checks and frozen-evidence manifest. The full frozen archive has 10,928 hashed files and excludes raw datasets, database files and credentials; its archive SHA256 is `2f0127b9df11c4450ac8ad39d12b49e4b42bc094da10dac626295a3118467f53`. [Experiment source and executed SQL](../experiments/ec2-200m/) preserve the original and selected profiles. The wider final schema, full-corpus latency and production update validation remain pending.

The external review did not complete. DeepSeek v4.1 Flash and GLM 5.3 Flash through the prescribed opencode CLI at max effort both returned the personal key's hard USD100/100 total-quota error, without a reset. Claude Code was excluded for PostgreSQL by the user, and no company credits were used. [Exact commands and failure status](../results/ec2-200m-2026-11-12/review-status.json) are retained. This draft makes no completed external-review claim and the PR has not been merged.
'''
assert '—' not in text
OUT.write_text(text)
print('Report bytes',len(text.encode()),'completed output checks',len(verify['completed_full_output_checks']))
