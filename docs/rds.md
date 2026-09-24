# Amazon RDS

## Objetivo

O projeto utiliza o Amazon RDS para executar uma instância PostgreSQL gerenciada na AWS.

O RDS representa a camada de banco de dados remoto do pipeline, enquanto o PostgreSQL em Docker continua disponível como ambiente local de desenvolvimento.

## Arquitetura

```text
API pública
    ↓
Python + Requests
    ↓
Pandas
    ↓
CSV / Parquet
    ↓
AWS S3
    ↓
Python + psycopg
    ↓
PostgreSQL
    ├── Local: Docker
    └── Remoto: Amazon RDS
```

## Configuração

O projeto utiliza diferentes arquivos de ambiente:

```text
.env
.env.rds
```

A escolha do ambiente é feita através da variável:

```text
APP_ENV
```

### Ambiente local

```text
APP_ENV=local
```

Utiliza o PostgreSQL executado pelo Docker Compose.

### Ambiente RDS

```text
APP_ENV=rds
```

Utiliza o PostgreSQL hospedado no Amazon RDS.

## PostgreSQL no RDS

Engine:

```text
PostgreSQL
```

Porta:

```text
5432
```

Região:

```text
sa-east-1
```

O acesso ao banco é controlado por um Security Group.

A regra de entrada utilizada durante o desenvolvimento permite conexões PostgreSQL somente a partir do IP autorizado do ambiente de desenvolvimento.

## SSL

A conexão com o RDS utiliza SSL/TLS.

O projeto utiliza:

```text
sslmode=verify-full
```

e o CA bundle da AWS:

```text
certs/global-bundle.pem
```

Esse certificado é utilizado para validar o certificado apresentado pela instância RDS.

## Teste de conexão

Com o ambiente local:

```powershell
$env:APP_ENV="local"
python src/test_connection.py
```

Com o RDS:

```powershell
$env:APP_ENV="rds"
python src/test_connection.py
```

O teste verifica a conexão e executa consultas simples para identificar o banco e o usuário utilizados.

## Carga dos dados

Os dados processados são carregados na tabela:

```text
occupations
```

A tabela utiliza `cod_cbo` como valor único para identificar a ocupação.

A carga pode ser executada novamente sem gerar registros duplicados.

## Validação

Depois da carga, a quantidade de registros pode ser validada com:

```sql
SELECT COUNT(*) AS total_occupations
FROM occupations;
```

Também é possível verificar a quantidade de códigos distintos:

```sql
SELECT COUNT(DISTINCT cod_cbo) AS distinct_cbo
FROM occupations;
```

A quantidade deve permanecer consistente entre execuções repetidas do pipeline.

## Local x RDS

O mesmo pipeline pode utilizar os dois bancos alterando apenas a configuração do ambiente.

```text
.env
 ↓
PostgreSQL Docker

.env.rds
 ↓
Amazon RDS
```

O código de conexão permanece o mesmo.

## Custos e encerramento

O RDS não deve permanecer executando desnecessariamente em um ambiente de estudos.

Para interromper temporariamente uma instância, no console:

```text
RDS
→ Databases
→ occupations-rds
→ Actions
→ Stop temporarily
```

A AWS não cobra pelas horas de execução da instância enquanto ela está parada, mas continuam existindo cobranças relacionadas a armazenamento provisionado, backups e IPv4 público quando aplicável. Uma instância parada também é reiniciada automaticamente depois de no máximo 7 dias.

Para eliminar definitivamente o recurso:

```text
RDS
→ Databases
→ occupations-rds
→ Actions
→ Delete
```

A exclusão remove os dados da instância. Antes de excluir, deve-se avaliar se é necessário criar um snapshot final. A proteção contra exclusão precisa estar desativada para que a instância possa ser excluída.

Para este projeto de aprendizado, quando o banco não for mais necessário, a opção de exclusão pode ser utilizada depois de garantir que os dados necessários estão preservados em outro local.

## Segurança

Nunca versionar:

```text
.env
.env.rds
```

Também não devem ser versionados:

* senhas;
* access keys;
* secret keys;
* tokens;
* credenciais de banco.

O arquivo `global-bundle.pem` não contém credenciais e pode permanecer versionado no projeto.
