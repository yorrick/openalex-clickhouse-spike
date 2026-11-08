# Every source leaf field and its ClickHouse destination

Snapshot: 26 June 2026. Generated from the saved representative Arrow schemas, one per entity. `[]` denotes an array element. A retained field may be transformed or filtered by the SQL loader, not copied losslessly. All top-level fields are catalogued in [the readable inventory](../../docs/openalex-field-inventory.md).

## works

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | `works.work_id`, `works.canonical_id`, `work_author.work_id`, `work_institution.work_id`, `work_topic.work_id`, `citation_edge.citing_work_id` |
| `doi` | `string` | No |
| `title` | `string` | No |
| `display_name` | `string` | No |
| `ids` | `map<string, string>` | No |
| `indexed_in[]` | `string` | No |
| `publication_date` | `date32[day]` | No |
| `publication_year` | `int32` | `works.publication_year`, `citation_edge.citing_year` |
| `language` | `string` | No |
| `type` | `string` | `works.work_type` |
| `authorships[].author.display_name` | `string` | No |
| `authorships[].author.id` | `string` | `work_author.author_id`, `work_institution.author_id` |
| `authorships[].author.orcid` | `string` | No |
| `authorships[].author_position` | `string` | `work_author.author_position` |
| `authorships[].affiliations[].institution_ids[]` | `string` | No |
| `authorships[].affiliations[].raw_affiliation_string` | `string` | No |
| `authorships[].countries[]` | `string` | No |
| `authorships[].raw_author_name` | `string` | No |
| `authorships[].raw_orcid` | `string` | No |
| `authorships[].is_corresponding` | `bool` | `work_author.is_corresponding` |
| `authorships[].raw_affiliation_strings[]` | `string` | No |
| `authorships[].institutions[].country_code` | `string` | No |
| `authorships[].institutions[].display_name` | `string` | No |
| `authorships[].institutions[].id` | `string` | `work_institution.institution_id` |
| `authorships[].institutions[].lineage[]` | `string` | No |
| `authorships[].institutions[].ror` | `string` | No |
| `authorships[].institutions[].type` | `string` | No |
| `authors_count` | `int32` | No |
| `corresponding_author_ids[]` | `string` | No |
| `corresponding_institution_ids[]` | `string` | No |
| `primary_topic.id` | `string` | `works.primary_topic_id`, `work_topic.is_primary` |
| `primary_topic.display_name` | `string` | No |
| `primary_topic.score` | `float` | No |
| `primary_topic.subfield.id` | `string` | No |
| `primary_topic.subfield.display_name` | `string` | No |
| `primary_topic.field.id` | `string` | No |
| `primary_topic.field.display_name` | `string` | No |
| `primary_topic.domain.id` | `string` | No |
| `primary_topic.domain.display_name` | `string` | No |
| `topics[].id` | `string` | `work_topic.topic_id`, `work_topic.is_primary` |
| `topics[].display_name` | `string` | No |
| `topics[].score` | `float` | `work_topic.score` |
| `topics[].subfield.id` | `string` | No |
| `topics[].subfield.display_name` | `string` | No |
| `topics[].field.id` | `string` | No |
| `topics[].field.display_name` | `string` | No |
| `topics[].domain.id` | `string` | No |
| `topics[].domain.display_name` | `string` | No |
| `keywords[].id` | `string` | No |
| `keywords[].display_name` | `string` | No |
| `keywords[].score` | `float` | No |
| `concepts[].id` | `string` | No |
| `concepts[].wikidata` | `string` | No |
| `concepts[].display_name` | `string` | No |
| `concepts[].level` | `int32` | No |
| `concepts[].score` | `float` | No |
| `locations[].id` | `string` | No |
| `locations[].source.id` | `string` | No |
| `locations[].source.display_name` | `string` | No |
| `locations[].source.issn_l` | `string` | No |
| `locations[].source.issn[]` | `string` | No |
| `locations[].source.is_oa` | `bool` | No |
| `locations[].source.is_in_doaj` | `bool` | No |
| `locations[].source.is_core` | `bool` | No |
| `locations[].source.host_organization` | `string` | No |
| `locations[].source.host_organization_name` | `string` | No |
| `locations[].source.host_organization_lineage[]` | `string` | No |
| `locations[].source.host_organization_lineage_names[]` | `string` | No |
| `locations[].source.type` | `string` | No |
| `locations[].is_oa` | `bool` | No |
| `locations[].is_published` | `bool` | No |
| `locations[].landing_page_url` | `string` | No |
| `locations[].pdf_url` | `string` | No |
| `locations[].raw_source_name` | `string` | No |
| `locations[].raw_type` | `string` | No |
| `locations[].provenance` | `string` | No |
| `locations[].license` | `string` | No |
| `locations[].license_id` | `string` | No |
| `locations[].version` | `string` | No |
| `locations[].is_accepted` | `bool` | No |
| `locations_count` | `int32` | No |
| `primary_location.id` | `string` | No |
| `primary_location.source.id` | `string` | `works.source_id` |
| `primary_location.source.display_name` | `string` | No |
| `primary_location.source.issn_l` | `string` | No |
| `primary_location.source.issn[]` | `string` | No |
| `primary_location.source.is_oa` | `bool` | No |
| `primary_location.source.is_in_doaj` | `bool` | No |
| `primary_location.source.is_core` | `bool` | No |
| `primary_location.source.host_organization` | `string` | No |
| `primary_location.source.host_organization_name` | `string` | No |
| `primary_location.source.host_organization_lineage[]` | `string` | No |
| `primary_location.source.host_organization_lineage_names[]` | `string` | No |
| `primary_location.source.type` | `string` | No |
| `primary_location.is_oa` | `bool` | No |
| `primary_location.is_published` | `bool` | No |
| `primary_location.landing_page_url` | `string` | No |
| `primary_location.pdf_url` | `string` | No |
| `primary_location.raw_source_name` | `string` | No |
| `primary_location.raw_type` | `string` | No |
| `primary_location.provenance` | `string` | No |
| `primary_location.license` | `string` | No |
| `primary_location.license_id` | `string` | No |
| `primary_location.version` | `string` | No |
| `primary_location.is_accepted` | `bool` | No |
| `best_oa_location.id` | `string` | No |
| `best_oa_location.source.id` | `string` | No |
| `best_oa_location.source.display_name` | `string` | No |
| `best_oa_location.source.issn_l` | `string` | No |
| `best_oa_location.source.issn[]` | `string` | No |
| `best_oa_location.source.is_oa` | `bool` | No |
| `best_oa_location.source.is_in_doaj` | `bool` | No |
| `best_oa_location.source.is_core` | `bool` | No |
| `best_oa_location.source.host_organization` | `string` | No |
| `best_oa_location.source.host_organization_name` | `string` | No |
| `best_oa_location.source.host_organization_lineage[]` | `string` | No |
| `best_oa_location.source.host_organization_lineage_names[]` | `string` | No |
| `best_oa_location.source.type` | `string` | No |
| `best_oa_location.is_oa` | `bool` | No |
| `best_oa_location.is_published` | `bool` | No |
| `best_oa_location.landing_page_url` | `string` | No |
| `best_oa_location.pdf_url` | `string` | No |
| `best_oa_location.raw_source_name` | `string` | No |
| `best_oa_location.raw_type` | `string` | No |
| `best_oa_location.provenance` | `string` | No |
| `best_oa_location.license` | `string` | No |
| `best_oa_location.license_id` | `string` | No |
| `best_oa_location.version` | `string` | No |
| `best_oa_location.is_accepted` | `bool` | No |
| `sustainable_development_goals[].id` | `string` | No |
| `sustainable_development_goals[].display_name` | `string` | No |
| `sustainable_development_goals[].score` | `double` | No |
| `awards[].id` | `string` | No |
| `awards[].display_name` | `string` | No |
| `awards[].funder_award_id` | `string` | No |
| `awards[].funder_id` | `string` | No |
| `awards[].funder_display_name` | `string` | No |
| `funders[].id` | `string` | No |
| `funders[].display_name` | `string` | No |
| `funders[].ror` | `string` | No |
| `institutions[].id` | `string` | No |
| `institutions[].display_name` | `string` | No |
| `institutions[].ror` | `string` | No |
| `institutions[].country_code` | `string` | No |
| `institutions[].type` | `string` | No |
| `institutions[].lineage[]` | `string` | No |
| `countries_distinct_count` | `int32` | No |
| `institutions_distinct_count` | `int32` | No |
| `open_access.is_oa` | `bool` | `works.is_oa` |
| `open_access.oa_status` | `string` | No |
| `open_access.any_repository_has_fulltext` | `bool` | No |
| `open_access.oa_url` | `string` | No |
| `is_paratext` | `bool` | No |
| `is_retracted` | `bool` | No |
| `is_xpac` | `bool` | `works.is_xpac` |
| `biblio.volume` | `string` | No |
| `biblio.issue` | `string` | No |
| `biblio.first_page` | `string` | No |
| `biblio.last_page` | `string` | No |
| `referenced_works[]` | `string` | `citation_edge.cited_work_id` |
| `referenced_works_count` | `int32` | No |
| `related_works[]` | `string` | No |
| `abstract_inverted_index` | `string` | No |
| `cited_by_count` | `int32` | `works.cited_by_count` |
| `counts_by_year[].year` | `int32` | No |
| `counts_by_year[].cited_by_count` | `int32` | No |
| `apc_list.value` | `int32` | No |
| `apc_list.currency` | `string` | No |
| `apc_list.value_usd` | `int32` | No |
| `apc_paid.value` | `double` | No |
| `apc_paid.currency` | `string` | No |
| `apc_paid.value_usd` | `double` | No |
| `fwci` | `double` | No |
| `citation_normalized_percentile.value` | `double` | No |
| `citation_normalized_percentile.is_in_top_1_percent` | `bool` | No |
| `citation_normalized_percentile.is_in_top_10_percent` | `bool` | No |
| `cited_by_percentile_year.min` | `int32` | No |
| `cited_by_percentile_year.max` | `int32` | No |
| `mesh[].descriptor_ui` | `string` | No |
| `mesh[].descriptor_name` | `string` | No |
| `mesh[].qualifier_ui` | `string` | No |
| `mesh[].qualifier_name` | `string` | No |
| `mesh[].is_major_topic` | `bool` | No |
| `has_content.pdf` | `bool` | No |
| `has_content.grobid_xml` | `bool` | No |
| `has_fulltext` | `bool` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |

