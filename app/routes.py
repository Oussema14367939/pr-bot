from flask import render_template, Blueprint
import sqlite3

bp = Blueprint('main', __name__)

@bp.route("/")
def index():
    conn = sqlite3.connect("prh.db")
    c = conn.cursor()
    c.execute("SELECT id, titre, auteur, date, score, statut, commentaire FROM pr_analysees ORDER BY id DESC")
    pr_list = c.fetchall()
    conn.close()
    return render_template("index.html", pr_list=pr_list)
