import duckdb
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/app.duckdb")
CSV_PATH = Path("data/startups.csv")


def seed_database():
    if not CSV_PATH.exists():
        raise FileNotFoundError("Arquivo startups.csv não encontrado em /data")

    conn = duckdb.connect(DB_PATH)

    # Verifica se a tabela já tem dados
    tables = conn.execute("SHOW TABLES").fetchall()
    if ("tech_score",) in tables:
        count = conn.execute("SELECT COUNT(*) FROM tech_score").fetchone()[0]
        if count > 0:
            print("Banco já populado. Seed ignorado.")
            conn.close()
            return

    print("Populando banco com dados do CSV...")

    df = pd.read_csv(CSV_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tech_score AS
        SELECT * FROM df
    """)

    print(f"{len(df)} registros inseridos com sucesso.")
    conn.close()


if __name__ == "__main__":
    seed_database()
