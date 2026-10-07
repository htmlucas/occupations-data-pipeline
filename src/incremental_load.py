from database import get_connection
import pandas as pd

def incremental_load(new_occupations):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT cod_cbo, nome_cbo FROM occupations")
            rows = cur.fetchall()

            load_occupations = pd.DataFrame(
                rows,
                columns=["CODIGO", "TITULO"]
            )

            new_occupations["CODIGO"] = new_occupations["CODIGO"].astype(str)
            load_occupations["CODIGO"] = load_occupations["CODIGO"].astype(str)

            comparison = new_occupations.merge(
                load_occupations,
                on="CODIGO",
                how="inner",
                suffixes=("_novo", "_atual")
            )


            unchanged = comparison[
                comparison["TITULO_novo"] == comparison["TITULO_atual"]
                ]

            updated = comparison[
                comparison["TITULO_novo"] != comparison["TITULO_atual"]
                ]

            news = new_occupations[
                ~new_occupations["CODIGO"].isin(load_occupations["CODIGO"])
            ]

            print('unchanged',unchanged)
            print('updated',updated)
            print('news',news)


            if not news.empty:
                for _, row in news.iterrows():
                    cur.execute(
                        """
                        INSERT INTO occupations (
                            cod_cbo,
                            nome_cbo
                        )
                        VALUES (%s, %s)
                        """,
                        (row['CODIGO'], row['TITULO'])
                    )

            if not updated.empty:
                for _, row in updated.iterrows():
                    cur.execute(
                        """
                        UPDATE occupations 
                        SET nome_cbo = %s
                        WHERE cod_cbo = %s
                        """,
                        (row['TITULO_novo'], row["CODIGO"])
                    )