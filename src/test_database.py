from database import get_connection


with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM occupations")
        rows = cur.fetchall()
        print(rows)