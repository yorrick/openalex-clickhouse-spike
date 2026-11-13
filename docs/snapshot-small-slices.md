# Small OpenAlex slices without Athena or an AWS account

Checked 13 November 2026 using anonymous HTTPS requests only. No AWS account, compute instance, Athena query, S3 Select operation or paid credentials were used. These are observations of the then-current snapshot, separate from the historical June snapshot used for the benchmarks.

## Layout and selecting complete files

OpenAlex publishes JSONL/gzip and Parquet/Snappy beneath `data/{format}/{entity}/updated_date=YYYY-MM-DD/part_*.{extension}`. The partition date records the entity's last update, not publication year. These are entity/update partitions, not an institution/topic/year index. This layout is documented in the [official snapshot description](https://help.openalex.org/access/snapshot/).

The anonymous Works manifest returned HTTP 200. It is dated 2026-10-14 and lists 1,898 Parquet files across 396 updated_date partitions. File sizes range from 64,058 bytes to 1,070,341,481 bytes; the median is 390,096,720 bytes. File row counts range from 1 to 400,000. The manifest totals are 464,765,485 Works and 744,042,462,611 bytes. These are what this manifest reports, not a reconciliation with other releases or the older benchmark. [Saved manifest and summaries](../results/snapshot-slicing-2026-11-13/) pin the observed bytes and SHA-256.

Downloading named files works for a bounded file sample or a complete small entity. It does not guarantee all Works for an institution, topic, author, publication year or selected list of IDs: matching records can occur in many update partitions. A sample chosen this way is not automatically representative, and cross-file citation/entity references do not become a self-contained graph.

## Anonymous ranges and Parquet metadata

Six ordinary HTTPS Range GETs returned HTTP 206 while inspecting three Works footers (smallest, middle file by byte size, largest). Only 609,492 footer/trailer bytes were transferred for that inspection, and footer row counts matched the manifest. The full manifest was unchanged when fetched again after the probes. No whole Works shard was downloaded.

The middle sample is 390,189,187 bytes with 400,000 rows in four row groups. Its first three publication_year min/max ranges are 1590 to 2026, 1462 to 2026 and 1513 to 2025. The largest sample has 400,000 rows in twelve row groups, also spanning broad year ranges. These three samples establish neither an exhaustive sorting audit nor that every filter must scan every row group; they show why updated_date directories cannot be treated as publication-year partitions.

A Parquet-aware local engine can use HTTP range reads and column projection rather than downloading every column. This is client-side query execution over ordinary object reads, not S3 running a WHERE clause. Predicate pruning depends on the requested filter and available statistics; for these broad-range samples, a narrow publication-year condition can still leave many row groups to inspect. We did not benchmark a full remote DuckDB/ClickHouse query in this check.

## S3 Select access and charges

[Amazon's SelectObjectContent API reference](https://docs.aws.amazon.com/AmazonS3/latest/API/API_SelectObjectContent.html) explicitly excludes anonymous access. Its [S3 Select guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/selecting-content-from-objects.html) also says the service is unavailable to new customers; existing customers can continue, and a request queries only one object. It is therefore not an account-free query endpoint for the public OpenAlex bucket.

Bucket-owner-pays should not be interpreted as permission to run Select. AWS describes ordinary request/storage/transfer billing in its [Requester Pays guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/RequesterPaysBuckets.html), and lists additional scanned/returned-data charges under [S3 Select pricing](https://aws.amazon.com/s3/pricing/). We did not establish that OpenAlex permits any authenticated Select operation, test existing-customer eligibility, or observe a Select invoice. The OpenAlex snapshot page credits the AWS Open Data program with covering download data-transfer fees; it does not document sponsorship of Select scan/return charges. No promise that OpenAlex will fund arbitrary query execution follows from its free downloads. Anonymous object retrieval is the verified free-to-the-downloader route here.

## Filtered small extracts

The [OpenAlex API](https://help.openalex.org/api/) can filter on publication year, institution and other bibliographic attributes without Athena. An anonymous request for three Works from 2024, selecting only id and publication_year, returned HTTP 200, three matching records and a 1,144-byte JSON response. The saved API receipt records a $0.0001 metered request against the anonymous free allowance, not a charge to an AWS account.

Currently the API reports a shared-IP $0.10/day anonymous allowance. A [free OpenAlex key](https://help.openalex.org/api/authentication/) raises the budget to $1/day, and [pricing documentation](https://help.openalex.org/access/pricing/) says no payment method is required. Filters/paging still have limits, and the API is the live service rather than the pinned snapshot; a snapshot-consistent extract needs to read/filter the relevant snapshot data. This verification did not create an OpenAlex account or key.

## Authenticated reads and who pays

Signing an ordinary S3 read does not by itself change its payer: the [AWS billing guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/RequesterPaysBuckets.html) says bucket owners normally pay, with Requester Pays as the exception. A successful anonymous read confirms this public download path does not require Requester Pays. Running local filtering incurs no Athena or EC2 query charge; copying data into your own S3 bucket or using AWS compute creates separate costs.

This does not settle whether authenticated S3 Select works against OpenAlex: existing-customer eligibility and authorization remain untested, Select has additional scan/return pricing, and the download-transfer sponsorship does not establish coverage of those charges. We have not issued a signed Select request or verified a Select bill. Anonymous reads were verified. For signed ordinary GETs, the bucket-owner-pays default means no S3 request or transfer charge to the reader is expected, but no signed read or billing invoice was checked; authenticated Select availability remains unestablished.

## Updates and file mutability

The [sync guide](https://help.openalex.org/access/sync/) says quarterly public releases replace files in place: changed records move to newer update-date partitions, so old partitions shrink. Database incremental sync reads partitions dated on or after the previous snapshot date and upserts by entity ID. File mirrors instead synchronize replacements and remove obsolete files. Deletions, metrics that do not advance updated_date and announced bulk changes need separate handling; this is not an immutable append-only feed.
