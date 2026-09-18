import psycopg
import os
from dotenv import load_dotenv

# Carregar variaveis do .env
load_dotenv()

def get_connection():
    return psycopg.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
    )

def execute_sql_file(cursor, sql_file):
    query = sql_file.read_text(encoding="utf-8")
    cursor.execute(query)
    return cursor.fetchall()