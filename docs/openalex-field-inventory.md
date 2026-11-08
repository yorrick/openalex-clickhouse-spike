# OpenAlex fields available versus loaded in ClickHouse

This inventory describes the **26 June 2026 snapshot used by our benchmarks**. It covers all 20 entity types present in that snapshot. It is not a catalogue of every field or entity currently exposed by the live API. Entity record counts come from the full snapshot manifest; field lists come from the saved benchmark schemas. For Works, the top-level cross-check covers the 154 selected files (31.89m rows), not all full-snapshot Works shards. No new performance test, data load, AWS resource or bulk download was run.

Only five source entities were loaded, producing nine normalized ClickHouse tables. All Authors, Institutions, Sources and Topics rows were loaded; Works was tested only at 2.00m, 10.11m and 31.89m rows. The full 510.37m Works figure below is a projection, not a completed load.

## What we retained

| Entity | Snapshot records | Top-level fields available | Fields used, including partial objects | Retained content |
|---|---:|---:|---:|---|
| works | 510,372,821 | 49 | 11 | IDs, publication year, type, primary source ID, OA and XPAC flags, citation count, primary topic ID; author, institution, topic and citation relationships. No titles, DOIs or abstracts. |
| authors | 119,129,660 | 20 | 3 | ID (canonical and numeric), display name, ORCID. No author-level statistics or affiliation histories. |
| institutions | 127,784 | 28 | 4 | ID (canonical and numeric), display name, country code, institution type. No ROR, geography or organizational lineage. |
| sources | 283,287 | 36 | 4 | ID (canonical and numeric), display name, ISSN-L, source type. No publisher hierarchy, OA history or APC information. |
| topics | 4,516 | 14 | 5 | Numeric ID, display name, subfield ID, field ID, domain ID. No topic description or keywords. |

“Used” means the loader reads at least one field from that top-level property. It does not mean the full object was preserved. IDs are converted to numeric keys, selected names are stored separately, null/empty values are normalized, some relationships are deduplicated, and fields use narrower ClickHouse types. This is an analytical projection, not a lossless copy.

For example, `works.authorships` has author metadata, raw names, raw affiliation strings, country arrays and institution objects. We kept only author ID, author position, corresponding-author flag and institution IDs. Institution country is available by joining the separate Institutions table; the original authorship country arrays were not retained.

## Every top-level field, by entity

“Selected nested fields” names the exact retained paths inside partly retained objects. The complete typed nested-path inventory and every destination column are in [the field-by-field appendix](../results/field-inventory-2026-11-08/fields.md) and [machine-readable inventory](../results/field-inventory-2026-11-08/inventory.json). Array paths use `[]`. Serialized objects such as `abstract_inverted_index` appear as string leaves in the saved Parquet schema; dynamic keys inside those strings are not separate physical fields.

### works

Snapshot: **510,372,821 records**, **724.970323 GB raw compressed Parquet**, **49 top-level fields**.

**Retained:** `id`, `publication_year`, `type`, `is_xpac`, `referenced_works`, `cited_by_count`.

**Partly retained:** `authorships`, `primary_topic`, `topics`, `primary_location`, `open_access`.

**Not loaded:** `doi`, `title`, `display_name`, `ids`, `indexed_in`, `publication_date`, `language`, `authors_count`, `corresponding_author_ids`, `corresponding_institution_ids`, `keywords`, `concepts`, `locations`, `locations_count`, `best_oa_location`, `sustainable_development_goals`, `awards`, `funders`, `institutions`, `countries_distinct_count`, `institutions_distinct_count`, `is_paratext`, `is_retracted`, `biblio`, `referenced_works_count`, `related_works`, `abstract_inverted_index`, `counts_by_year`, `apc_list`, `apc_paid`, `fwci`, `citation_normalized_percentile`, `cited_by_percentile_year`, `mesh`, `has_content`, `has_fulltext`, `created_date`, `updated_date`.

