# Local DuckDB extraction and API comparison

Measured 13 November 2026 on **one 400,000-Work Parquet shard, 390,189,187 bytes**, selected by middle file size from the current manifest. Filtering publication_year=2018 yields **17,644 Works (4.411%)**. This is not a complete 2018 export, a representative sample of every shard, or an analytical DuckDB-versus-ClickHouse benchmark.

All S3 reads were anonymous. No certification account, AWS credentials, S3 Select, Athena, EC2 or S3 writes were used. The Python harness runs the embedded DuckDB engine through its API, not a database server. Actual exported Parquet values were checked independently against the raw source with PyArrow.

## Extraction results

Three fresh processes per variant; medians below time COPY execution, including reading, filtering and Parquet writing, excluding setup, later telemetry and QA. The local source was likely OS-cache resident after download; OS caches were not cleared. MB is decimal and GiB binary. GET body bytes exclude protocol overhead.

| Path and columns | Median COPY s | S3 GET body MB/run | Parquet output MB | Max process RSS GiB |
|---|---:|---:|---:|---:|
| Local ID/year | 0.0057 | 0.000 | 0.102 | 0.081 |
| S3 ID/year, default cache | 1.3008 | 4.395 | 0.102 | 0.094 |
| Local full records | 0.6461 | 0.000 | 13.526 | 0.927 |
| S3 full records, default cache | 66.9412 | 390.959 | 13.526 | 1.150 |
| S3 full records, cache disabled | 94.1902 | 494.008 | 13.526 | 0.857 |

Every case writes the same 17,644 rows. Full output retains all **51 top-level source fields / 200 physical Parquet leaves**, including nested values. Input compression is Snappy and output is ZSTD, so size ratios combine row selection and compression changes. Exact executed SQL and all settings/repeats are archived.

The initial cache-disabled setting was unnecessary with fresh processes and exaggerated overlap. The corrected default-cache arm measured **66.941 s / 390.959 MB**, versus **94.190 s / 494.008 MB** with caching disabled. The byte saving follows from less overlapping range traffic. The arms were not interleaved and network throughput changed, so the full time difference cannot be attributed to caching alone. Original results remain separately labelled. ID/year reads about 1.13% of object bytes, meeting the predeclared <=10% target. Full records read essentially the whole object, rejecting the <=25% target; default caching meets the separate follow-up <=1.02-times-object criterion.

All four row groups contain 2018 records and span centuries. Page indexes exist, so retained row-group bytes are not a universal floor for every reader. In the disabled-cache case, GET ranges cover all source bytes except its four-byte magic header, with 103.819 MB of overlapping ranges. A separate continuous per-process macOS observation received **495.857 MB**, consistent with **494.008 MB** HTTP bodies plus protocol overhead. An earlier one-shot snapshot missed prior traffic and is not used as a lifetime total; per-flow sampling also misses some short flows. Extra network observations are excluded from primary medians. The fourth narrow and full observations ran concurrently and are not comparable latency samples.

One full unsigned GetObject baseline took **104.373 s**, including streaming SHA-256, local writing and fsync. It is one observation with a different read pattern, not a repeated bandwidth comparison. Source ETag, version and size were unchanged across all phases; the raw SHA-256 was rechecked after the follow-ups. See final-qa.json and extra-qa.json in the results archive. Raw input and exported files remain in ~/work/data/openalex-duckdb-slicing-20261113, outside Git.

## One-pass year partitioning

DuckDB rewrote all **400,000 records and all source fields** into **269 publication-year partition directories** in one pass over the cached local file. The three COPY times were **3.727, 3.764 and 4.026 s**, median **3.764 s**. Total output was about **299.2 MB**; the 2018 partition is one **13.58 MB Parquet file**, containing all 17,644 matching Works. Publication year is also stored inside each file. This phase made zero HTTP requests.

