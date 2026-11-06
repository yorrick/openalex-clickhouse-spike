"""Generate human comparison tables directly from persisted measured evidence."""
from pathlib import Path
from statistics import median
import json
from analyze_series import main as analyze
from export_report import main as export,REPO,REPORT,DEST,HERE

GIB=2**30

def cases(data,q):return [v for k,v in data['cases'].items() if k[:3]==q]
def max_med(data,q,key):
 values=[]
 for c in cases(data,q):
  samples=[r.get(key) for r in c['resources']]
  if len(samples)!=3 or any(v is None for v in samples):return None
  values.append(median(samples))
 return max(values) if values else None
def max_peak(data,q,key):
 values=[r.get(key) for c in cases(data,q) for r in c['resources']]
 return max(values) if values and all(v is not None for v in values) else None
def num(value,scale=1,digits=2):
 if value is None:return 'n/a'
 if scale==GIB and 0<value/scale<.005:return '<0.01'
 return f'{value/scale:.{digits}f}'

def validate_analysis(analysis):
 expected={'q01','q02','q03','q04','q07'}|{q+'-s'+str(seed) for q in ('q05','q06') for seed in (51557542,24222542,2003585639)}
 comparisons=0
 for tier in ('stage2_small','stage2_medium','stage2_large'):
  d=analysis['tiers'][tier]
  if d['state']!='complete' or d['athena_all_matched'] is not True or d['merges_quiescent'] is not True or set(d['cases'])!=expected:raise RuntimeError('Tier evidence incomplete: '+tier)
  for name,c in d['cases'].items():
   if c['status'] not in ('PASS','FAIL_LATENCY') or c['qa_matched'] is not True or len(c['warm_seconds'])!=3 or len(c['resources'])!=3 or len(c['athena_runs'])!=3 or any(r.get('matched') is not True for r in c['athena_runs']):raise RuntimeError('Case evidence incomplete: '+tier+'/'+name)
   comparisons+=len(c['athena_runs'])
 if comparisons!=99:raise RuntimeError('Expected exactly99 validated comparisons')
 return comparisons
def fmt(v):return f'{v:.3f}'
def percent(v):
 if v is None:return 'n/a'
 return '<0.001%' if 0<v<.00001 else f'{v*100:.3f}%'