**Selected nested fields:** `authorships[].author.id`, `authorships[].author_position`, `authorships[].is_corresponding`, `authorships[].institutions[].id`, `primary_topic.id`, `topics[].id`, `topics[].score`, `primary_location.source.id`, `open_access.is_oa`.

| Source field | ClickHouse destination |
|---|---|
| `id` | `works.work_id`, `works.canonical_id`, `work_author.work_id`, `work_institution.work_id`, `work_topic.work_id`, `citation_edge.citing_work_id` |
| `publication_year` | `works.publication_year`, `citation_edge.citing_year` |
| `type` | `works.work_type` |
| `primary_location.source.id` | `works.source_id` |
| `open_access.is_oa` | `works.is_oa` |
| `is_xpac` | `works.is_xpac` |
| `cited_by_count` | `works.cited_by_count` |
| `primary_topic.id` | `works.primary_topic_id`, `work_topic.is_primary` |
| `authorships[].author.id` | `work_author.author_id`, `work_institution.author_id` |
| `authorships[].author_position` | `work_author.author_position` |
| `authorships[].is_corresponding` | `work_author.is_corresponding` |
| `authorships[].institutions[].id` | `work_institution.institution_id` |
| `topics[].id` | `work_topic.topic_id`, `work_topic.is_primary` |
| `topics[].score` | `work_topic.score` |
| `referenced_works[]` | `citation_edge.cited_work_id` |

### authors

Snapshot: **119,129,660 records**, **52.769910 GB raw compressed Parquet**, **20 top-level fields**.

**Retained:** `id`, `display_name`, `orcid`.

**Not loaded:** `display_name_alternatives`, `raw_author_names`, `full_name`, `works_count`, `cited_by_count`, `summary_stats`, `ids`, `affiliations`, `last_known_institutions`, `topics`, `topic_share`, `x_concepts`, `sources`, `counts_by_year`, `works_api_url`, `updated_date`, `created_date`.

| Source field | ClickHouse destination |
|---|---|
| `id` | `authors.author_id`, `authors.canonical_id` |
| `display_name` | `authors.display_name` |
| `orcid` | `authors.orcid` |

### institutions

Snapshot: **127,784 records**, **0.095649 GB raw compressed Parquet**, **28 top-level fields**.

**Retained:** `id`, `display_name`, `country_code`, `type`.

**Not loaded:** `ror`, `lineage`, `is_super_system`, `type_id`, `homepage_url`, `image_url`, `image_thumbnail_url`, `display_name_acronyms`, `display_name_alternatives`, `works_count`, `cited_by_count`, `ids`, `roles`, `repositories`, `geo`, `topics`, `topic_share`, `associated_institutions`, `counts_by_year`, `summary_stats`, `status`, `works_api_url`, `updated_date`, `created_date`.

| Source field | ClickHouse destination |
|---|---|
| `id` | `institutions.institution_id`, `institutions.canonical_id` |
| `display_name` | `institutions.display_name` |
| `country_code` | `institutions.country_code` |
| `type` | `institutions.institution_type` |

### sources

Snapshot: **283,287 records**, **0.170337 GB raw compressed Parquet**, **36 top-level fields**.

**Retained:** `id`, `issn_l`, `display_name`, `type`.

**Not loaded:** `issn`, `host_organization`, `host_organization_name`, `host_organization_lineage`, `works_count`, `oa_works_count`, `cited_by_count`, `summary_stats`, `is_oa`, `is_in_doaj`, `is_in_doaj_since_year`, `is_high_oa_rate`, `is_high_oa_rate_since_year`, `is_in_scielo`, `is_ojs`, `is_core`, `oa_flip_year`, `first_publication_year`, `last_publication_year`, `ids`, `homepage_url`, `apc_prices`, `apc_usd`, `country_code`, `societies`, `alternate_titles`, `topics`, `topic_share`, `counts_by_year`, `works_api_url`, `updated_date`, `created_date`.

