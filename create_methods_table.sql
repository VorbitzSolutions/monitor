-- Table: public.methods

-- DROP TABLE IF EXISTS public.methods;

CREATE TABLE IF NOT EXISTS public.methods
(
    method character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT methods_pkey PRIMARY KEY (method),
    CONSTRAINT methods_method_key UNIQUE (method)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.methods
    OWNER to postgres;