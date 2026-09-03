# Occupations Data Pipeline

Pipeline de Engenharia de Dados desenvolvido de forma incremental para ingestão, transformação, validação, armazenamento e análise de dados sobre ocupações profissionais.

O projeto utiliza dados relacionados à **Classificação Brasileira de Ocupações (CBO)** como fonte principal e será evoluído gradualmente para trabalhar com diferentes formatos de dados, bancos de dados, cloud e processamento de dados em maior escala.

## Objetivo

Construir um pipeline de dados sobre ocupações profissionais que possa futuramente disponibilizar informações como:

- Código da ocupação
- Nome da ocupação
- Nomes similares
- Descrição
- Skills e conhecimentos
- Certificações
- Ocupações relacionadas
- Outros dados relevantes para análise

O foco do projeto é praticar conceitos de **Engenharia de Dados**, como:

- Ingestão
- Transformação
- Qualidade de dados
- Validação
- Armazenamento
- Modelagem
- SQL
- Análise
- Arquitetura de dados

---

## Evolução do projeto

O projeto será desenvolvido em etapas, aumentando gradualmente a complexidade:

```text
API pública
    ↓
Python + Requests
    ↓
Pandas / DataFrames
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

A ordem poderá ser ajustada conforme os requisitos e aprendizados de cada etapa.

---

## Etapa 1 — Ingestão e limpeza inicial

Na primeira etapa, o projeto utilizava um arquivo CSV contendo dados de ocupações como fonte local.

O pipeline realizava:

- leitura do CSV com Pandas;
- remoção de linhas completamente duplicadas;
- identificação de CBOs duplicados;
- remoção de registros sem nome de ocupação;
- filtro opcional por palavra-chave;
- geração de um CSV processado.

### Fluxo inicial

```text
CSV
 ↓
Pandas
 ↓
Validação
 ↓
Limpeza
 ↓
CSV processado
```

---

## Etapa 2 — Ingestão via API

Na segunda etapa, o pipeline passou a realizar a ingestão dos dados através de uma **API pública**, utilizando Python e Requests.

O objetivo foi simular um cenário mais próximo de um pipeline real, no qual os dados precisam ser coletados de uma fonte externa.

### Fluxo atual

```text
API pública
     ↓
Python + Requests
     ↓
JSON bruto
     ↓
Pandas / DataFrame
     ↓
Validação
     ↓
Transformação
     ↓
CSV processado
```

A resposta original da API é preservada na camada `raw`, enquanto os dados tratados são armazenados na camada `processed`.

### Tratamento de erros

A ingestão possui tratamento para situações relacionadas à comunicação com a API, incluindo:

- erros de conexão;
- erros HTTP;
- respostas inválidas;
- falhas durante a requisição.

As respostas HTTP são validadas antes do processamento dos dados.

---

## Qualidade dos dados

Durante o processamento são realizadas validações para identificar problemas na origem dos dados.

### Registros duplicados

São identificadas linhas completamente duplicadas utilizando os registros presentes no DataFrame.

### CBOs duplicados

O campo `cod_cbo` é tratado como identificador único da ocupação.

A validação contabiliza quantos **CBOs distintos aparecem mais de uma vez**, independentemente da quantidade de ocorrências.

Por exemplo:

```text
100 → 3 ocorrências
200 → 1 ocorrência
300 → 2 ocorrências
```

Resultado:

```text
CBOs únicos duplicados: 2
```

Os CBOs `100` e `300` são contabilizados uma vez cada.

### Registros sem nome

Registros que não possuem nome da ocupação são removidos da camada processada.

---

## Camadas de dados

O projeto utiliza uma separação simples entre os dados recebidos e os dados processados.

```text
data/
│
├── raw/
│   └── dados recebidos da fonte
│
└── processed/
    └── dados tratados