| Source field | ClickHouse destination |
|---|---|
| `id` | `sources.source_id`, `sources.canonical_id` |
| `display_name` | `sources.display_name` |
| `issn_l` | `sources.issn_l` |
| `type` | `sources.source_type` |

### topics

Snapshot: **4,516 records**, **0.002589 GB raw compressed Parquet**, **14 top-level fields**.

**Retained:** `id`, `display_name`.

**Partly retained:** `subfield`, `field`, `domain`.

**Not loaded:** `description`, `keywords`, `ids`, `siblings`, `works_count`, `cited_by_count`, `works_api_url`, `updated_date`, `created_date`.

**Selected nested fields:** `subfield.id`, `field.id`, `domain.id`.

| Source field | ClickHouse destination |
|---|---|
| `id` | `topics.topic_id` |
| `display_name` | `topics.display_name` |
| `subfield.id` | `topics.subfield_id` |
| `field.id` | `topics.field_id` |
| `domain.id` | `topics.domain_id` |

### concepts

Snapshot: **65,026 records**, **0.010310 GB raw compressed Parquet**, **18 top-level fields**.

**Not loaded:** `id`, `display_name`, `level`, `description`, `wikidata`, `image_url`, `image_thumbnail_url`, `works_count`, `cited_by_count`, `ids`, `works_api_url`, `summary_stats`, `international`, `ancestors`, `related_concepts`, `counts_by_year`, `created_date`, `updated_date`.

No fields from this entity were loaded into ClickHouse.

### continents

Snapshot: **7 records**, **0.000017 GB raw compressed Parquet**, **11 top-level fields**.

**Not loaded:** `id`, `display_name`, `wikidata_id`, `wikidata_url`, `wikipedia_url`, `display_name_alternatives`, `description`, `ids`, `created_date`, `updated_date`, `countries`.

No fields from this entity were loaded into ClickHouse.

### countries

Snapshot: **247 records**, **0.000107 GB raw compressed Parquet**, **21 top-level fields**.

**Not loaded:** `id`, `country_code`, `display_name`, `continent_id`, `is_global_south`, `wikidata_url`, `wikipedia_url`, `display_name_alternatives`, `description`, `alpha_3`, `numeric`, `full_name`, `works_count`, `cited_by_count`, `authors_api_url`, `institutions_api_url`, `works_api_url`, `ids`, `created_date`, `updated_date`, `continent`.

No table from this entity was loaded. Country code is retained in `institutions.country_code`, but the Countries records and their other fields were not imported.

### domains

Snapshot: **4 records**, **0.000009 GB raw compressed Parquet**, **12 top-level fields**.

**Not loaded:** `id`, `display_name`, `description`, `ids`, `display_name_alternatives`, `fields`, `siblings`, `works_count`, `cited_by_count`, `works_api_url`, `updated_date`, `created_date`.

No table from this entity was loaded. Domain IDs are retained in `topics.domain_id`, but the Domains records and their other fields were not imported.

### fields

Snapshot: **26 records**, **0.000019 GB raw compressed Parquet**, **13 top-level fields**.

**Not loaded:** `id`, `display_name`, `description`, `ids`, `display_name_alternatives`, `domain`, `subfields`, `siblings`, `works_count`, `cited_by_count`, `works_api_url`, `updated_date`, `created_date`.

No table from this entity was loaded. Field IDs are retained in `topics.field_id`, but the Fields records and their other fields were not imported.

### funders

Snapshot: **45,640 records**, **0.011920 GB raw compressed Parquet**, **17 top-level fields**.

**Not loaded:** `id`, `display_name`, `alternate_titles`, `country_code`, `description`, `homepage_url`, `image_url`, `image_thumbnail_url`, `ids`, `works_count`, `cited_by_count`, `awards_count`, `roles`, `counts_by_year`, `summary_stats`, `created_date`, `updated_date`.

No fields from this entity were loaded into ClickHouse.

### institution-types

Snapshot: **8 records**, **0.000004 GB raw compressed Parquet**, **7 top-level fields**.

