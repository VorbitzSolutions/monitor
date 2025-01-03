-- Table: public.shutdown

-- DROP TABLE IF EXISTS public.shutdown;

CREATE TABLE IF NOT EXISTS public.shutdown
(
    id integer NOT NULL DEFAULT nextval('shutdown_id_seq'::regclass),
    status integer,
    CONSTRAINT shutdown_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.shutdown
    OWNER to postgres;