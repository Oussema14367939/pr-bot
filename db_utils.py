import sqlite3
from datetime import datetime

DB_PATH = "prh.db"

def insert_pr(repo, titre, auteur, date, score, statut, commentaire):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO pr_analysees (repo, titre, auteur, date, score, statut, commentaire)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        repo,
        titre,
        auteur,
        date if date else datetime.utcnow().isoformat(),
        score,
        statut,
        commentaire
    ))
    conn.commit()
    conn.close()
