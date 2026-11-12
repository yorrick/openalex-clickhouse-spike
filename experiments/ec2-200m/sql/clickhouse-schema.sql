CREATE DATABASE IF NOT EXISTS openalex_spike;

CREATE OR REPLACE FUNCTION openalex_numeric_id AS id ->
    toUInt64OrNull(extract(id, '[A-Z]([0-9]+)$'));

CREATE OR REPLACE FUNCTION openalex_hierarchy_id AS id ->
    toUInt64OrNull(extract(id, '/([0-9]+)$'));

CREATE TABLE openalex_spike.works
(
    work_id UInt64,
    canonical_id String,
    publication_year Nullable(UInt16),
    work_type LowCardinality(String),
    source_id Nullable(UInt64),
    is_oa Bool,
    is_xpac Bool,
    cited_by_count UInt32,
    primary_topic_id Nullable(UInt64)
) ENGINE = MergeTree ORDER BY (ifNull(publication_year, 0), work_id);

CREATE TABLE openalex_spike.work_author
(
    work_id UInt64,
    author_id UInt64,
    author_position LowCardinality(String),
    is_corresponding Bool
) ENGINE = MergeTree ORDER BY (author_id, work_id);

CREATE TABLE openalex_spike.work_institution
(
    work_id UInt64,
    author_id UInt64,
    institution_id UInt64
) ENGINE = MergeTree ORDER BY (institution_id, work_id, author_id);

CREATE TABLE openalex_spike.work_topic
(
    work_id UInt64,
    topic_id UInt64,
    score Float32,
    is_primary Bool
) ENGINE = MergeTree ORDER BY (topic_id, work_id);

CREATE TABLE openalex_spike.citation_edge
(
    citing_work_id UInt64,
    cited_work_id UInt64,
    citing_year Nullable(UInt16)
) ENGINE = MergeTree ORDER BY (citing_work_id, cited_work_id);

CREATE TABLE openalex_spike.authors
(
    author_id UInt64,
    canonical_id String,
    display_name String,
    orcid Nullable(String)
) ENGINE = MergeTree ORDER BY author_id;

CREATE TABLE openalex_spike.institutions
(
    institution_id UInt64,
    canonical_id String,
    display_name String,
    country_code Nullable(String),
    institution_type LowCardinality(Nullable(String))
) ENGINE = MergeTree ORDER BY institution_id;

CREATE TABLE openalex_spike.sources
(
    source_id UInt64,
    canonical_id String,
    display_name Nullable(String),
    issn_l Nullable(String),
    source_type LowCardinality(Nullable(String))
) ENGINE = MergeTree ORDER BY source_id;

CREATE TABLE openalex_spike.topics
(
    topic_id UInt64,
    display_name String,
    subfield_id UInt64,
    field_id UInt64,
    domain_id UInt64
) ENGINE = MergeTree ORDER BY topic_id;