def main():
 analyze();analysis=json.loads((HERE/'series-analysis.json').read_text());validate_analysis(analysis)
 export()
 datasets={t:json.loads((DEST/(t+'.json')).read_text()) for t in ('stage2_small','stage2_medium','stage2_large')}
 # Golden assertions protect narrative rounding from silently stale prose.
 assert [round(d['cases']['q02']['median_seconds'],3) for d in datasets.values()]==[.657,15.990,65.512]
 assert all(c['max_seconds']<60 for t,d in datasets.items() if t!='stage2_large' for c in d['cases'].values())
 assert all(c['max_seconds']<25 for k,c in datasets['stage2_large']['cases'].items() if k!='q02')
 assert round(datasets['stage2_large']['cases']['q02']['min_seconds'],3)==65.153
 assert round(datasets['stage2_large']['cases']['q02']['max_seconds'],3)==66.142
 assert round(max_med(datasets['stage2_large'],'q02','average_cpu_cores'),1)==4.8
 assert round(max_peak(datasets['stage2_large'],'q02','query_peak_bytes')/GIB,1)==4.1
 for d in datasets.values():
  c2=d['cases']['q02']['cold_resources'];c3=d['cases']['q03']['cold_resources']
  assert c3['physical_read_bytes']>c2['physical_read_bytes']
  assert c3['io_stall_fraction']>c2['io_stall_fraction']
  assert max(r['physical_read_bytes'] for r in d['cases']['q03']['resources'])<2**20
 assert max(r['spill_compressed_bytes'] for r in datasets['stage2_small']['cases']['q02']['resources'])==0
 medium_first=datasets['stage2_medium']['cases']['q02']['resources'][0]
 assert round(medium_first['external_join_compressed_bytes']/1e9,3)==.785 and medium_first['external_aggregation_compressed_bytes']==0
 assert 17<max(max_med(d,q,'average_cpu_cores') for d in datasets.values() for q in ('q01','q02','q03','q04','q05','q06','q07'))<17.5
 assert round(max_med(datasets['stage2_large'],'q03','average_cpu_cores'),1)==4.3
 assert round(max_med(datasets['stage2_large'],'q04','average_cpu_cores'),1)==1.9
 assert 15.5<max_med(datasets['stage2_large'],'q07','average_cpu_cores')<16.5
 assert round(max_med(datasets['stage2_large'],'q02','physical_write_bytes_s')/2**20)==24
 cold= datasets['stage2_large']['cases']['q03']['cold_resources']
 assert round(cold['physical_read_bytes']/1e9,2)==3.12 and round(cold['io_stall_fraction']*100,1)==11.5
 fixed=sum(int(r['bytes']) for r in datasets['stage2_large']['table_bytes'] if r['table'] in ('authors','institutions','sources','topics'))
 extrapolated=fixed+(datasets['stage2_large']['normalized_bytes']-fixed)*510372821/31885241
 assert round(extrapolated/1e9)==60
 assert round(max(r['query_peak_bytes'] for c in datasets['stage2_large']['cases'].values() for r in c['resources'])/GIB,1)==6.3
 local=json.loads((REPO/'results/aws-small-2026-11-06/local-baseline.json').read_text())
 names={'q01':'Publication counts','q02':'Topic statistics','q03':'Author output','q04':'International collaboration','q05':'One-hop citations','q06':'Two-hop citations','q07':'Citations by year'}
 rows=[];volume=[];resource=[];cold=[];storage=[]
 for tier,d in datasets.items():
  n=d['work_records'];label=f'{n/1e6:.2f}m'
  volume.append(f"| {n:,} | {d['percent_full_works']:.3f}% | {d['works_raw_bytes']/1e9:.3f} | {d['selected_raw_bytes']/1e9:.3f} | {d['normalized_bytes']/1e9:.3f} | {d['load_dimensions_seconds']:.1f} / {d['load_works_seconds']:.1f} s | ${d['athena_scan_cost_usd_all_checks']:.4f} |")
  for q,name in names.items():
   cc=cases(d,q);ch=max(c['median_seconds'] for c in cc);ath=max(c['athena_median_seconds'] for c in cc);worst=max(c['max_seconds'] for c in cc)
   scan=max(max(c['athena_scan_bytes']) for c in cc)/1e9
   rows.append(f"| {label} | {q}: {name} | {local['tiers'][tier]['warm_sequential_queries'][q]['median_seconds']:.3f} | {ch:.3f} | {worst:.3f} | {ath:.3f} | {scan:.3f} | {'FAIL <60 s' if worst>=60 else 'PASS <60 s'} |")
   cpu=max_med(d,q,'average_cpu_cores');query=max_peak(d,q,'query_peak_bytes');anon=max_peak(d,q,'container_sampled_peak_anon_bytes');file=max_peak(d,q,'container_sampled_peak_file_bytes')
   rd=max_med(d,q,'physical_read_bytes_s');wr=max_med(d,q,'physical_write_bytes_s');iops=max_med(d,q,'physical_iops');wait=max_med(d,q,'physical_await_ms');stall=max_med(d,q,'io_stall_fraction');throttle=max_peak(d,q,'container_throttled_cpu_seconds')
   cpulabel='n/a' if cpu is None else f'{cpu:.2f} ({cpu/18*100:.1f}%)'
   resource.append(f"| {label} | {q} | {cpulabel} | {num(query,GIB)} | {num(anon,GIB)} / {num(file,GIB)} | {num(rd,2**20)} / {num(wr,2**20)} | {num(iops,digits=1)} / {num(wait)} | {percent(stall)} | {num(throttle,1,3)} |")
   if q in ('q02','q03','q04','q07'):
    c=cc[0];r=c['cold_resources'];cold.append(f"| {label} | {q} | {c['cold_seconds']:.3f} | {r['physical_read_bytes']/1e9:.3f} | {r['physical_read_bytes_s']/2**20:.1f} | {r['io_stall_fraction']*100:.1f}% |")
  for table in d['table_bytes']:
   storage.append(f"| {label} | {table['table']} | {int(table['rows']):,} | {int(table['bytes'])/1e9:.3f} |")
 text='''# Single-user resource benchmark results

## Summary, matched local and AWS inputs (2026-11-06)

The three requested volumes are complete: **2,002,982, 10,109,733 and
31,885,241 Works**, with **99 of 99 repeated ClickHouse/Athena output comparisons
matching exactly**. This is seven query families and three fixed seeds for each
of the two graph families, each repeated three times per tier. All seven
families pass the 60-second warm target at 2m and 10m. At 31.89m, baseline topic
statistics (q02) takes **65.153-66.142 seconds**; every other baseline case stays
below 25 seconds. These are single-user measurements, not concurrency capacity.

The slow topic query uses about **4.8 of the 18 allocated CPU cores on average**,
with about **4.1 GiB peak query memory**. It performs external join and aggregation work but has
very little physical I/O wait. Other queries use up to about 16-17 cores.
This points to query/settings experiments before buying more CPUs; it does not
prove that five CPUs would deliver the same latency. Full OpenAlex has not been
loaded, and neither a full-corpus one-minute target nor a need for a cluster has
been established.

### Resources, input volume and cost

Every matched AWS tier used a fresh **m7g.8xlarge, 32 vCPU / 128 GiB**, with
ClickHouse in Docker limited to **18 CPUs / 50 GiB**. Query settings were 18
threads, 12 GiB query memory, 4 GiB external group/sort thresholds and auto joins.
The writable disk was **400 GiB encrypted gp3, 3,000 IOPS / 500 MiB/s**, shared
with the guest OS, with no additional Docker disk throttle. The host EBS baseline
is 1,250 MB/s / 40,000 IOPS, so the provisioned volume is the lower throughput cap.
The separate retained source disk is **120 GiB gp3 / 3,000 IOPS / 125 MiB/s**,
read-only during benchmarks. Its ongoing cost is approximately **$9.60/month**.

| Works | Fraction of full Works | Works input GB | All selected raw GB | Active CH GB | Dimension / Works load | Athena scans, all checks |
|---:|---:|---:|---:|---:|---:|---:|
'''+ '\n'.join(volume)+'''

GB means decimal bytes / 10^9; GiB and MiB are binary. All tiers include the
complete **119,129,660 Authors (52.770 GB compressed)** and the complete
institutions, sources and topics, in addition to their nested Works subset.
The full June 26 snapshot contains **510,372,821 Works**, **630,105,216 records
across entities**, and **778.039 GB compressed Parquet**. The 31.89m tier is
**6.247% of Works and 12.635% of all raw bytes**, not a uniform random sample.
ClickHouse stores only the selected benchmark columns and normalized relations,
so the reduction from raw bytes reflects field projection as well as compression.
The source disk always holds the 98.302 GB largest cohort; smaller logical
cohorts use subsets of its files. Dimension load time is fixed because the
119m Author rows are loaded each time.

Costs in the last column cover raw-input probes, the CSV/type control and all
comparison repeats, not just the published query times. Scan fees are conservative
estimates using $5 per 10^12 scanned bytes, per-statement MB rounding and a 10 MB
minimum, not an invoice. S3, compute and storage are additional. The full temporary
experiment cost and cleanup evidence are in the cost section below.

### Performance: local, EC2 and Athena

Seconds. Local values are historical medians of five warm sequential runs.
New ClickHouse values are server query_log medians of three round-robin warm
FORMAT Null runs following one primer, with separate JSON output validation.
Athena values are medians of three engine-3 TotalExecutionTime measurements,
including queue/planning/service time but excluding CSV fetching; result reuse
is disabled. For graph families, each displayed value is the maximum across the
three fixed seeds; per-seed results are in the evidence JSON. Maxima are observed
values, not p95 estimates. Every displayed case matched Athena on all three repeats.

| Works | Query family | Local median s | EC2 median s | EC2 max s | Athena median s | Athena scan GB/run, max | EC2 warm target |
|---|---|---:|---:|---:|---:|---:|---|
'''+ '\n'.join(rows)+'''

The input Parquet and normalized-table SHA256 hashes match the historical local
runs at all three tiers. Both use the ARM64 ClickHouse tag 26.3.12.3, but the
resolved OCI ARM manifest and image config differ. Therefore this is an
input-matched operational comparison, not an isolated hardware A/B. The old
2m local author-query anomaly has no established cause. Graph seeds differ
from historical local runs, and new q07 adds a deterministic final tie-break
for equal output keys; treat those local comparisons as contextual.

### Actual CPU, memory and disk use

CPU is query user+system CPU seconds divided by server elapsed seconds, shown
as **average busy cores and percent of the 18-CPU allocation**. It is not an
instantaneous maximum. Per-family CPU and I/O values are the median of three
runs (maximum seed median for graph families); memory columns are maximum
observed peaks. Query memory comes from query_log. Container anonymous memory
and file cache (including state inherited from earlier queries) are separately sampled nominally every 0.5 seconds; their separate maxima
need not occur together and must not be added. Missing historical local CPU/I/O
measurements remain unavailable; no smaller tiers were rerun to fill gaps.

| Works | Query | CPU cores (% of 18) | Peak query GiB | Container anon / file-cache peaks GiB | Host read / write MiB/s | Host IOPS / await ms | Container I/O stall | CPU throttle s, max |
|---|---|---:|---:|---:|---:|---:|---:|---:|
'''+ '\n'.join(resource)+'''

Physical I/O is sampled from /proc/diskstats across all host NVMe devices during
the client execution window. It can include OS activity and delayed writeback
from earlier work, particularly for very short queries. Zero warm physical reads
means cached reads; ClickHouse still reads logical rows and bytes. Device await
is weighted by operation count within each run, then folded as a per-case median;
IOPS is summed across devices. A missing constituent gives n/a. PSI stall is
the fraction of wall time with at least one task stalled, not a fraction of all work.
NVMe busy percentage is saved but is not a reliable percentage of throughput
capacity. Complete compressed monitoring traces are published alongside the summary JSON.
Container cgroup CPU totals, CPU throttling, memory.current,
memory.stat, io.stat and pressure totals are retained with each timed run.

Active-table storage is shown below. It excludes inactive parts, temporary join
files, logs and the OS. Baseline peak filesystem occupancy was not sampled and
is explicitly unavailable. Subsequent tuning also samples scratch filesystem
occupancy. No additional runs are needed to manufacture missing measurements.

| Works | Normalized table | Records / edges | Active compressed GB |
|---|---|---:|---:|
'''+ '\n'.join(storage)+'''

### Cold guest-cache observations

One cache-cleared observation per case, with ClickHouse caches and the Linux
page cache dropped before each query, follows the warm series. EBS backend
caches are outside this control. These are observations, not cold-run medians.
Cold q03 has more physical reads and I/O pressure than cold q02; its warm
observations have essentially no physical reads.

| Works | Query | Cold s | Physical read GB | Read MiB/s | Container I/O stall |
|---|---|---:|---:|---:|---:|
'''+ '\n'.join(cold)+'''

### Scaling and sizing conclusions

For the last 3.15-fold increase in Works, q03 grows about 3.14-fold and q07
about 3.05-fold, broadly proportional over that interval; q04 grows about
4.25-fold. One-hop lookups stay around 3-4 milliseconds for the fixed seeds.
These three volumes and non-random nested shards do not establish a universal
scaling law, and fixed-seed graph results do not describe every possible seed.

The q02 median grows **0.657 -> 15.990 -> 65.512 seconds**, for Works multipliers
of 5.05 and 3.15. Its time multipliers are about 24.3 and 4.10. External join
processing appears at 10m: about 0.785 GB compressed versus zero at 2m.
At 31.89m, compressed external processing totals about 2.67 GB in warm1, split
into about 2.20 GB of joins and 0.47 GB of aggregation in warm1. This is a change in execution
regime, so a single linear fit would be misleading. The precise trigger was not
isolated. In particular, the external group-by threshold must not be described
as the proven trigger for external join work.

At 31.89m, q02 averages 4.8 cores, q03 about 4.3 and q04 about 1.9; q07 uses
about 16 cores. More provisioned CPU alone is not an established fix for the
slower join families. Warm q02 writes roughly 24 MiB/s on average and its I/O
stall is tiny, well below the 500 MiB/s provisioned throughput. In the cold observations,
q03 reads about 3.12 GB and spends about 11.5% of its monitoring window in
I/O pressure. Disk reads contribute to cold author-query latency; disk throughput was
not varied and a minimum required EBS bandwidth was not measured.

All baseline warm cases except q02 at 31.89m met the single-user target under
the tested settings. The q02 miss is not attributed to the container limit. Peak query memory across the baseline is about 6.3 GiB,
but this is not a minimum container RAM estimate: the container also uses
anonymous server memory and tens of GiB of reclaimable file cache. CPU count,
container RAM and disk bandwidth were not independently swept, so no minimum
resource configuration is established by this study.

Full-corpus deployment remains an extrapolation. Holding the complete Authors
and support dimensions fixed, linearly scaling just the Works-derived normalized
tables from 31.89m to 510.37m gives about **60 GB active selected-column data**.
This excludes unused source fields, temporary processing space, inactive parts,
logs, replicas and distribution differences. This arithmetic does not establish
full-corpus storage capacity, query memory or latency. A single instance is
still a candidate; a second node or a cluster is not yet
justified by these measurements. The current 31.89m timings do not establish a
one-minute SLA on 16 times as many Works.

### Data provenance and reproducibility

All 2,771 historical files were recovered from public OpenAlex S3 version
history. A private server-side S3 copy provides an immutable Athena cohort;
EC2 downloads the same pinned versions directly from OpenAlex onto retained EBS.
Every full-object server SHA256 matches the original cached fingerprint, and
EC2 verified incoming and filesystem-readback SHA256 plus Parquet footer counts.
The direct download took **23.38 minutes**. The final raw data paths stay within
AWS. An earlier laptop upload attempt was stopped and its partial source bucket
removed; it is not an input to these results.

The raw source volume is mounted block read-only and ext4 ro,noload, then bound
read-only to Docker, with EROFS verified on a write attempt. ClickHouse writes
only to separate scratch storage. Each tier starts with a fresh guest and fresh
ClickHouse data directory, waits for merges to become quiescent, then stops
merges before timing. Query-log duration excludes post-query SYSTEM FLUSH LOGS.
The code commit deployed to guests is 0b3d5bcfbb5062aca4d26ae5f813c4659a234b5d.
Graph seeds 51557542, 24222542 and 2003585639 were preregistered on eligible 2m
vertices near outgoing-degree p50/p90/p99 and held fixed across tiers.

Athena uses manifest-selected private S3 Parquet files and independent SQL
normalization views, including the full Authors table. Exact file/count/decode
probes precede each tier. Equality checks compare complete typed multisets,
preserving duplicates, NULL versus empty string, booleans and 64-bit integers.
This validates query outputs in the selected fields, not every OpenAlex field
or all conceivable bibliometric definitions. Athena scans only projected
Parquet columns but may read the whole selected cohort for broad aggregations;
these are explicit manifests rather than a partition-pruning performance test.

Measured evidence: [executed SQL](../../results/aws-scaling-2026-11-06/queries.json),
[input-file versions and fingerprints](../../results/aws-scaling-2026-11-06/input-files.json),
[input proof](../../results/aws-scaling-2026-11-06/input-proof.json),
[2m](../../results/aws-scaling-2026-11-06/stage2_small.json),
[10m](../../results/aws-scaling-2026-11-06/stage2_medium.json),
[31.89m](../../results/aws-scaling-2026-11-06/stage2_large.json).
The immutable historical local runs remain in results/stage2-single-memory50-cpu18
and the instrumented repeatability result directories. Earlier reports treated
an absent spill counter as zero; those old no-spill claims are unverified. This
series checks that ExternalProcessingCompressedBytesTotal is supported before
interpreting its value, and preserves raw ProfileEvents.

Price/meter definitions: [Athena pricing](https://aws.amazon.com/athena/pricing/),
[gp3 performance](https://docs.aws.amazon.com/ebs/latest/userguide/general-purpose.html),
[ClickHouse query_log](https://clickhouse.com/docs/reference/system-tables/query_log).
'''
 tuning=json.loads((DEST/'q02-tuning.json').read_text())
 successful=[(k,v) for k,v in tuning['cases'].items() if v['report_target_outcome']=='PASS' and k not in ('original_a','original_b')]
 if successful:
  best_name,best=min(successful,key=lambda kv:kv[1]['median_seconds'])
  prefix=f"A focused follow-up brings q02 to **{best['median_seconds']:.3f} seconds** on the same 18 CPU / 50 GiB container, with exact output equality. See the tuning table for the settings and memory/CPU trade-offs.\n\n"
  text=text.replace('The slow topic query uses',prefix+'In the baseline, the slow topic query uses',1)
 for extra in ('tuning-report.md','cost-report.md'):
  if not (HERE/extra).exists():raise RuntimeError('Required final report section missing: '+extra)
  text+='\n'+(HERE/extra).read_text()
 text+='\nEarlier pilot and local repeatability detail: [frozen pre-scaling report](2026-08-05-single-user-resource-benchmark-history.md).\n'
 REPORT.write_text(text)
 print('generated_report_bytes',len(text.encode()))

if __name__=='__main__':main()
