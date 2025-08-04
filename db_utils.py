import sqlite3
from datetime import datetime
from datetime import datetime, timezone
DB_PATH = "prh.db"

def insert_pr(repo, titre, auteur, date, score, statut, commentaire):
    print(f"🔍 Connexion à la base : {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO pr_analysees (repo, titre, auteur, date, score, statut, commentaire)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        repo,
        titre,
        auteur,
        date if date else datetime.now(timezone.utc).isoformat(),
        score,
        statut,
        commentaire
    ))
    conn.commit()
    conn.close()
