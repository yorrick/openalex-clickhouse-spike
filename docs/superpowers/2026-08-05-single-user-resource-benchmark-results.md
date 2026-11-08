# Single-user resource benchmark results

[Interactive results diagram, created by Claude Code](https://chatgpt.com/space/page_6f224aabf09881919eef15f7eea7dd9c).

## Summary, matched local and AWS inputs (2026-11-06)

The three requested volumes are complete: **2,002,982, 10,109,733 and
31,885,241 Works**, with **99 of 99 repeated ClickHouse/Athena output comparisons
matching exactly**. This is seven query families and three fixed seeds for each
of the two graph families, each repeated three times per tier. All seven
families pass the 60-second warm target at 2m and 10m. At 31.89m, baseline topic
statistics (q02) takes **65.153-66.142 seconds**; every other baseline case stays
below 25 seconds. These are single-user measurements, not concurrency capacity.

A focused follow-up brings q02 to **5.640 seconds** with forced parallel_hash, a 24 GiB query-memory limit and 8 GiB spill thresholds, on the same 18 CPU / 50 GiB container. The SQL rewrite, output-identical on this cohort, reaches **9.258 seconds** under the original 12 / 4 GiB query settings. Both match all output rows.

In the baseline, the slow topic query uses about **4.8 of the 18 allocated CPU cores on average**,
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
| 2,002,982 | 0.392% | 3.254 | 56.323 | 3.619 | 31.3 / 22.0 s | $0.1045 |
| 10,109,733 | 1.981% | 15.118 | 68.187 | 4.501 | 31.5 / 77.0 s | $0.2788 |
| 31,885,241 | 6.247% | 45.233 | 98.302 | 6.890 | 31.7 / 205.2 s | $0.7241 |

GB means decimal bytes / 10^9; GiB and MiB are binary. All tiers include the
complete **119,129,660 Authors (52.770 GB compressed)** and the complete
institutions, sources and topics, in addition to their nested Works subset.
The full June 26 snapshot contains **510,372,821 Works**, **630,105,216 records
across entities**, and **778.039 GB compressed Parquet**. The all-entity record
total includes **187,148 records in 15 additional support-entity types**. Those
support files are cached, while the benchmark loads the five core entities and
their normalized relations; this difference is not a normalization row loss. The 31.89m tier is
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
including queue/planning/service time and S3 result materialization but excluding CSV fetching; result reuse
is disabled. For graph families, each displayed value is the maximum across the
three fixed seeds; per-seed results are in the evidence JSON. Maxima are observed
values, not p95 estimates. Every displayed case matched Athena on all three repeats. Athena materializes
results to S3 while ClickHouse FORMAT Null discards timed output; together with
raw versus normalized storage, this prevents an isolated engine-only comparison.

| Works | Query family | Local median s | EC2 median s | EC2 max s | Athena median s | Athena scan GB/run, max | EC2 warm target |
|---|---|---:|---:|---:|---:|---:|---|
| 2.00m | q01: Publication counts | 0.060 | 0.018 | 0.019 | 4.345 | 0.020 | PASS <60 s |
| 2.00m | q02: Topic statistics | 1.363 | 0.657 | 0.659 | 5.617 | 0.085 | PASS <60 s |
| 2.00m | q03: Author output | 33.630 | 1.042 | 1.068 | 148.720 | 3.312 | PASS <60 s |
| 2.00m | q04: International collaboration | 1.109 | 0.755 | 0.765 | 10.922 | 0.966 | PASS <60 s |
| 2.00m | q05: One-hop citations | 0.011 | 0.003 | 0.004 | 5.060 | 0.202 | PASS <60 s |
| 2.00m | q06: Two-hop citations | 0.200 | 0.021 | 0.021 | 5.430 | 0.202 | PASS <60 s |
| 2.00m | q07: Citations by year | 2.502 | 0.182 | 0.188 | 5.521 | 0.178 | PASS <60 s |
| 10.11m | q01: Publication counts | 0.027 | 0.035 | 0.036 | 14.352 | 0.102 | PASS <60 s |
| 10.11m | q02: Topic statistics | 10.780 | 15.990 | 16.193 | 13.757 | 0.435 | PASS <60 s |
| 10.11m | q03: Author output | 2.978 | 5.619 | 5.775 | 135.099 | 5.136 | PASS <60 s |
| 10.11m | q04: International collaboration | 2.512 | 5.706 | 5.731 | 14.325 | 4.545 | PASS <60 s |
| 10.11m | q05: One-hop citations | 0.007 | 0.004 | 0.004 | 13.964 | 0.909 | PASS <60 s |
| 10.11m | q06: Two-hop citations | 0.103 | 0.055 | 0.055 | 13.357 | 0.909 | PASS <60 s |
| 10.11m | q07: Citations by year | 1.250 | 1.620 | 1.851 | 12.803 | 0.824 | PASS <60 s |
| 31.89m | q01: Publication counts | 1.538 | 0.076 | 0.077 | 36.338 | 0.317 | PASS <60 s |
| 31.89m | q02: Topic statistics | 65.285 | 65.512 | 66.142 | 43.261 | 1.321 | FAIL <60 s |
| 31.89m | q03: Author output | 9.896 | 17.630 | 17.684 | 130.395 | 9.834 | PASS <60 s |
| 31.89m | q04: International collaboration | 11.465 | 24.270 | 24.312 | 36.921 | 13.755 | PASS <60 s |
| 31.89m | q05: One-hop citations | 0.011 | 0.004 | 0.004 | 38.131 | 2.704 | PASS <60 s |
| 31.89m | q06: Two-hop citations | 0.322 | 0.174 | 0.174 | 39.546 | 2.704 | PASS <60 s |
| 31.89m | q07: Citations by year | 3.781 | 4.947 | 5.310 | 39.825 | 2.451 | PASS <60 s |

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
| 2.00m | q01 | 5.75 (32.0%) | 0.06 | 3.19 / 13.75 | 0.00 / 0.00 | 0.0 / n/a | 0.000% | 0.000 |
| 2.00m | q02 | 3.32 (18.5%) | 1.05 | 3.38 / 13.75 | 0.00 / 0.00 | 0.0 / n/a | 0.000% | 0.000 |
| 2.00m | q03 | 8.44 (46.9%) | 2.11 | 3.73 / 13.75 | 0.00 / 0.00 | 0.0 / n/a | <0.001% | 0.073 |
| 2.00m | q04 | 2.19 (12.1%) | 0.64 | 3.34 / 13.75 | 0.00 / 0.00 | 0.0 / n/a | 0.000% | 0.000 |
| 2.00m | q05 | 1.87 (10.4%) | <0.01 | 2.59 / 13.75 | 0.00 / 0.00 | 0.0 / n/a | 0.000% | 0.000 |
| 2.00m | q06 | 10.89 (60.5%) | 0.01 | 1.84 / 13.76 | 0.00 / 0.00 | 0.0 / n/a | 0.000% | 0.000 |
| 2.00m | q07 | 16.71 (92.8%) | 0.87 | 2.87 / 13.76 | 0.00 / 0.00 | 0.0 / n/a | 0.000% | 0.000 |
| 10.11m | q01 | 11.87 (65.9%) | 0.11 | 6.45 / 18.86 | 0.00 / 0.00 | 0.0 / n/a | 0.000% | 0.000 |
| 10.11m | q02 | 2.04 (11.3%) | 2.88 | 6.45 / 19.56 | 0.00 / 0.60 | 4.2 / 2.43 | <0.001% | 0.000 |
| 10.11m | q03 | 4.70 (26.1%) | 4.15 | 5.67 / 19.16 | 0.00 / 0.40 | 3.5 / 2.55 | <0.001% | 0.029 |
| 10.11m | q04 | 1.77 (9.8%) | 2.11 | 5.05 / 18.87 | 0.00 / 1.92 | 18.5 / 2.23 | <0.001% | 0.000 |
| 10.11m | q05 | 1.39 (7.7%) | <0.01 | 3.50 / 18.88 | 0.00 / 0.00 | 0.0 / n/a | 0.000% | 0.000 |
| 10.11m | q06 | 16.06 (89.2%) | 0.01 | 1.76 / 18.88 | 0.00 / 0.00 | 0.0 / n/a | 0.000% | 0.000 |
| 10.11m | q07 | 16.29 (90.5%) | 5.95 | 7.70 / 19.33 | 0.00 / 0.00 | 0.0 / n/a | 0.000% | 0.204 |
| 31.89m | q01 | 15.22 (84.5%) | 0.11 | 4.78 / 32.58 | 0.00 / 0.00 | 0.0 / n/a | 0.000% | 0.000 |
| 31.89m | q02 | 4.79 (26.6%) | 4.09 | 7.35 / 34.55 | 0.00 / 24.26 | 111.9 / 2.97 | <0.001% | 0.000 |
| 31.89m | q03 | 4.31 (23.9%) | 4.22 | 6.29 / 33.70 | 0.00 / 0.28 | 2.2 / 2.58 | <0.001% | 0.627 |
| 31.89m | q04 | 1.93 (10.7%) | 4.51 | 6.48 / 32.59 | 0.00 / 0.57 | 4.3 / 2.45 | <0.001% | 0.000 |
| 31.89m | q05 | 2.04 (11.3%) | <0.01 | 5.68 / 32.57 | 0.00 / 0.00 | 0.0 / n/a | 0.000% | 0.000 |
| 31.89m | q06 | 17.32 (96.2%) | 0.01 | 2.79 / 32.57 | 0.00 / 0.00 | 0.0 / n/a | 0.000% | 0.001 |
| 31.89m | q07 | 16.17 (89.8%) | 6.32 | 10.72 / 33.88 | 0.00 / 1.00 | 6.4 / 2.71 | <0.001% | 0.454 |

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
| 2.00m | authors | 119,129,660 | 3.349 |
| 2.00m | citation_edge | 15,283,016 | 0.108 |
| 2.00m | institutions | 127,784 | 0.004 |
| 2.00m | sources | 283,287 | 0.011 |
| 2.00m | topics | 4,516 | 0.000 |
| 2.00m | work_author | 3,852,081 | 0.041 |
| 2.00m | work_institution | 2,646,224 | 0.024 |
| 2.00m | work_topic | 4,139,113 | 0.039 |
| 2.00m | works | 2,002,982 | 0.044 |
| 10.11m | authors | 119,129,660 | 3.349 |
| 10.11m | citation_edge | 70,415,984 | 0.462 |
| 10.11m | institutions | 127,784 | 0.004 |
| 10.11m | sources | 283,287 | 0.011 |
| 10.11m | topics | 4,516 | 0.000 |
| 10.11m | work_author | 16,075,482 | 0.159 |
| 10.11m | work_institution | 12,517,247 | 0.101 |
| 10.11m | work_topic | 21,657,004 | 0.202 |
| 10.11m | works | 10,109,733 | 0.214 |
| 31.89m | authors | 119,129,660 | 3.349 |
| 31.89m | citation_edge | 208,787,187 | 1.524 |
| 31.89m | institutions | 127,784 | 0.004 |
| 31.89m | sources | 283,287 | 0.011 |
| 31.89m | topics | 4,516 | 0.000 |
| 31.89m | work_author | 51,816,498 | 0.465 |
| 31.89m | work_institution | 39,499,697 | 0.300 |
| 31.89m | work_topic | 64,589,578 | 0.591 |
| 31.89m | works | 31,885,241 | 0.646 |

### Cold guest-cache observations

One cache-cleared observation per case, with ClickHouse caches and the Linux
page cache dropped before each query, follows the warm series. EBS backend
caches are outside this control. These are observations, not cold-run medians.
Cold q03 has more physical reads and I/O pressure than cold q02; its warm
observations have essentially no physical reads.

| Works | Query | Cold s | Physical read GB | Read MiB/s | Container I/O stall |
|---|---|---:|---:|---:|---:|
| 2.00m | q02 | 0.694 | 0.038 | 42.0 | 0.4% |
| 2.00m | q03 | 5.847 | 2.562 | 406.9 | 61.0% |
| 2.00m | q04 | 0.809 | 0.022 | 21.8 | 0.4% |
| 2.00m | q07 | 0.221 | 0.096 | 239.6 | 1.8% |
| 10.11m | q02 | 16.367 | 0.202 | 11.5 | 0.2% |
| 10.11m | q03 | 9.984 | 2.717 | 255.5 | 31.2% |
| 10.11m | q04 | 5.737 | 0.094 | 15.2 | 0.2% |
| 10.11m | q07 | 1.912 | 0.427 | 196.8 | 1.7% |
| 31.89m | q02 | 66.537 | 0.555 | 7.9 | 0.1% |
| 31.89m | q03 | 21.459 | 3.121 | 137.6 | 11.5% |
| 31.89m | q04 | 24.519 | 0.297 | 11.4 | 0.1% |
| 31.89m | q07 | 5.378 | 1.291 | 221.9 | 1.5% |

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
The [field inventory](../openalex-field-inventory.md) catalogues the saved benchmark
schemas and maps the fields and relationships preserved by this estimate.
The estimate excludes unused source fields, temporary processing space, inactive parts,
logs, replicas and distribution differences. This arithmetic does not establish
full-corpus storage capacity, query memory or latency. A single instance is
still a candidate; a second node or a cluster is not yet
justified by these measurements. The current 31.89m timings do not establish a
one-minute SLA on 16 times as many Works.

As arithmetic, not a prediction, uniform scaling by a factor of 16 would require no more
than about **3.75 seconds** at 31.89m to meet 60 seconds at full volume. The q02
fixes, q03, q04 and q07 exceed that starting time; uniform scaling of the 13.28 GiB
hash-arm peak would be **over 210 GiB**, above this 128 GiB host. Fixed dimensions,
group cardinalities, plans and caching make such proportional assumptions
uncertain. A full-corpus one-minute configuration therefore depends on further
tuning and potentially more memory/CPU; the present study does not choose a
single larger host or a cluster.

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
The repository snapshot deployed to all four ClickHouse benchmark and tuning guests is
0b3d5bcfbb5062aca4d26ae5f813c4659a234b5d. Benchmark and tuning guest payloads
are archived separately; the tuning payload SHA256 is
2981b06a0a9333227505f16edd602409634d486b64dbf0ec0f8cd02adde6ae9a,
extracted from deployed user data and verified byte-identical.
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

## Focused q02 tuning, 31.89 million Works

This follow-up keeps the **18 CPU / 50 GiB container, same Ubuntu AMI and OCI
image, input identity, normalized-table hash and 400 GiB gp3 disk**. It tests a
24 GiB query-memory / 8 GiB spill-threshold bundle, then forced parallel_hash
with that bundle, and a SQL rewrite under the original 12 / 4 GiB
query settings. The rewrite aggregates numeric topic IDs before joining names. It is output-identical
on the full tested cohort and the three-Work fixture; topic-ID uniqueness was verified.
All 838,464 output rows must hash to the baseline result independently validated
by Athena. Original-SQL controls bracket the variants. A three-Work native
preflight exercised all five cases, settings, telemetry and typed QA before the
large load. No smaller cohort was rerun and no new Athena scans were needed.

| Arm | Query memory / spill threshold, join | Three warm seconds | CPU cores, median | Peak query GiB | Host write MiB/s, median | Compressed external GB, median | Sampled root occupancy GB, max | Target result |
|---|---|---|---:|---:|---:|---:|---:|---|
| original_a | 12 / 4 GiB, auto | 65.521, 64.889, 66.232 | 5.06 | 4.06 | 17.26 | 2.674 | 27.84 | FAIL_LATENCY |
| memory24 | 24 / 8 GiB, auto | 65.983, 64.905, 64.725 | 5.01 | 4.85 | 18.10 | 2.204 | 25.80 | FAIL_LATENCY |
| parallel_hash24 | 24 / 8 GiB, parallel_hash | 5.640, 5.660, 5.633 | 16.18 | 13.28 | 0.84 | 0.598 | 13.95 | PASS |
| preaggregate12 | 12 / 4 GiB, auto | 9.248, 9.300, 9.258 | 6.57 | 3.74 | 0.34 | 0.000 | 12.29 | PASS |
| original_b | 12 / 4 GiB, auto | 65.033, 65.796, 64.994 | 4.83 | 4.04 | 23.49 | 2.678 | 14.56 | FAIL_LATENCY |

The original guest policy allowed a 1.20 control-median ratio. External review
pointed out that this exceeds the roughly 8% baseline-to-target gap. A stricter
**1.08 ratio** was recorded at **2026-11-06T21:47:10.609453+00:00**, after launch and
before observing any large-cohort variant or closing-control results. This is
a disclosed secondary analysis rule; the original policy, guest outcomes and
measurements are preserved. The measured control ratio is **1.0075**.
A report PASS requires all three observations under 60 seconds, exact QA,
verified effective settings and stable controls under the stricter rule.

Scratch occupancy is sampled root-filesystem use during timed warm windows,
including OS, logs, tables and temporary files. It depends on run order and
deletions, so these arm values cannot be compared as incremental query allocations
or used to infer minimum disk capacity. Load-phase peak occupancy is unrecorded.
Peak per-query allocation and container cache are separate in the evidence.
The memory24 arm changes both query memory and spill thresholds, so it does not
isolate the effect of RAM alone. CPU count and disk bandwidth are held fixed.
The SQL rewrite and forced join choice are experiments, not automatic fallback
behavior in the application. Original benchmark medians remain unchanged. The tuned arms have warm measurements
only; no cache-cleared or concurrent-user tuning trial was performed.

Evidence: [tuning measurements](../../results/aws-scaling-2026-11-06/q02-tuning.json)
and [full tuning trace](../../results/aws-scaling-2026-11-06/telemetry-q02-tuning.json.gz).

The query-memory/spill bundle alone has median **64.905 s**.
Changing only the join algorithm within that bundle gives **5.640 s**,
about **11.5 times faster**, using about
**16.18 cores** and **13.28 GiB peak query allocation**. The rewrite gives
**9.258 s**, about **6.57 cores** and **3.74 GiB**,
under the original query limits. Both are measured working choices for this
31.89m tier; neither required a larger CPU allocation or container RAM limit.
The rewrite is the lower-memory option, while the forced hash join is faster.
These per-query experiments do not establish smaller-container minima or full-corpus latency.

The captured settings show max_bytes_in_join=0 and
**default_max_bytes_in_join=1,000,000,000 bytes**, distinct from the 12/24 GiB
query-memory limit. The official 26.3.12.3 [JoinSwitcher source](https://github.com/ClickHouse/ClickHouse/blob/v26.3.12.3-lts/src/Interpreters/JoinSwitcher.cpp)
uses that default when no explicit join limit exists and switches from a hash
join to a merge join when exceeded. This mechanism is consistent with the
observed external-join transition and the unchanged automatic-join latency when
query memory and spill thresholds are raised together. The threshold itself was not varied, so the exact
breakpoint is not an independently validated causal measurement. The forced
hash arm still has some external aggregation; it must not be called spill-free.

## Costs and teardown

The conservative temporary experiment total is **US$3.52**, below the
approved US$15 envelope. This includes **US$1.10746** of estimated Athena
scan fees across **221.492 GB** of rounded statements, and a full
**US$1 allowance** for requests, S3 copies/storage, returned results, CPU credits,
minor boundary timing and the earlier US$0.081 pilot. This is a rate-based
estimate with an unmetered allowance, not a proven invoice upper bound; credits and tax are excluded.

| Run | Instance | Bounded lifetime | EC2 upper | Scratch upper | Public IPv4 upper |
|---|---|---:|---:|---:|---:|
| source preparation/probe | t4g.small | 2.63 min | $0.0007 | $0.0001 | $0.0002 |
| source preparation/probe | t4g.small | 2.60 min | $0.0007 | $0.0001 | $0.0002 |
| source preparation/probe | t4g.small | 26.08 min | $0.0073 | $0.0008 | $0.0022 |
| small baseline | m7g.8xlarge | 5.60 min | $0.1218 | $0.0060 | $0.0005 |
| medium baseline | m7g.8xlarge | 8.96 min | $0.1949 | $0.0096 | $0.0007 |
| large baseline | m7g.8xlarge | 20.21 min | $0.4399 | $0.0217 | $0.0017 |
| 31.89m q02 tuning | m7g.8xlarge | 26.16 min | $0.5692 | $0.0281 | $0.0022 |

Compute subtotal: $1.3345; temporary root EBS: $0.0663; public IPv4:
$0.0077. Bounds run from the recorded launch to the durable cleanup record,
plus 60 seconds per VM for launch-record timing. Root storage uses $0.08/GiB-month
and $0.04/additional MiB/s-month above the included 125 MiB/s; the 400 GiB / 500 MiB/s
configuration is $47/month while provisioned, prorated for these brief runs.
EC2 m7g.8xlarge is $1.3056/hour on demand; this is the host charge even though
Docker has only 18 of its 32 CPUs. Query latency alone is not the total cost of
an ephemeral run: boot, loading, priming, QA and teardown also consume time.
Keeping that host running continuously would be a different cost model.

Every study instance is terminated and all temporary root disks, security groups,
instance roles/profiles and termination schedules are removed. Athena workgroups
and Glue databases are removed. The private 98.302 GB source copy is explicitly
deleted after QA. Evidence/result buckets have seven-day expiration; public reports
and complete telemetry are also retained in Git and the local study directory.
The only intentional ongoing disk is the encrypted **120 GiB raw EBS volume**,
kept detached in us-east-1a at approximately **US$9.60/month** until explicitly
removed. Its source data remain available for future tests without laptop upload.

Details: [cost calculation](../../results/aws-scaling-2026-11-06/costs.json),
[final cleanup inventory](../../results/aws-scaling-2026-11-06/cleanup.json).
Rates: [Athena](https://aws.amazon.com/athena/pricing/),
[EBS](https://aws.amazon.com/ebs/pricing/),
[public IPv4](https://aws.amazon.com/vpc/pricing/).

## Independent review

Claude Code **claude-opus-5-5** reviewed the design, tuning and final results at
explicit **max** effort, and the resource calculations and documented corrections
at **high** effort. Initial BLOCK findings were verified and corrected or rejected
with evidence. The final max review found no numeric errors and one treatment
wording error; that was corrected, and the final high-effort correction review
returned **PASS**. All six CLI processes completed with exit0.

[Exact CLI commands and verdicts](../../results/aws-scaling-2026-11-06/review-record.json),
[finding adjudication](../../results/aws-scaling-2026-11-06/review-adjudication.md),
[final max review](../../results/aws-scaling-2026-11-06/final-review-output.md),
[correction PASS](../../results/aws-scaling-2026-11-06/final-correction-output.md).
The reviewers read supplied evidence; they did not run the tests or independently
retrieve private raw artifacts. Agent QA includes38 focused passing tests, live
native fixtures and the complete typed output comparisons described above.

Earlier pilot and local repeatability detail: [frozen pre-scaling report](2026-08-05-single-user-resource-benchmark-history.md).