```

### Raw

Contém os dados originais recebidos da fonte.

Essa camada deve permanecer **inalterada**, permitindo que os dados originais possam ser utilizados novamente caso as regras de transformação sejam modificadas.

### Processed

Contém os dados após as etapas de:

- validação;
- limpeza;
- remoção de registros inválidos;
- remoção de duplicidades;
- aplicação de filtros.

---

## Estrutura do projeto

```text
occupations-data-pipeline/
│
├── data/
│   ├── raw/
│   │   ├── cbo.csv
│   │   └── ...
│   │
│   └── processed/
│       └── occupations_processed.csv
│
├── src/
│   └── ingest_occupations.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Tecnologias utilizadas

### Atualmente

- Python
- Requests
- Pandas
- CSV
- JSON
- Git
- GitHub

### Futuramente

- Parquet
- PostgreSQL
- SQL
- Docker
- AWS S3
- AWS RDS
- Terraform
- Kafka
- Spark

---

## Como executar

Clone o projeto:

```bash
git clone <repository-url>
cd occupations-data-pipeline
```

Crie um ambiente virtual:

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

Para realizar uma busca por palavra-chave:

```bash
python src/ingest_occupations.py --search engenheiro
```

---

## Exemplo de execução

```text
Registros recebidos: 13
Linhas duplicadas encontradas: 10
CBOs únicos duplicados: 3
Registros sem nome: 3
Registros após limpeza: 2
Registros descartados: 11
Registros após filtro: 2
Arquivo salvo em: data/processed/occupations_processed.csv
```

Os valores acima representam apenas um conjunto de testes utilizado durante o desenvolvimento e não representam necessariamente a quantidade de registros existente na fonte oficial.

---

## Próximas etapas

### Etapa 3 — CSV, JSON e Parquet

Trabalhar com diferentes formatos de armazenamento e entender quando cada um é mais adequado.

Objetivos:

- trabalhar com CSV;
- trabalhar com JSON;
- introduzir o formato Parquet;
- comparar tamanho dos arquivos;
- comparar estrutura dos dados;
- ler os arquivos novamente utilizando Pandas;
- validar se os dados permanecem consistentes após a conversão.

Fluxo esperado:

```text
API
 ↓
JSON Raw
 ↓
Pandas / DataFrame
 ↓
Validação
 ↓
CSV
 ↓
Parquet
```

### Etapa 4 — PostgreSQL

- Modelagem relacional;
- criação das tabelas;
- definição de chaves;
- carga dos dados;
- constraints;
- integridade dos dados;
- conexão do pipeline com o banco.

### Etapa 5 — SQL e Analytics

- consultas analíticas;
- agregações;
- métricas;
- análise das ocupações;
- criação de indicadores;
- exploração dos dados utilizando SQL.

### Etapa 6 — Docker

- Containerização do pipeline;
- PostgreSQL em container;
- configuração do ambiente;
- execução reproduzível do projeto.

### Etapa 7 — AWS S3

- armazenamento dos dados na nuvem;
- organização dos dados por camadas;
- introdução ao conceito de Data Lake;
- integração do pipeline com armazenamento em cloud.

### Etapa 8 — AWS RDS

- utilização de PostgreSQL gerenciado;
- conexão do pipeline com banco remoto;
- separação entre aplicação, banco e infraestrutura.

### Etapa 9 — Terraform

- Infraestrutura como código;
- provisionamento dos recursos utilizados pelo projeto;
- configuração reproduzível da infraestrutura.

### Etapas futuras

Após a construção do pipeline principal, o projeto poderá evoluir para:

- Kafka;
- processamento de streaming;
- Apache NiFi;
- Spark;
- processamento distribuído;
- enriquecimento das informações das ocupações;
- geração de dados adicionais utilizando IA.

---

## Status

🚧 Em desenvolvimento

**Etapa atual:** 2 — Ingestão de dados via API pública.

O projeto está sendo desenvolvido incrementalmente como parte de uma jornada prática de aprendizado em Engenharia de Dados.