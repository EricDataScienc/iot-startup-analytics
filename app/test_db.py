import sqlite3

conn = sqlite3.connect("data/app.db")
cursor = conn.cursor()

for row in cursor.execute("SELECT * FROM tech_score LIMIT 5"):
    print(row)

conn.close()
