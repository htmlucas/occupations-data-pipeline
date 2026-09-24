from pathlib import Path
import os

import psycopg
from dotenv import dotenv_values


BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

LOCAL_ENV = BASE_DIR / ".env"
RDS_ENV = BASE_DIR / ".env.rds"

SQL = {
    "total": """
        SELECT COUNT(*) AS value
        FROM occupations;
    """,

    "distinct_cbo": """
        SELECT COUNT(DISTINCT cod_cbo) AS value
        FROM occupations;
    """,

    "duplicate_cbo": """
        SELECT COUNT(*) AS value
        FROM (
            SELECT cod_cbo
            FROM occupations
            GROUP BY cod_cbo
            HAVING COUNT(*) > 1
        ) duplicated;
    """,

    "empty_names": """
        SELECT COUNT(*) AS value
        FROM occupations
        WHERE nome_cbo IS NULL
           OR TRIM(nome_cbo) = '';
    """
}


def get_connection(env_file):
    env = dotenv_values(env_file)

    connection_params = {
        "host": env.get("DB_HOST"),
        "port": env.get("DB_PORT"),
        "dbname": env.get("DB_DATABASE"),
        "user": env.get("DB_USERNAME"),
        "password": env.get("DB_PASSWORD"),
    }

    sslmode = env.get("DB_SSLMODE")

    if sslmode:
        connection_params["sslmode"] = sslmode

        sslrootcert = env.get("DB_SSLROOTCERT")

        if sslrootcert:
            connection_params["sslrootcert"] = str(
                BASE_DIR / sslrootcert
            )

    return psycopg.connect(**connection_params)


def execute_query(conn, query):
    with conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()[0]


def collect_database_data(name, env_file):
    print(f"Consultando {name}...")

    with get_connection(env_file) as conn:
        return {
            "database": name,
            "total": execute_query(conn, SQL["total"]),
            "distinct_cbo": execute_query(conn, SQL["distinct_cbo"]),
            "duplicate_cbo": execute_query(conn, SQL["duplicate_cbo"]),
            "empty_names": execute_query(conn, SQL["empty_names"]),
        }


def compare(local, rds):
    comparison = {
        "total": local["total"] == rds["total"],
        "distinct_cbo": local["distinct_cbo"] == rds["distinct_cbo"],
        "duplicate_cbo": local["duplicate_cbo"] == rds["duplicate_cbo"],
        "empty_names": local["empty_names"] == rds["empty_names"],
    }

    return comparison


def generate_report(local, rds, comparison):
    report_file = REPORTS_DIR / "database_comparison.md"

    status = lambda value: "✅ Igual" if value else "❌ Diferente"

    content = f"""# Comparação entre PostgreSQL Local e Amazon RDS

## Objetivo

Comparar os dados armazenados no PostgreSQL local e no PostgreSQL hospedado no Amazon RDS.

A comparação utiliza as mesmas consultas de validação nos dois ambientes.

## Resultados

| Métrica | PostgreSQL Local | Amazon RDS | Resultado |
|---|---:|---:|---|
| Total de registros | {local["total"]} | {rds["total"]} | {status(comparison["total"])} |
| CBOs distintos | {local["distinct_cbo"]} | {rds["distinct_cbo"]} | {status(comparison["distinct_cbo"])} |
| CBOs duplicados | {local["duplicate_cbo"]} | {rds["duplicate_cbo"]} | {status(comparison["duplicate_cbo"])} |
| Nomes nulos/vazios | {local["empty_names"]} | {rds["empty_names"]} | {status(comparison["empty_names"])} |

## Interpretação

A comparação verifica se os dois ambientes possuem o mesmo estado dos dados carregados.

### PostgreSQL Local

- Total de registros: **{local["total"]}**
- CBOs distintos: **{local["distinct_cbo"]}**
- CBOs duplicados: **{local["duplicate_cbo"]}**
- Nomes nulos/vazios: **{local["empty_names"]}**

### Amazon RDS

- Total de registros: **{rds["total"]}**
- CBOs distintos: **{rds["distinct_cbo"]}**
- CBOs duplicados: **{rds["duplicate_cbo"]}**
- Nomes nulos/vazios: **{rds["empty_names"]}**

## Conclusão

"""

    if all(comparison.values()):
        content += (
            "Os dois ambientes apresentaram os mesmos resultados para "
            "as validações realizadas."
        )
    else:
        content += (
            "Foram encontradas diferenças entre os ambientes. "
            "É necessário investigar as métricas marcadas como diferentes."
        )

    report_file.write_text(content, encoding="utf-8")

    print(f"\nRelatório salvo em: {report_file}")


def main():
    local = collect_database_data(
        "PostgreSQL Local",
        LOCAL_ENV
    )

    rds = collect_database_data(
        "Amazon RDS",
        RDS_ENV
    )

    comparison = compare(local, rds)

    print("\n=== Comparação ===")
    print(f"Total de registros: {local['total']} == {rds['total']}")
    print(
        f"CBOs distintos: "
        f"{local['distinct_cbo']} == {rds['distinct_cbo']}"
    )
    print(
        f"CBOs duplicados: "
        f"{local['duplicate_cbo']} == {rds['duplicate_cbo']}"
    )
    print(
        f"Nomes nulos/vazios: "
        f"{local['empty_names']} == {rds['empty_names']}"
    )

    generate_report(local, rds, comparison)


if __name__ == "__main__":
    main()