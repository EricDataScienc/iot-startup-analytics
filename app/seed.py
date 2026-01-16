import os
import sqlite3
import pandas as pd

# Caminhos do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")
CSV_PATH = os.path.join(BASE_DIR, "data", "startups.csv")

# Conexão com o banco
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Recriar tabela
cursor.execute("DROP TABLE IF EXISTS tech_score")
cursor.execute("""
CREATE TABLE tech_score (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    startup_name TEXT,
    setor TEXT,
    tech_score REAL,
    performance REAL,
    viabilidade REAL,
    confiabilidade REAL,
    usabilidade REAL,
    energia REAL,
    fisico REAL,
    conectividade REAL,
    ciclo_vida REAL
)
""")

print("Lendo CSV...")
df = pd.read_csv(CSV_PATH)

# Normalizar colunas
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
)

# Colunas técnicas (1.x até 8.x)
tech_columns = [col for col in df.columns if col[0].isdigit()]

print(f"Calculando Tech Score usando {len(tech_columns)} métricas...")

# Score global
df["tech_score"] = df[tech_columns].mean(axis=1)

# Mapeamento por dimensão
group_map = {
    "performance": [c for c in df.columns if c.startswith("1.")],
    "viabilidade": [c for c in df.columns if c.startswith("2.")],
    "confiabilidade": [c for c in df.columns if c.startswith("3.")],
    "usabilidade": [c for c in df.columns if c.startswith("4.")],
    "energia": [c for c in df.columns if c.startswith("5.")],
    "fisico": [c for c in df.columns if c.startswith("6.")],
    "conectividade": [c for c in df.columns if c.startswith("7.")],
    "ciclo_vida": [c for c in df.columns if c.startswith("8.")]
}

# Calcular médias por dimensão
for group, cols in group_map.items():
    df[group] = df[cols].mean(axis=1)

print("Inserindo dados no banco...")

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO tech_score (
            startup_name, setor, tech_score,
            performance, viabilidade, confiabilidade,
            usabilidade, energia, fisico,
            conectividade, ciclo_vida
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["nome_startup"],
        row["setor"],
        round(row["tech_score"], 2),
        round(row["performance"], 2),
        round(row["viabilidade"], 2),
        round(row["confiabilidade"], 2),
        round(row["usabilidade"], 2),
        round(row["energia"], 2),
        round(row["fisico"], 2),
        round(row["conectividade"], 2),
        round(row["ciclo_vida"], 2)
    ))

conn.commit()
conn.close()

print("Seed finalizado com sucesso!")