**Not loaded:** `id`, `display_name`, `works_api_url`, `works_count`, `cited_by_count`, `created_date`, `updated_date`.

No table from this entity was loaded. Institution type values are retained in `institutions.institution_type`, but the Institution Types records were not imported.

### keywords

Snapshot: **65,004 records**, **0.003712 GB raw compressed Parquet**, **7 top-level fields**.

**Not loaded:** `id`, `display_name`, `works_count`, `cited_by_count`, `works_api_url`, `created_date`, `updated_date`.

No fields from this entity were loaded into ClickHouse.

### languages

Snapshot: **179 records**, **0.000123 GB raw compressed Parquet**, **7 top-level fields**.

**Not loaded:** `id`, `works_api_url`, `display_name`, `works_count`, `cited_by_count`, `created_date`, `updated_date`.

No fields from this entity were loaded into ClickHouse.

### licenses

Snapshot: **10 records**, **0.000011 GB raw compressed Parquet**, **9 top-level fields**.

**Not loaded:** `id`, `display_name`, `works_count`, `cited_by_count`, `url`, `description`, `works_api_url`, `created_date`, `updated_date`.

No fields from this entity were loaded into ClickHouse.

### publishers

Snapshot: **10,703 records**, **0.003704 GB raw compressed Parquet**, **21 top-level fields**.

**Not loaded:** `id`, `lineage`, `display_name`, `alternate_titles`, `country_codes`, `hierarchy_level`, `parent_publisher`, `ids`, `ror_id`, `image_url`, `image_thumbnail_url`, `wikidata_id`, `homepage_url`, `works_count`, `cited_by_count`, `summary_stats`, `roles`, `counts_by_year`, `sources_api_url`, `created_date`, `updated_date`.

No fields from this entity were loaded into ClickHouse.

### sdgs

Snapshot: **17 records**, **0.000010 GB raw compressed Parquet**, **11 top-level fields**.

**Not loaded:** `id`, `ids`, `display_name`, `description`, `works_count`, `cited_by_count`, `image_url`, `image_thumbnail_url`, `works_api_url`, `created_date`, `updated_date`.

No fields from this entity were loaded into ClickHouse.

### source-types

Snapshot: **6 records**, **0.000004 GB raw compressed Parquet**, **7 top-level fields**.

**Not loaded:** `id`, `display_name`, `works_api_url`, `works_count`, `cited_by_count`, `created_date`, `updated_date`.

No table from this entity was loaded. Source type values are retained in `sources.source_type`, but the Source Types records were not imported.

### subfields

Snapshot: **252 records**, **0.000174 GB raw compressed Parquet**, **14 top-level fields**.

**Not loaded:** `id`, `display_name`, `description`, `ids`, `display_name_alternatives`, `field`, `domain`, `topics`, `siblings`, `works_count`, `cited_by_count`, `works_api_url`, `updated_date`, `created_date`.

No table from this entity was loaded. Subfield IDs are retained in `topics.subfield_id`, but the Subfields records and their other fields were not imported.

### work-types

Snapshot: **19 records**, **0.000009 GB raw compressed Parquet**, **8 top-level fields**.

**Not loaded:** `id`, `works_api_url`, `display_name`, `description`, `works_count`, `cited_by_count`, `created_date`, `updated_date`.

No table from this entity was loaded. Work type values are retained in `works.work_type`, but the Work Types records were not imported.

## Why approximately 60 GB does not mean 60 GB of RAM

At 31,885,241 Works, all nine active tables occupied **6.890 GB compressed on disk**. Complete Authors and the three other fixed dimensions occupied **3.364 GB** of that total. Holding these dimensions fixed and scaling only Works and their relationship tables by **16.0066** gives **59.80 GB** at 510,372,821 Works.

That is conditional storage arithmetic for the selected schema. Cohorts are nested and nonrandom; authorship counts, citation degrees, topic assignments and compressibility can differ outside the tested cohort. It excludes discarded fields, inactive parts, temporary processing space, logs, backups and the unimported entity tables. It is neither measured full-corpus storage nor a RAM requirement.

