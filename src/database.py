import psycopg
import os

from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Carregar variaveis do .env
env_file = ".env.rds" if os.getenv("APP_ENV") == "rds" else ".env"
load_dotenv(BASE_DIR / env_file)

def get_connection():
    connection_params = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "dbname": os.getenv("DB_DATABASE"),
        "user": os.getenv("DB_USERNAME"),
        "password": os.getenv("DB_PASSWORD"),
    }

    sslmode = os.getenv("DB_SSLMODE")

    if sslmode:
        connection_params["sslmode"] = sslmode
        sslrootcert = os.getenv("DB_SSLROOTCERT")

        if sslrootcert:
            connection_params["sslrootcert"] = str(BASE_DIR / sslrootcert)
    return psycopg.connect(**connection_params)

def execute_sql_file(cursor, sql_file):
    query = sql_file.read_text(encoding="utf-8")
    cursor.execute(query)

    if cursor.description is not None:
        return cursor.fetchall()

    return None