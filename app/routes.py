# routes.py
from flask import render_template, Blueprint, request, jsonify
import sqlite3
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route("/")
def index():
    conn = sqlite3.connect("prh.db")
    c = conn.cursor()
    c.execute("SELECT id, titre, auteur, date, score, statut, commentaire FROM pr_analysees ORDER BY id DESC")
    pr_list = c.fetchall()
    conn.close()
    return render_template("index.html", pr_list=pr_list)

@bp.route("/insert_pr", methods=["POST"])
def insert_pr():
    data = request.json
    try:
        conn = sqlite3.connect("prh.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO pr_analysees (repo, titre, auteur, date, score, statut, commentaire)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("repo"),
            data.get("titre"),
            data.get("auteur"),
            data.get("date") or datetime.utcnow().isoformat(),
            data.get("score"),
            data.get("statut"),
            data.get("commentaire")
        ))
        conn.commit()
        conn.close()
        return jsonify({"message": "✅ Insertion réussie"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
