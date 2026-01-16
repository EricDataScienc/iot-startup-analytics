import sqlite3
from pathlib import Path

DB_PATH = Path("data/app.db")


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tech_score (
            startup_id TEXT,
            startup_name TEXT,
            setor TEXT,
            status TEXT,
            data_avaliacao TEXT,
            score_1 REAL,
            score_2 REAL,
            score_3 REAL,
            score_4 REAL,
            score_5 REAL,
            score_6 REAL,
            score_7 REAL,
            score_8 REAL
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    print("Banco SQLite criado com sucesso.")