## authors

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | `authors.author_id`, `authors.canonical_id` |
| `display_name` | `string` | `authors.display_name` |
| `display_name_alternatives[]` | `string` | No |
| `raw_author_names[]` | `string` | No |
| `full_name` | `string` | No |
| `orcid` | `string` | `authors.orcid` |
| `works_count` | `int32` | No |
| `cited_by_count` | `int32` | No |
| `summary_stats.2yr_mean_citedness` | `double` | No |
| `summary_stats.h_index` | `int32` | No |
| `summary_stats.i10_index` | `int32` | No |
| `ids.openalex` | `string` | No |
| `ids.orcid` | `string` | No |
| `affiliations[].institution.id` | `string` | No |
| `affiliations[].institution.ror` | `string` | No |
| `affiliations[].institution.display_name` | `string` | No |
| `affiliations[].institution.country_code` | `string` | No |
| `affiliations[].institution.type` | `string` | No |
| `affiliations[].institution.lineage[]` | `string` | No |
| `affiliations[].years[]` | `int32` | No |
| `last_known_institutions[].id` | `string` | No |
| `last_known_institutions[].ror` | `string` | No |
| `last_known_institutions[].display_name` | `string` | No |
| `last_known_institutions[].country_code` | `string` | No |
| `last_known_institutions[].type` | `string` | No |
| `last_known_institutions[].lineage[]` | `string` | No |
| `topics[].id` | `string` | No |
| `topics[].display_name` | `string` | No |
| `topics[].count` | `int32` | No |
| `topics[].subfield.id` | `string` | No |
| `topics[].subfield.display_name` | `string` | No |
| `topics[].field.id` | `string` | No |
| `topics[].field.display_name` | `string` | No |
| `topics[].domain.id` | `string` | No |
| `topics[].domain.display_name` | `string` | No |
| `topic_share[].id` | `string` | No |
| `topic_share[].display_name` | `string` | No |
| `topic_share[].value` | `double` | No |
| `topic_share[].subfield.id` | `string` | No |
| `topic_share[].subfield.display_name` | `string` | No |
| `topic_share[].field.id` | `string` | No |
| `topic_share[].field.display_name` | `string` | No |
| `topic_share[].domain.id` | `string` | No |
| `topic_share[].domain.display_name` | `string` | No |
| `x_concepts[].id` | `string` | No |
| `x_concepts[].wikidata` | `string` | No |
| `x_concepts[].display_name` | `string` | No |
| `x_concepts[].level` | `int32` | No |
| `x_concepts[].score` | `float` | No |
| `x_concepts[].count` | `int32` | No |
| `sources[].id` | `string` | No |
| `sources[].display_name` | `string` | No |
| `sources[].issn_l` | `string` | No |
| `sources[].issn[]` | `string` | No |
| `sources[].is_oa` | `bool` | No |
| `sources[].is_in_doaj` | `bool` | No |
| `sources[].is_core` | `bool` | No |
| `sources[].host_organization` | `string` | No |
| `sources[].host_organization_name` | `string` | No |
| `sources[].host_organization_lineage[]` | `string` | No |
| `sources[].host_organization_lineage_names[]` | `string` | No |
| `sources[].type` | `string` | No |
| `counts_by_year[].year` | `int32` | No |
| `counts_by_year[].works_count` | `int32` | No |
| `counts_by_year[].oa_works_count` | `int32` | No |
| `counts_by_year[].cited_by_count` | `int32` | No |
| `works_api_url` | `string` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |

## institutions

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | `institutions.institution_id`, `institutions.canonical_id` |
| `ror` | `string` | No |
| `display_name` | `string` | `institutions.display_name` |
| `country_code` | `string` | `institutions.country_code` |
| `type` | `string` | `institutions.institution_type` |
| `lineage[]` | `string` | No |
| `is_super_system` | `bool` | No |
| `type_id` | `string` | No |
| `homepage_url` | `string` | No |
| `image_url` | `string` | No |
| `image_thumbnail_url` | `string` | No |
| `display_name_acronyms[]` | `string` | No |
| `display_name_alternatives[]` | `string` | No |
| `works_count` | `int32` | No |
| `cited_by_count` | `int32` | No |
| `ids.openalex` | `string` | No |
| `ids.ror` | `string` | No |
| `ids.grid` | `string` | No |
| `ids.wikipedia` | `string` | No |
| `ids.wikidata` | `string` | No |
| `roles[].role` | `string` | No |
| `roles[].id` | `string` | No |
| `roles[].works_count` | `int32` | No |
| `repositories[].id` | `string` | No |
| `repositories[].display_name` | `string` | No |
| `repositories[].host_organization` | `string` | No |
| `repositories[].host_organization_name` | `string` | No |
| `repositories[].host_organization_lineage[]` | `string` | No |
| `geo.city` | `string` | No |
| `geo.geonames_city_id` | `string` | No |
| `geo.region` | `string` | No |
| `geo.country_code` | `string` | No |
| `geo.country` | `string` | No |
| `geo.latitude` | `double` | No |
| `geo.longitude` | `double` | No |
| `topics[].id` | `string` | No |
| `topics[].display_name` | `string` | No |
| `topics[].count` | `int32` | No |
| `topics[].score` | `float` | No |
| `topics[].subfield.id` | `string` | No |
| `topics[].subfield.display_name` | `string` | No |
| `topics[].field.id` | `string` | No |
| `topics[].field.display_name` | `string` | No |
| `topics[].domain.id` | `string` | No |
| `topics[].domain.display_name` | `string` | No |
| `topic_share[].id` | `string` | No |
| `topic_share[].display_name` | `string` | No |
| `topic_share[].value` | `double` | No |
| `topic_share[].subfield.id` | `string` | No |
| `topic_share[].subfield.display_name` | `string` | No |
| `topic_share[].field.id` | `string` | No |
| `topic_share[].field.display_name` | `string` | No |
| `topic_share[].domain.id` | `string` | No |
| `topic_share[].domain.display_name` | `string` | No |
| `associated_institutions[].id` | `string` | No |
| `associated_institutions[].ror` | `string` | No |
| `associated_institutions[].display_name` | `string` | No |
| `associated_institutions[].country_code` | `string` | No |
| `associated_institutions[].type` | `string` | No |
| `associated_institutions[].relationship` | `string` | No |
| `counts_by_year[].year` | `int32` | No |
| `counts_by_year[].works_count` | `int32` | No |
| `counts_by_year[].oa_works_count` | `int32` | No |
| `counts_by_year[].cited_by_count` | `int32` | No |
| `summary_stats.2yr_mean_citedness` | `double` | No |
| `summary_stats.h_index` | `int32` | No |
| `summary_stats.i10_index` | `int32` | No |
| `status` | `string` | No |
| `works_api_url` | `string` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |

## sources

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | `sources.source_id`, `sources.canonical_id` |
| `issn_l` | `string` | `sources.issn_l` |
| `issn[]` | `string` | No |
| `display_name` | `string` | `sources.display_name` |
| `host_organization` | `string` | No |
| `host_organization_name` | `string` | No |
| `host_organization_lineage[]` | `string` | No |
| `works_count` | `int32` | No |
| `oa_works_count` | `int32` | No |
| `cited_by_count` | `int32` | No |
| `summary_stats.2yr_mean_citedness` | `double` | No |
| `summary_stats.h_index` | `int32` | No |
| `summary_stats.i10_index` | `int32` | No |
| `is_oa` | `bool` | No |
| `is_in_doaj` | `bool` | No |
| `is_in_doaj_since_year` | `int32` | No |
| `is_high_oa_rate` | `bool` | No |
| `is_high_oa_rate_since_year` | `int64` | No |
| `is_in_scielo` | `bool` | No |
| `is_ojs` | `bool` | No |
| `is_core` | `bool` | No |
| `oa_flip_year` | `int32` | No |
| `first_publication_year` | `int32` | No |
| `last_publication_year` | `int32` | No |
| `ids.openalex` | `string` | No |
| `ids.issn_l` | `string` | No |
| `ids.issn[]` | `string` | No |
| `ids.mag` | `string` | No |
| `ids.wikidata` | `string` | No |
| `homepage_url` | `string` | No |
| `apc_prices[].price` | `int32` | No |
| `apc_prices[].currency` | `string` | No |
| `apc_usd` | `int32` | No |
| `country_code` | `string` | No |
| `societies[].url` | `string` | No |
| `societies[].organization` | `string` | No |
| `alternate_titles[]` | `string` | No |
| `type` | `string` | `sources.source_type` |
| `topics[].id` | `string` | No |
| `topics[].display_name` | `string` | No |
| `topics[].count` | `int32` | No |
| `topics[].subfield.id` | `string` | No |
| `topics[].subfield.display_name` | `string` | No |
| `topics[].field.id` | `string` | No |
| `topics[].field.display_name` | `string` | No |
| `topics[].domain.id` | `string` | No |
| `topics[].domain.display_name` | `string` | No |
| `topic_share[].id` | `string` | No |
| `topic_share[].display_name` | `string` | No |
| `topic_share[].value` | `double` | No |
| `topic_share[].subfield.id` | `string` | No |
| `topic_share[].subfield.display_name` | `string` | No |
| `topic_share[].field.id` | `string` | No |
| `topic_share[].field.display_name` | `string` | No |
| `topic_share[].domain.id` | `string` | No |
| `topic_share[].domain.display_name` | `string` | No |
| `counts_by_year[].year` | `int32` | No |
| `counts_by_year[].works_count` | `int32` | No |
| `counts_by_year[].oa_works_count` | `int32` | No |
| `counts_by_year[].cited_by_count` | `int32` | No |
| `works_api_url` | `string` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |

## topics

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | `topics.topic_id` |
| `display_name` | `string` | `topics.display_name` |
| `description` | `string` | No |
| `keywords[]` | `string` | No |
| `ids.openalex` | `string` | No |
| `ids.wikipedia` | `string` | No |
| `subfield.id` | `string` | `topics.subfield_id` |
| `subfield.display_name` | `string` | No |
| `field.id` | `string` | `topics.field_id` |
| `field.display_name` | `string` | No |
| `domain.id` | `string` | `topics.domain_id` |
| `domain.display_name` | `string` | No |
| `siblings[].id` | `string` | No |
| `siblings[].display_name` | `string` | No |
| `works_count` | `int32` | No |
| `cited_by_count` | `int32` | No |
| `works_api_url` | `string` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |

## concepts

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | No |
| `display_name` | `string` | No |
| `level` | `int32` | No |
| `description` | `string` | No |
| `wikidata` | `string` | No |
| `image_url` | `string` | No |
| `image_thumbnail_url` | `string` | No |
| `works_count` | `int32` | No |
| `cited_by_count` | `int32` | No |
| `ids.openalex` | `string` | No |
| `ids.wikidata` | `string` | No |
| `ids.wikipedia` | `string` | No |
| `ids.umls_aui[]` | `string` | No |
| `ids.umls_cui[]` | `string` | No |
| `ids.mag` | `string` | No |
| `works_api_url` | `string` | No |
| `summary_stats.2yr_mean_citedness` | `double` | No |
| `summary_stats.h_index` | `int32` | No |
| `summary_stats.i10_index` | `int32` | No |
| `international` | `map<string, string>` | No |
| `ancestors[]` | `string` | No |
| `related_concepts[]` | `string` | No |
| `counts_by_year[]` | `string` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |

## continents

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | No |
| `display_name` | `string` | No |
| `wikidata_id` | `string` | No |
| `wikidata_url` | `string` | No |
| `wikipedia_url` | `string` | No |
| `display_name_alternatives[]` | `string` | No |
| `description` | `string` | No |
| `ids.openalex` | `string` | No |
| `ids.wikidata` | `string` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |
| `countries[].id` | `string` | No |
| `countries[].display_name` | `string` | No |

## countries

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | No |
| `country_code` | `string` | No |
| `display_name` | `string` | No |
| `continent_id` | `int32` | No |
| `is_global_south` | `bool` | No |
| `wikidata_url` | `string` | No |
| `wikipedia_url` | `string` | No |
| `display_name_alternatives[]` | `string` | No |
| `description` | `string` | No |
| `alpha_3` | `string` | No |
| `numeric` | `int32` | No |
| `full_name` | `string` | No |
| `works_count` | `int64` | No |
| `cited_by_count` | `int64` | No |
| `authors_api_url` | `string` | No |
| `institutions_api_url` | `string` | No |
| `works_api_url` | `string` | No |
| `ids.openalex` | `string` | No |
| `ids.iso` | `string` | No |
| `ids.wikidata` | `string` | No |
| `ids.wikipedia` | `string` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |
| `continent.id` | `string` | No |
| `continent.display_name` | `string` | No |

## domains

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | No |
| `display_name` | `string` | No |
| `description` | `string` | No |
| `ids.openalex` | `string` | No |
| `ids.wikidata` | `string` | No |
| `ids.wikipedia` | `string` | No |
| `display_name_alternatives[]` | `string` | No |
| `fields[].id` | `string` | No |
| `fields[].display_name` | `string` | No |
| `siblings[].id` | `string` | No |
| `siblings[].display_name` | `string` | No |
| `works_count` | `int32` | No |
| `cited_by_count` | `int32` | No |
| `works_api_url` | `string` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |

## fields

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | No |
| `display_name` | `string` | No |
| `description` | `string` | No |
| `ids.openalex` | `string` | No |
| `ids.wikidata` | `string` | No |
| `ids.wikipedia` | `string` | No |
| `display_name_alternatives[]` | `string` | No |
| `domain.id` | `string` | No |
| `domain.display_name` | `string` | No |
| `subfields[].id` | `string` | No |
| `subfields[].display_name` | `string` | No |
| `siblings[].id` | `string` | No |
| `siblings[].display_name` | `string` | No |
| `works_count` | `int32` | No |
| `cited_by_count` | `int32` | No |
| `works_api_url` | `string` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |

## funders

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | No |
| `display_name` | `string` | No |
| `alternate_titles[]` | `string` | No |
| `country_code` | `string` | No |
| `description` | `string` | No |
| `homepage_url` | `string` | No |
| `image_url` | `string` | No |
| `image_thumbnail_url` | `string` | No |
| `ids.openalex` | `string` | No |
| `ids.ror` | `string` | No |
| `ids.wikidata` | `string` | No |
| `ids.crossref` | `int64` | No |
| `ids.doi` | `string` | No |
| `works_count` | `int32` | No |
| `cited_by_count` | `int32` | No |
| `awards_count` | `int64` | No |
| `roles[].role` | `string` | No |
| `roles[].id` | `string` | No |
| `roles[].works_count` | `int32` | No |
| `counts_by_year[].year` | `int32` | No |
| `counts_by_year[].works_count` | `int32` | No |
| `counts_by_year[].oa_works_count` | `int32` | No |
| `counts_by_year[].cited_by_count` | `int32` | No |
| `summary_stats.2yr_mean_citedness` | `double` | No |
| `summary_stats.h_index` | `int32` | No |
| `summary_stats.i10_index` | `int32` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |

