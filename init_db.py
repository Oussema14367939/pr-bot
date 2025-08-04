import sqlite3

DB_PATH = "prh.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pr_analysees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repo TEXT,
            titre TEXT,
            auteur TEXT,
            date TEXT,
            score INTEGER,
            statut TEXT,
            commentaire TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Table 'pr_analysees' créée avec succès.")

if __name__ == "__main__":
    init_db()
