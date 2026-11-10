--
-- PostgreSQL database dump
--

\restrict Y2mNS3jSLVL3HSFj5yM0QsQpWxmnxi3TQOcoqfQFalNre1i1Qv2HHDKEqyNIn20

-- Dumped from database version 18.6 (Debian 18.6-1.pgdg13+2)
-- Dumped by pg_dump version 18.6 (Debian 18.6-1.pgdg13+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: authors; Type: TABLE; Schema: public; Owner: openalex
--

CREATE TABLE public.authors (
    author_id bigint NOT NULL,
    canonical_id text,
    display_name text,
    orcid text
);


ALTER TABLE public.authors OWNER TO openalex;

--
-- Name: citation_edge; Type: TABLE; Schema: public; Owner: openalex
--

CREATE TABLE public.citation_edge (
    citing_work_id bigint,
    cited_work_id bigint,
    citing_year integer
)
WITH (autovacuum_enabled='false');


ALTER TABLE public.citation_edge OWNER TO openalex;

--
-- Name: institutions; Type: TABLE; Schema: public; Owner: openalex
--

CREATE TABLE public.institutions (
    institution_id bigint NOT NULL,
    canonical_id text,
    display_name text,
    country_code text,
    institution_type text
);


ALTER TABLE public.institutions OWNER TO openalex;

--
-- Name: sources; Type: TABLE; Schema: public; Owner: openalex
--

CREATE TABLE public.sources (
    source_id bigint NOT NULL,
    canonical_id text,
    display_name text,
    issn_l text,
    source_type text
);


ALTER TABLE public.sources OWNER TO openalex;

--
-- Name: topics; Type: TABLE; Schema: public; Owner: openalex
--

CREATE TABLE public.topics (
    topic_id bigint NOT NULL,
    display_name text,
    subfield_id bigint,
    field_id bigint,
    domain_id bigint
);


ALTER TABLE public.topics OWNER TO openalex;

--
-- Name: work_author; Type: TABLE; Schema: public; Owner: openalex
--

CREATE TABLE public.work_author (
    work_id bigint,
    author_id bigint,
    author_position text,
    is_corresponding boolean
);


ALTER TABLE public.work_author OWNER TO openalex;

--
-- Name: work_institution; Type: TABLE; Schema: public; Owner: openalex
--

CREATE TABLE public.work_institution (
    work_id bigint,
    author_id bigint,
    institution_id bigint
);


ALTER TABLE public.work_institution OWNER TO openalex;

--
-- Name: work_topic; Type: TABLE; Schema: public; Owner: openalex
--

CREATE TABLE public.work_topic (
    work_id bigint,
    topic_id bigint,
    score real,
    is_primary boolean
);


ALTER TABLE public.work_topic OWNER TO openalex;

--
-- Name: works; Type: TABLE; Schema: public; Owner: openalex
--

CREATE TABLE public.works (
    work_id bigint NOT NULL,
    canonical_id text,
    publication_year integer,
    work_type text,
    source_id bigint,
    is_oa boolean,
    is_xpac boolean,
    cited_by_count bigint,
    primary_topic_id bigint
);


ALTER TABLE public.works OWNER TO openalex;

--
-- Name: authors authors_pk; Type: CONSTRAINT; Schema: public; Owner: openalex
--

ALTER TABLE ONLY public.authors
    ADD CONSTRAINT authors_pk PRIMARY KEY (author_id);


--
-- Name: institutions institutions_pk; Type: CONSTRAINT; Schema: public; Owner: openalex
--

ALTER TABLE ONLY public.institutions
    ADD CONSTRAINT institutions_pk PRIMARY KEY (institution_id);


--
-- Name: sources sources_pk; Type: CONSTRAINT; Schema: public; Owner: openalex
--

ALTER TABLE ONLY public.sources
    ADD CONSTRAINT sources_pk PRIMARY KEY (source_id);


--
-- Name: topics topics_pk; Type: CONSTRAINT; Schema: public; Owner: openalex
--

ALTER TABLE ONLY public.topics
    ADD CONSTRAINT topics_pk PRIMARY KEY (topic_id);


--
-- Name: works works_pk; Type: CONSTRAINT; Schema: public; Owner: openalex
--

ALTER TABLE ONLY public.works
    ADD CONSTRAINT works_pk PRIMARY KEY (work_id);


--
-- Name: work_author_author_work; Type: INDEX; Schema: public; Owner: openalex
--

CREATE INDEX work_author_author_work ON public.work_author USING btree (author_id, work_id);


--
-- Name: work_author_work_author; Type: INDEX; Schema: public; Owner: openalex
--

CREATE INDEX work_author_work_author ON public.work_author USING btree (work_id, author_id);


--
-- Name: work_institution_institution_work_author; Type: INDEX; Schema: public; Owner: openalex
--

CREATE INDEX work_institution_institution_work_author ON public.work_institution USING btree (institution_id, work_id, author_id);


--
-- Name: work_institution_work_institution; Type: INDEX; Schema: public; Owner: openalex
--

CREATE INDEX work_institution_work_institution ON public.work_institution USING btree (work_id, institution_id);


--
-- Name: work_topic_topic_work; Type: INDEX; Schema: public; Owner: openalex
--

CREATE INDEX work_topic_topic_work ON public.work_topic USING btree (topic_id, work_id);


--
-- Name: work_topic_work_topic; Type: INDEX; Schema: public; Owner: openalex
--

CREATE INDEX work_topic_work_topic ON public.work_topic USING btree (work_id, topic_id);


--
-- Name: works_year_id; Type: INDEX; Schema: public; Owner: openalex
--

CREATE INDEX works_year_id ON public.works USING btree (publication_year, work_id);


--
-- PostgreSQL database dump complete
--

\unrestrict Y2mNS3jSLVL3HSFj5yM0QsQpWxmnxi3TQOcoqfQFalNre1i1Qv2HHDKEqyNIn20

