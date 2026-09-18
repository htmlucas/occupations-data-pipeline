from pathlib import Path

from database import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent
SQL_FILE = BASE_DIR / "sql" / "create_tables.sql"

sql = SQL_FILE.read_text(encoding="utf-8")

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute(sql)

print("Tabelas criadas com sucesso!")