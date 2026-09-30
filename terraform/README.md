# Terraform — Occupations Data Pipeline

Infraestrutura como código (IaC) utilizada para gerenciar a infraestrutura AWS do projeto `occupations-data-pipeline`.

## Objetivo

Aprender Terraform na prática utilizando o próprio pipeline como projeto de estudo.

O Terraform é utilizado para declarar e gerenciar recursos de infraestrutura, permitindo visualizar as alterações antes de aplicá-las.

## O que foi feito

- Instalar o Terraform;
- Criar uma pasta `terraform/`;
- Configurar o provider AWS;
- Utilizar as credenciais configuradas na AWS CLI;
- Definir a região por variável;
- Gerenciar um bucket S3 existente;
- Importar o bucket S3 existente para o Terraform State;
- Habilitar versionamento do bucket;
- Configurar criptografia server-side com AES256;
- Bloquear acesso público ao bucket;
- Utilizar variáveis para:
  - região;
  - nome do bucket;
- Criar um `outputs.tf`;
- Criar um `terraform.tfvars.example`;
- Configurar `.gitignore` para arquivos locais e de state;
- Executar:
  - `terraform init`;
  - `terraform fmt`;
  - `terraform validate`;
  - `terraform plan`;
  - `terraform apply`;
  - `terraform output`;
- Validar a infraestrutura criada através do Terraform;
- Documentar o processo.

## Infraestrutura

Atualmente o Terraform gerencia um bucket S3 utilizado pelo projeto.

### S3

O bucket possui:

- Versionamento habilitado;
- Criptografia server-side com AES256;
- Bloqueio de acesso público.

Bucket utilizado:

```text
occupations-data-pipeline-lucas-2026
```

## Estrutura

```text
terraform/
├── .gitignore
├── .terraform.lock.hcl
├── README.md
├── main.tf
├── outputs.tf
├── terraform.tfvars.example
└── variables.tf
```

Arquivos utilizados localmente, mas não versionados:

```text
terraform/
├── .terraform/
├── terraform.tfstate
├── terraform.tfstate.*
└── terraform.tfvars
```

## Variáveis

As variáveis utilizadas pelo projeto são declaradas em `variables.tf`.

Atualmente:

- `aws_region`: região AWS utilizada pela infraestrutura;
- `bucket_name`: nome do bucket S3.

Exemplo:

```hcl
aws_region  = "sa-east-1"
bucket_name = "occupations-data-pipeline-lucas-2026"
```

O arquivo `terraform.tfvars` não é versionado.

Para facilitar a configuração de quem clonar o projeto, existe o arquivo:

```text
terraform.tfvars.example
```

## Pré-requisitos

- Terraform;
- AWS CLI;
- Credenciais AWS configuradas.

Verificar o Terraform:

```powershell
terraform version
```

Verificar a AWS CLI:

```powershell
aws --version
```

Verificar a autenticação na AWS:

```powershell
aws sts get-caller-identity
```

## Inicialização

Dentro da pasta `terraform`:

```powershell
terraform init
```

O comando inicializa o diretório de trabalho e instala os providers necessários.

## Formatação

Para formatar os arquivos Terraform:

```powershell
terraform fmt
```

## Validação

Para verificar se a configuração está sintaticamente válida:

```powershell
terraform validate
```

## Planejamento

Para visualizar as alterações que o Terraform pretende realizar:

```powershell
terraform plan
```

O `plan` não altera a infraestrutura.

Ele apenas apresenta o que seria criado, alterado ou destruído.

Antes de executar `terraform apply`, o plano deve ser revisado.

## Aplicação

Para aplicar as alterações:

```powershell
terraform apply
```

O Terraform solicitará confirmação antes de realizar as alterações.

## Outputs

Os outputs definidos em `outputs.tf` podem ser consultados com:

```powershell
terraform output
```

Atualmente são disponibilizados:

- nome do bucket;
- ARN do bucket.

## Importação de recursos existentes

O bucket S3 já existia antes de ser gerenciado pelo Terraform.

Por isso, foi utilizada a importação:

