# Occupations Data Pipeline

Pipeline de Engenharia de Dados desenvolvido de forma incremental para ingestão, transformação, validação e análise de dados sobre ocupações profissionais.

O projeto utiliza dados da **Classificação Brasileira de Ocupações (CBO)** como fonte inicial e será evoluído gradualmente para trabalhar com banco de dados, cloud e processamento de dados em maior escala.

## Objetivo

Construir um pipeline de dados sobre ocupações profissionais que possa futuramente disponibilizar informações como:

* Código e nome da ocupação
* Nomes similares
* Descrição da ocupação
* Conhecimentos e habilidades
* Skills
* Certificações
* Ocupações relacionadas
* Outros dados relevantes para análise do mercado de trabalho

O foco principal do projeto é **Engenharia de Dados**, trabalhando com ingestão, transformação, qualidade, armazenamento, modelagem e análise dos dados.

## Evolução planejada

O projeto será desenvolvido em etapas:

```text
Fonte de dados
     ↓
Python + Pandas
     ↓
CSV / JSON / Parquet
     ↓
PostgreSQL
     ↓
SQL + Analytics
     ↓
Docker
     ↓
AWS S3
     ↓
AWS RDS
     ↓
Terraform
     ↓
Kafka / Streaming
     ↓
Processamento distribuído
```

A ordem poderá ser ajustada conforme a evolução do projeto e os requisitos de cada etapa.

---

# Etapa 1 — Ingestão e limpeza dos dados

Nesta primeira etapa, o objetivo é construir uma rotina inicial para carregar os dados de ocupações, realizar validações básicas de qualidade e gerar uma versão processada do dataset.

## Pipeline atual

```text
data/raw/cbo.csv
       │
       ▼
   Pandas
       │
       ▼
Validação e limpeza
       │
       ├── Remoção de linhas duplicadas
       ├── Validação de CBOs duplicados
       └── Remoção de ocupações sem nome
       │
       ▼
data/processed/
occupations_processed.csv
```

## Regras de qualidade

Atualmente o pipeline realiza as seguintes verificações:

### Linhas duplicadas

Verifica se existem registros completamente iguais no DataFrame.

```python
df.duplicated().sum()
```

### CBOs duplicados

O campo `cod_cbo` é tratado como identificador único da ocupação.

O pipeline verifica quantos códigos CBO distintos aparecem mais de uma vez.

Exemplo:

```text
cod_cbo
100 → 3 ocorrências
200 → 1 ocorrência
300 → 2 ocorrências
```

Resultado:

```text
CBOs únicos duplicados: 2
```

Os CBOs `100` e `300` são contabilizados uma vez cada.

### Nomes ausentes

Registros que não possuem `nom_cbo` são removidos da camada processada.

---

# Estrutura do projeto

```text
occupations-data-pipeline/
│
├── data/
│   ├── raw/
│   │   └── cbo.csv
│   │
│   └── processed/
│       └── occupations_processed.csv
│
├── src/
│   └── ingest_occupations.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Tecnologias

* Python
* Pandas
* CSV
* Git / GitHub

## Como executar

Clone o repositório:

```bash
git clone <repository-url>
cd occupations-data-pipeline
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o pipeline:

```bash
python src/ingest_occupations.py
```

Também é possível filtrar as ocupações por uma palavra-chave:

```bash
python src/ingest_occupations.py --search engenheiro
```

O resultado será salvo em:

```text
data/processed/
```

## Exemplo de saída

```text
Registros recebidos: 13
Linhas duplicadas encontradas: 10
CBOs unicos duplicados: 3
Registros sem nome: 3
Registros após limpeza: 2
Registros descartados: 11
Registros após filtro: 2
Arquivo salvo em: data/processed/occupations_processed.csv
```

Os valores acima são apenas um exemplo utilizado para demonstrar as validações do pipeline.

---

# Próximas etapas

### Etapa 2

* Melhorar a camada de dados processados
* Introduzir Parquet
* Comparar CSV e Parquet
* Explorar características dos dados

### Etapa 3

* Modelagem relacional
* PostgreSQL
* Criação de tabelas
* Carga dos dados

### Etapa 4

* Consultas SQL
* Métricas
* Análises sobre as ocupações

### Etapa 5

* Docker
* Containerização do pipeline e PostgreSQL

### Etapa 6

* AWS S3
* Armazenamento dos dados na nuvem

### Etapa 7

* AWS RDS
* PostgreSQL gerenciado na AWS

### Etapa 8

* Terraform
* Infraestrutura como código

### Etapas futuras

* Kafka
* Streaming
* Processamento de fluxos
* Spark
* Processamento distribuído
* Enriquecimento dos dados com IA

---

# Status

🚧 Projeto em desenvolvimento.

**Etapa atual:** 1 — Ingestão e limpeza inicial dos dados.

O projeto será atualizado incrementalmente conforme novas etapas de Engenharia de Dados forem implementadas.
