create table if not exists occupations (
	id SERIAL PRIMARY KEY,
	cod_cbo VARCHAR(100) NOT NULL UNIQUE,
	nome_cbo VARCHAR(512) NOT NULL
);

create table if not exists pipeline_runs (
    id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(100),
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    status VARCHAR(100) DEFAULT 'SUCCESS',
    records_received SMALLINT,
    records_processed SMALLINT,
    records_discarded SMALLINT,
    error_message VARCHAR(512),
    created_at TIMESTAMPTZ
);