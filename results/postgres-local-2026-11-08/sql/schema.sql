CREATE TABLE IF NOT EXISTS authors(author_id bigint,canonical_id text,display_name text,orcid text);
CREATE TABLE IF NOT EXISTS institutions(institution_id bigint,canonical_id text,display_name text,country_code text,institution_type text);
CREATE TABLE IF NOT EXISTS sources(source_id bigint,canonical_id text,display_name text,issn_l text,source_type text);
CREATE TABLE IF NOT EXISTS topics(topic_id bigint,display_name text,subfield_id bigint,field_id bigint,domain_id bigint);
CREATE TABLE IF NOT EXISTS works(work_id bigint,canonical_id text,publication_year integer,work_type text,source_id bigint,is_oa boolean,is_xpac boolean,cited_by_count bigint,primary_topic_id bigint);
CREATE TABLE IF NOT EXISTS work_author(work_id bigint,author_id bigint,author_position text,is_corresponding boolean);
CREATE TABLE IF NOT EXISTS work_institution(work_id bigint,author_id bigint,institution_id bigint);
CREATE TABLE IF NOT EXISTS work_topic(work_id bigint,topic_id bigint,score real,is_primary boolean);
CREATE TABLE IF NOT EXISTS citation_edge(citing_work_id bigint,cited_work_id bigint,citing_year integer);