Peak RSS reached **5.44 GiB** and CPU averaged **3.39 to 3.65 busy cores** with eight DuckDB threads configured. Independent QA checks every ID/year value across all three partitioned datasets, all full 2018 records in all three, and every full record in the first 400,000-row dataset. This does not size a small cloud instance or establish whole-snapshot performance. Hosted download latency, update processing, compaction and redistribution costs were not measured.

## API retrieval comparison

The API arm requested the **same 17,644 known IDs** in **177 batches of at most 100**, using gzip, four pooled connections and **0.21 s between request starts**, about 4.76 requests/s. ID discovery and cursor paging are excluded. This pacing is below the documented anonymous maximum and sets a 36.96 s floor before the final response; maximum API throughput was not measured. All returned objects were written to JSONL.

Three runs took **37.308, 37.374 and 37.218 s**, median **37.308 s**, including HTTP, gzip decoding, JSON parsing and JSONL writing. Each received about **19.33 MB** compressed and wrote **116.70 MB** JSONL. Across the three runs, **$0.0531 of the anonymous free allowance** was consumed, not paid credits or an AWS charge.

This was not equal-coverage snapshot retrieval: each run returned **15,705 rows / 15,701 distinct IDs**, including **15,232 exact original-ID matches**, **469 other returned IDs**, **2,412 original IDs absent**, and **four duplicate rows**. All batch responses were complete according to meta.count; no extra page was silently omitted. Only **15,671 rows** still report year 2018. Three individually sampled absent IDs returned 404, without establishing the cause of every missing/different ID. API objects have 52 top-level fields across the returned set and different freshness/schema from the snapshot. No full-record equality with the snapshot is claimed.

The API arm was paced by the script, while full-record S3 extraction was constrained by this host's network throughput (about 5.8 MB/s in the default-cache arm). The shorter API wall time therefore does not establish a winner for equal datasets or arbitrary query-defined exports, especially given the coverage, schema and output-format differences. It also does not measure downloading an already prepared hosted Parquet shard. Repartitioning once can reduce repeated preparation when a published layout matches the desired slice; institution/topic slices overlap and may need a different strategy. No public redistribution service was built.

## Configuration and reproducibility

Host: Apple M5 Max, 18 logical CPUs, 128 GiB physical RAM; DuckDB 2.0.0. Eight query threads and memory_limit='8GB' were configured; this is a database allocation cap, not an OS CPU/RAM quota. The parent watchdog used 12 GiB RSS / 240 s per case. Initial cases lacked an explicit temp-space cap but recorded zero spill; follow-ups set 4 GB. Physical-disk bandwidth and IOPS were not measured. CPU is process usage around COPY, not profiler operator time, which can include waiting. Per-case CPU/RAM and profile counters are archived. API peak RSS is process-lifetime, not an independent per-repeat maximum.

The Python API does not run .duckdbrc. AWS variables are stripped, config/credential paths and DuckDB secret storage are study-owned and empty, automatic credential fetching/refresh is disabled, and one empty-key S3 config with Requester Pays false is used. DuckDB HTTP logs redact some header values but retain their names. Across all 3,702 logged requests in the extraction cases, the only request-header names were user-agent, host, range and if-match, with no Authorization or SigV4 x-amz headers; runtime inspection selected only that nonpersistent anonymous config. SQL uses s3:// paths; S3 itself uses HTTPS transport.

[Executed scripts and SQL](../experiments/duckdb-extraction-2026-11-13/) are throwaway study artifacts, not production exporters. [Compact results and receipts](../results/duckdb-extraction-2026-11-13/) preserve inputs, hashes and repeat scopes. Raw records and private local network addresses remain outside Git. No raw data was uploaded from the laptop to AWS. The full snapshot, all-2018 export, server/concurrency behavior and bibliometric comparisons against ClickHouse remain unvalidated.

Independent review: Claude Code, claude-opus-5-5 at max effort for evidence and high effort for the bounded correction, returned PASS after interpretation fixes. [Review findings and adjudication](../results/duckdb-extraction-2026-11-13/review-adjudication.md) and exact retained CLI invocations are archived.