```powershell
terraform import aws_s3_bucket.occupations occupations-data-pipeline-lucas-2026
```

A importação associa um recurso existente ao Terraform State.

Ela não cria um novo recurso.

Depois da importação, o comando:

```powershell
terraform plan
```

pode ser utilizado para verificar se a configuração Terraform corresponde ao recurso existente.

## Terraform State

O arquivo `terraform.tfstate` mantém o estado conhecido pelo Terraform sobre os recursos que ele gerencia.

Neste projeto, o state não é versionado no Git.

O `.gitignore` impede o envio de:

```text
.terraform/
*.tfstate
*.tfstate.*
*.tfvars
```

O State é importante porque permite ao Terraform comparar:

```text
Configuração Terraform
        ↓
Terraform State
        ↓
Infraestrutura existente na AWS
```

e determinar quais alterações precisam ser realizadas.

## Segurança

As credenciais da AWS não são armazenadas nos arquivos `.tf`.

A autenticação utilizada pelo Terraform é feita através das credenciais configuradas na AWS CLI.

Também não são versionados:

- `terraform.tfstate`;
- arquivos auxiliares do state;
- `terraform.tfvars`;
- `.terraform/`.

O arquivo `terraform.tfvars.example` contém apenas valores de exemplo e pode ser versionado.

## Git

O projeto utiliza `.gitignore` para evitar o versionamento de arquivos locais e informações que não devem ser armazenadas no repositório.

Exemplo:

```gitignore
.terraform/
*.tfstate
*.tfstate.*
*.tfvars
```

O arquivo `.terraform.lock.hcl` é versionado, pois registra as versões dos providers utilizadas pelo projeto.

## RDS

O projeto inicialmente previa declarar um RDS PostgreSQL e um Security Group utilizando Terraform.

Essa etapa foi retirada temporariamente para evitar custos durante o aprendizado.

O Terraform atualmente gerencia apenas os recursos necessários para esta etapa do projeto.

## Relação com o pipeline

O Terraform não executa o pipeline Python.

As responsabilidades são separadas:

```text
Python / Pandas
       ↓
Processamento dos dados
       ↓
Terraform
       ↓
Infraestrutura AWS
       ↓
S3
```

O objetivo inicial é entender e controlar a infraestrutura com Terraform.

A integração entre o pipeline Python e a infraestrutura pode ser adicionada posteriormente.

## Validação da infraestrutura

Depois de aplicar as configurações, os recursos podem ser verificados através dos comandos do Terraform:

```powershell
terraform plan
```

e:

```powershell
terraform output
```

O objetivo é garantir que:

- o bucket existe;
- o Terraform reconhece o recurso;
- não existem alterações pendentes inesperadas;
- os outputs retornam as informações esperadas.

## Comandos principais

```powershell
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
terraform output
terraform destroy
```

> `terraform destroy` deve ser utilizado com cuidado, principalmente quando o Terraform estiver gerenciando recursos com dados importantes.

## Evolução

O Terraform faz parte da evolução do projeto `occupations-data-pipeline`.

O projeto começou com processamento local dos dados de ocupações e foi evoluindo para diferentes etapas de armazenamento, processamento e infraestrutura.

A utilização do Terraform adiciona uma camada de Infrastructure as Code (IaC), permitindo que parte da infraestrutura do projeto seja declarada, versionada e reproduzida através de código.

## Próximos passos

- Continuar aprimorando a organização dos arquivos Terraform;
- Explorar melhor variáveis e outputs;
- Aprofundar o entendimento sobre Terraform State;
- Avaliar gerenciamento remoto de State no futuro;
- Evoluir a infraestrutura conforme o pipeline crescer;
- Integrar o pipeline Python com a infraestrutura AWS em uma etapa posterior.

## Custos

Recursos AWS pagos não serão criados apenas para fins de aprendizado sem necessidade.

O RDS PostgreSQL foi deixado fora desta etapa para evitar custos recorrentes durante o desenvolvimento.

O foco atual é aprender Terraform utilizando recursos AWS necessários e de baixo custo para o projeto.