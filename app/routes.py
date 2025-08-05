# app/routes.py

from flask import render_template, Blueprint, request, jsonify
from datetime import datetime
from .models import PullRequest
from . import db

bp = Blueprint('main', __name__)

@bp.route("/")
def index():
    pr_list = PullRequest.query.order_by(PullRequest.id.desc()).all()
    return render_template("index.html", pr_list=pr_list)

@bp.route("/insert_pr", methods=["POST"])
def insert_pr():
    data = request.json
    try:
        pr = PullRequest(
            repo=data.get("repo"),
            titre=data.get("titre"),
            auteur=data.get("auteur"),
            date=data.get("date") or datetime.utcnow().isoformat(),
            score=data.get("score"),
            statut=data.get("statut"),
            commentaire=data.get("commentaire")
        )
        db.session.add(pr)
        db.session.commit()
        return jsonify({"message": "✅ Insertion réussie"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
