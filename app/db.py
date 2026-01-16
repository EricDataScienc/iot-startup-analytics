import sqlite3
from pathlib import Path

DB_PATH = Path("data/app.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


if __name__ == "__main__":
    conn = get_connection()
    conn.close()
    print("Banco SQLite inicializado com sucesso.")