## institution-types

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | No |
| `display_name` | `string` | No |
| `works_api_url` | `string` | No |
| `works_count` | `int64` | No |
| `cited_by_count` | `int64` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |

## keywords

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | No |
| `display_name` | `string` | No |
| `works_count` | `int32` | No |
| `cited_by_count` | `int32` | No |
| `works_api_url` | `string` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |

## languages

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | No |
| `works_api_url` | `string` | No |
| `display_name` | `string` | No |
| `works_count` | `int64` | No |
| `cited_by_count` | `int64` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |

## licenses

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | No |
| `display_name` | `string` | No |
| `works_count` | `int64` | No |
| `cited_by_count` | `int64` | No |
| `url` | `string` | No |
| `description` | `string` | No |
| `works_api_url` | `string` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |

## publishers

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | No |
| `lineage[]` | `string` | No |
| `display_name` | `string` | No |
| `alternate_titles[]` | `string` | No |
| `country_codes[]` | `string` | No |
| `hierarchy_level` | `int32` | No |
| `parent_publisher.id` | `string` | No |
| `parent_publisher.display_name` | `string` | No |
| `ids.openalex` | `string` | No |
| `ids.ror` | `string` | No |
| `ids.wikidata` | `string` | No |
| `ror_id` | `string` | No |
| `image_url` | `string` | No |
| `image_thumbnail_url` | `string` | No |
| `wikidata_id` | `string` | No |
| `homepage_url` | `string` | No |
| `works_count` | `int64` | No |
| `cited_by_count` | `int64` | No |
| `summary_stats.2yr_mean_citedness` | `double` | No |
| `summary_stats.h_index` | `int32` | No |
| `summary_stats.i10_index` | `int32` | No |
| `roles[].role` | `string` | No |
| `roles[].id` | `string` | No |
| `roles[].works_count` | `int32` | No |
| `counts_by_year[].year` | `int32` | No |
| `counts_by_year[].works_count` | `int64` | No |
| `counts_by_year[].cited_by_count` | `int64` | No |
| `sources_api_url` | `string` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |

## sdgs

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | No |
| `ids.openalex` | `string` | No |
| `ids.un` | `string` | No |
| `ids.wikidata` | `string` | No |
| `display_name` | `string` | No |
| `description` | `string` | No |
| `works_count` | `int64` | No |
| `cited_by_count` | `int64` | No |
| `image_url` | `string` | No |
| `image_thumbnail_url` | `string` | No |
| `works_api_url` | `string` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |

## source-types

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | No |
| `display_name` | `string` | No |
| `works_api_url` | `string` | No |
| `works_count` | `int64` | No |
| `cited_by_count` | `int64` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |

## subfields

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | No |
| `display_name` | `string` | No |
| `description` | `string` | No |
| `ids.openalex` | `string` | No |
| `ids.wikidata` | `string` | No |
| `ids.wikipedia` | `string` | No |
| `display_name_alternatives[]` | `string` | No |
| `field.id` | `string` | No |
| `field.display_name` | `string` | No |
| `domain.id` | `string` | No |
| `domain.display_name` | `string` | No |
| `topics[].id` | `string` | No |
| `topics[].display_name` | `string` | No |
| `siblings[].id` | `string` | No |
| `siblings[].display_name` | `string` | No |
| `works_count` | `int32` | No |
| `cited_by_count` | `int32` | No |
| `works_api_url` | `string` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |

## work-types

| Source field path | Source leaf type | Loaded into ClickHouse |
|---|---|---|
| `id` | `string` | No |
| `works_api_url` | `string` | No |
| `display_name` | `string` | No |
| `description` | `string` | No |
| `works_count` | `int64` | No |
| `cited_by_count` | `int64` | No |
| `created_date` | `timestamp[us, tz=UTC]` | No |
| `updated_date` | `timestamp[us, tz=UTC]` | No |
