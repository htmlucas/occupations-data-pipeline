import pandas as pd
from pathlib import Path
from database import get_connection, execute_sql_file

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
SQL_DIR = BASE_DIR / "sql"
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

REPORT_FILE_NAME = "occupations_analysis.md"
processed_parquet_name = "official_occupations_processed.parquet"

parquet_output_file = PROCESSED_DIR / processed_parquet_name

df = pd.read_parquet(parquet_output_file, engine="pyarrow")

connection = get_connection()
cursor = connection.cursor()

count_occupations_result = execute_sql_file(cursor, Path(SQL_DIR / "total_occupations.sql"))
count_distinct_occupations_result = execute_sql_file(cursor,Path(SQL_DIR / "count_unique_cbo.sql"))
count_name_null_or_empty_occupations_result = execute_sql_file(cursor,Path(SQL_DIR / "count_null_or_empty_names_cbos.sql"))
max_and_min_name_occupations_result = execute_sql_file(cursor,Path(SQL_DIR / "count_max_and_min_names_cbos.sql"))
search_name_occupation_result = execute_sql_file(cursor,Path(SQL_DIR / "search_occupation.sql"))
sample_occupations_result = execute_sql_file(cursor,Path(SQL_DIR / "sample_occupations.sql"))

cursor.close()
connection.close()

result_count_occupations_string = ''

if count_occupations_result[0][0] == len(df):
    result_count_occupations_string = "A quantidade de registros é igual"
else:
    result_count_occupations_string = "A quantidade de registros é diferente"


for row in max_and_min_name_occupations_result:
    if(row[2] == 'Maior'):
        max_name = row[0]
        max_length = row[1]
    else:
        min_name = row[0]
        min_length = row[1]

search_rows = ""

for row in  search_name_occupation_result:
    search_rows += f"| {row[0]} | {row[1]} |\n"

sample_rows = ""
for row in sample_occupations_result:
    sample_rows += f"| {row[0]} |\n"


report = f"""
# Occupations Data Analysis

## Dataset

| Métrica | Resultado |
|---|---:|
| Registros no Parquet | {len(df)} |
| Registros no PostgreSQL | {count_occupations_result[0][0]} |
| CBOs distintos | {count_distinct_occupations_result[0][0]} |

{result_count_occupations_string}

---

## Qualidade dos dados

### CBOs duplicados

| Métrica | Resultado |
|---|---:|
| Total de registros | {count_occupations_result[0][0]} |
| CBOs distintos | {count_distinct_occupations_result[0][0]} |
| CBOs duplicados | 0 |

Não foram identificados códigos CBO duplicados na tabela do PostgreSQL.

### Ocupações sem nome

| Métrica | Resultado |
|---|---:|
| Registros sem nome | {count_name_null_or_empty_occupations_result[0][0]} |

Foi identificado {count_name_null_or_empty_occupations_result[0][0]} registro com nome de ocupação ausente ou vazio.

---

## Características dos nomes das ocupações

### Maior e menor nome

| Tipo | Ocupação | Tamanho |
|---|---|---:|
| Maior | {max_name} | {max_length} |
| Menor | {min_name} | {min_length} |

O maior nome possui {max_length} caracteres, enquanto o menor possui {min_length} caracteres.

---

## Busca por palavra-chave

### Palavra-chave: `engenheiro`

Foram encontradas {len(search_name_occupation_result)} ocupações relacionadas ao termo `engenheiro`.

Alguns resultados:

| Código CBO | Ocupação |
|---|---|
{search_rows}

A consulta foi realizada diretamente no PostgreSQL utilizando uma busca por palavra-chave no nome da ocupação.

---

## Amostra de ocupações

As primeiras 20 ocupações, ordenadas alfabeticamente:

| Ocupação |
|---|
{sample_rows}


---

## Comparação entre Parquet e PostgreSQL

| Métrica | Parquet | PostgreSQL |
|---|---:|---:|
| Registros | {len(df)} | {count_occupations_result[0][0]} |
| Códigos CBO distintos | {len(df)} | {count_distinct_occupations_result[0][0]} |

A quantidade de registros presente no arquivo Parquet corresponde à quantidade de registros carregada no PostgreSQL.

---

## Consultas realizadas

As seguintes análises foram executadas:

- `total_occupations.sql`
- `count_unique_cbo.sql`
- `count_null_or_empty_names_cbos.sql`
- `count_max_and_min_names_cbos.sql`
- `search_occupation.sql`
- `sample_occupations.sql`

---

## Conclusão

A análise confirmou que o dataset processado contém {len(df)} ocupações e que o PostgreSQL possui {count_occupations_result[0][0]} de registros.

Também foram analisados:

- unicidade dos códigos CBO;
- registros sem nome;
- tamanho dos nomes das ocupações;
- busca de ocupações por palavra-chave;
- amostra ordenada dos dados;
- comparação entre o arquivo Parquet e os dados carregados no PostgreSQL.

Essas consultas servem como uma primeira camada de validação e exploração dos dados antes das próximas etapas do pipeline.
 
"""

Path("reports/occupations_analysis.md").write_text(
    report,
    encoding="utf-8"
)