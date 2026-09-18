create table if not exists occupations (
	id SERIAL PRIMARY KEY,
	cod_cbo VARCHAR(100) NOT NULL UNIQUE,
	nome_cbo VARCHAR(512) NOT NULL
)