The 15 unimported entity types together occupy only **30.13 MB raw compressed** in this snapshot. Omitting whole support entities explains little of the reduction. Most source bytes are in Works (**724.97 GB**) and Authors (**52.77 GB**); discarding many fields within those records is the main scope difference. Raw Parquet and normalized ClickHouse encodings also differ, so their size ratio is not a pure compression ratio.

Your caching idea is plausible: on a machine with sufficient spare RAM, frequently used compressed files can remain in the operating system page cache. ClickHouse also has distinct mark and uncompressed-data caches; see the [official cache documentation](https://clickhouse.com/docs/concepts/features/performance/caches/caches). A cached read can avoid physical disk reads, but the engine still decompresses data, scans rows, builds joins and performs aggregations.

The same measured tables contained **19.59 GB of uncompressed column data**. Applying the same fixed-dimensions arithmetic gives about **164.0 GB uncompressed** at full Works volume. This is another conditional estimate, not a minimum RAM requirement: ClickHouse can decompress and process column blocks without keeping every column uncompressed in RAM at once.

Working memory is additional to cached compressed files. At the tested 31.89m scale, the parallel-hash topic query peaked at **13.28 GiB of query memory**, although the entire selected database occupied **6.89 GB compressed**. That is query memory, not total server memory, and excludes file cache. The same query took 65.5 seconds with the original plan, 5.64 seconds with a parallel hash join, and 9.26 seconds with pre-aggregated SQL on the same container. Caching alone therefore does not establish query speed or full-corpus memory requirements.

A single machine remains a plausible candidate for this selected analytical schema. We have not established that all complete OpenAlex records fit in RAM or that the full corpus meets a one-minute target. No further benchmark was run for this inventory.

## Evidence and scope

- Saved Arrow schemas for all 20 entities are archived in [the schemas directory](../results/field-inventory-2026-11-08/schemas). Nested fields come from one saved representative schema per entity. Top-level field names match the union of the already collected compressed-column metadata for all 2,771 sealed benchmark files; no additional file scan was run.
- The ClickHouse mappings were checked against `sql/00_schema.sql`, `sql/11_load_complete_authors.sql`, `sql/12_load_small_dimensions.sql` and `sql/20_load_works.sql`. All four match the deployed benchmark commit `0b3d5bcfbb5062aca4d26ae5f813c4659a234b5d` byte for byte. Every one of the nine tables and its columns is accounted for.
- `10_load_dimensions.sql` is the earlier sampled-author loader; it was not used for the complete-author Stage 2 runs. `05_raw_evidence.sql` provides query-time raw evidence, not an additional persisted analytical copy.
- [Original benchmark report](superpowers/2026-08-05-single-user-resource-benchmark-results.md), [full snapshot counts](../results/aws-scaling-2026-11-06/full-snapshot.json) and [measured 31.89m storage](../results/aws-scaling-2026-11-06/stage2_large.json), and [query-memory/tuning measurements](../results/aws-scaling-2026-11-06/q02-tuning.json).
- [OpenAlex snapshot documentation](https://help.openalex.org/access/snapshot/) explains that snapshot entity records follow the API object shape. Its current entity listing also includes Awards; Awards is not a separate entity in our historical 20-entity manifest, although `works.awards` is a field in that snapshot and was not loaded.

## Independent review

Claude Code `claude-opus-5-5` at explicit `high` effort reviewed the schemas, SQL mappings, field lists and storage arithmetic. Its initial wording findings were corrected, and a targeted second CLI review returned PASS; both CLI processes completed successfully with exit code 0. [Commands, checks and finding adjudication](../results/field-inventory-2026-11-08/provenance.json), [initial review](../results/field-inventory-2026-11-08/review-output.txt), [correction PASS](../results/field-inventory-2026-11-08/correction-review-output.txt).
