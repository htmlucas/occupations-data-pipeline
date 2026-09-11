import pandas as pd
from pathlib import Path
from database import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
processed_parquet_name = "official_occupations_processed.parquet"
parquet_output_file = PROCESSED_DIR / processed_parquet_name

df = pd.read_parquet(parquet_output_file, engine="pyarrow")

tuplas = list(df.itertuples(index=False, name=None))
print(len(tuplas))

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO occupations (cod_cbo, nome_cbo)
            VALUES (%s, %s)
            ON CONFLICT (cod_cbo) DO NOTHING
            """,
            tuplas
        )
        cur.execute("SELECT * FROM occupations")
        query = cur.fetchall()
        quantidade_apos_carga = len(query)
        print("Quantidade de registros no arquivo de origem:", len(df))
        print("Quantidade de registros inseridos", len(tuplas))
        print("Quantidade de registros apos carga", quantidade_apos_carga)