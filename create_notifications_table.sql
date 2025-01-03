-- Table: public.notifications

-- DROP TABLE IF EXISTS public.notifications;

CREATE TABLE IF NOT EXISTS public.notifications
(
    notify_id integer NOT NULL DEFAULT nextval('notifications_notify_id_seq'::regclass),
    domain_id integer NOT NULL,
    address character varying(255) COLLATE pg_catalog."default" NOT NULL,
    method character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT notifications_pkey PRIMARY KEY (notify_id),
    CONSTRAINT notifications_address_key UNIQUE (address),
    CONSTRAINT notifications_domain_id_fkey FOREIGN KEY (domain_id)
        REFERENCES public.domains (domain_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.notifications
    OWNER to postgres;