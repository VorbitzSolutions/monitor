-- Table: public.domains

-- DROP TABLE IF EXISTS public.domains;

CREATE TABLE IF NOT EXISTS public.domains
(
    domain_id integer NOT NULL DEFAULT nextval('domains_domain_id_seq'::regclass),
    client_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    url character varying(255) COLLATE pg_catalog."default" NOT NULL,
    kword character varying(255) COLLATE pg_catalog."default" NOT NULL,
    andwords character varying(255)[] COLLATE pg_catalog."default" NOT NULL,
    notwords character varying(255)[] COLLATE pg_catalog."default" NOT NULL,
    status integer NOT NULL,
    create_date character varying(255) COLLATE pg_catalog."default" NOT NULL,
    modified_date character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT domains_pkey PRIMARY KEY (domain_id),
    CONSTRAINT domains_url_key UNIQUE (url)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.domains
    OWNER to postgres;
-- Index: index_name

-- DROP INDEX IF EXISTS public.index_name;

CREATE INDEX IF NOT EXISTS index_name
    ON public.domains USING btree
    (client_name COLLATE pg_catalog."default" ASC NULLS LAST)
    INCLUDE(client_name)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;