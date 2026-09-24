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
# Etapa 1 (Primeiro Ingestão de dados via arquivo)
Comecei um projeto contínuo de Engenharia de Dados utilizando dados de ocupações profissionais.

Nesta primeira etapa, construí uma rotina em Python que consome uma fonte pública, transforma os registros em um DataFrame com Pandas, valida duplicidades e campos obrigatórios e salva os dados em camadas raw e processed.

Próximos passos: persistir os dados em PostgreSQL, criar consultas analíticas e preparar o pipeline para evoluir posteriormente para cloud e infraestrutura como código.
# Etapa 2 (Ingestão de Dados via API)
Evoluí meu pipeline de dados sobre ocupações profissionais para consumir uma API pública usando Python e Requests. A resposta original agora é preservada na camada raw, enquanto o Pandas realiza a transformação, validação e geração da camada processada.

Nesta etapa pratiquei ingestão via API, tratamento de erros, conversão de JSON para DataFrame e regras de qualidade como unicidade do código CBO e remoção de registros sem nome.
# Etapa 3 (Comparação entre Parquet, Json e CSV)
Evoluí meu pipeline de dados sobre ocupações profissionais para trabalhar com diferentes formatos de armazenamento.

A resposta original da API continua sendo preservada em JSON na camada raw, enquanto os dados processados agora são exportados em CSV e Parquet.

Também implementei uma comparação entre os formatos considerando registros, colunas e tamanho dos arquivos.

Com isso, avancei na compreensão de como pipelines reais organizam dados brutos e processados para diferentes objetivos de integração, inspeção e análise.

Próximo passo: modelar esses dados em PostgreSQL.
# Etapa 4 (Persistir dados no PostgreSQL)
Evoluí meu pipeline de dados sobre ocupações profissionais para utilizar o PostgreSQL como camada de armazenamento persistente.

O fluxo agora realiza a ingestão via API pública, processa os dados com Pandas, gera os arquivos tratados e carrega os registros em uma tabela relacional.

Também implementei validações para evitar duplicidade de códigos CBO em execuções repetidas e realizei consultas SQL para conferir a consistência da carga.

Com essa etapa, comecei a conectar as fases de ingestão, transformação e armazenamento em banco dentro do mesmo pipeline.

Próximo passo: construir consultas analíticas sobre os dados carregados.
# Etapa 5 (Consultas Análiticas)
Evoluí meu pipeline de dados sobre ocupações profissionais para além da ingestão e do armazenamento.

Nesta etapa, criei consultas analíticas em PostgreSQL para medir a quantidade de ocupações, validar a consistência dos registros, pesquisar padrões nos nomes e comparar os dados armazenados com os arquivos processados.

Também integrei essas consultas com Python para gerar resultados de forma reproduzível.

O projeto agora já cobre ingestão, transformação, persistência e uma primeira camada de análise.

Próximo passo: preparar o ambiente com Docker para tornar a execução mais reproduzível.
# Etapa 6 (Docker)
Evoluí meu pipeline de dados sobre ocupações profissionais para um ambiente reproduzível com Docker.

Agora o projeto sobe o PostgreSQL e o pipeline Python em containers, utilizando variáveis de ambiente, volume persistente e comunicação entre serviços.

Com isso, reduzi a dependência da configuração local e aproximei o projeto de um cenário mais próximo do desenvolvimento profissional.

O fluxo já contempla ingestão via API, transformação com Pandas, geração de arquivos, carga no PostgreSQL e consultas analíticas.

Próximo passo: preparar a organização dos dados para armazenamento em cloud com AWS S3.

# Etapa 7 (Armazenamento no Bucket S3 da Amazon)
Evoluí meu pipeline de dados sobre ocupações profissionais para utilizar o Amazon S3 como camada de armazenamento em nuvem.

O projeto agora organiza os arquivos em camadas raw, processed e reports, mantendo a separação entre dados brutos, dados tratados e resultados das execuções.

Também implementei o upload dos arquivos utilizando Python e boto3 e adicionei histórico de execução: cada execução do pipeline recebe um identificador (run_id), permitindo manter versões diferentes dos dados no S3 em vez de sobrescrever a execução anterior.

Na prática, cada execução passa a gerar uma estrutura como:

raw/<run_id>/
processed/<run_id>/
reports/<run_id>/

Essa etapa foi importante para entender, na prática, a diferença entre armazenamento de objetos em cloud e persistência relacional em PostgreSQL, além de trabalhar com versionamento lógico e histórico de execuções.

# Etapa 8 (Integração do Pipeline com o Amazon RDS)
Amazon RDS

O pipeline possui suporte a PostgreSQL local e PostgreSQL hospedado no Amazon RDS.

O ambiente utilizado pode ser selecionado através da variável APP_ENV:

APP_ENV=local

utiliza o PostgreSQL executado pelo Docker.

APP_ENV=rds

utiliza a instância PostgreSQL no Amazon RDS.

O projeto utiliza conexão SSL para o RDS e mantém as credenciais fora do código-fonte através de arquivos de ambiente não versionados.

Fluxo
API
 ↓
Python + Pandas
 ↓
CSV / Parquet
 ↓
S3
 ↓
PostgreSQL
 ├── Docker
 └── Amazon RDS
Testar conexão

PostgreSQL local:

$env:APP_ENV="local"
python src/test_connection.py

Amazon RDS:

$env:APP_ENV="rds"
python src/test_connection.py
Carga

A mesma rotina de carga pode ser executada em ambos os ambientes. O destino é definido através do ambiente configurado.

A carga utiliza cod_cbo como identificador único e pode ser reexecutada sem gerar registros duplicados.

Documentação

A configuração detalhada do Amazon RDS está disponível em docs/rds.md.

## Comparação entre PostgreSQL Local e Amazon RDS

O projeto possui uma rotina que executa as mesmas validações nos bancos local e remoto e gera um relatório comparativo em `reports/database_comparison.md`.

As validações incluem quantidade de registros, quantidade de CBOs distintos, duplicidades e nomes nulos ou vazios.