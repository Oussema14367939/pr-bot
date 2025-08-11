from flask import Blueprint, request, jsonify
from .models import PullRequest
from .extensions import db
from datetime import datetime

bp = Blueprint('main', __name__)

# ✅ Route pour récupérer toutes les PRs
@bp.route("/api/prs", methods=["GET"])
def get_all_prs():
    try:
        pr_list = PullRequest.query.order_by(PullRequest.id.desc()).all()
        pr_data = [
            {
                "id": pr.id,
                "repo": pr.repo,
                "titre": pr.titre,
                "auteur": pr.auteur,
                "date": pr.date if pr.date else "",
                "score": pr.score,
                "statut": pr.statut,
                "commentaire": pr.commentaire
            }
            for pr in pr_list
        ]
        return jsonify(pr_data), 200
    except Exception as e:
        print(f"[ERREUR GET] {e}")
        return jsonify({"error": str(e)}), 500


# ✅ Route pour insérer une nouvelle PR
@bp.route("/api/prs", methods=["POST"])
def insert_pr():
    data = request.json
    try:
        pr = PullRequest(
            repo=data.get("repo"),
            titre=data.get("titre"),
            auteur=data.get("auteur"),
            date=datetime.strptime(data.get("date"), "%Y-%m-%d %H:%M:%S") if data.get("date") else datetime.utcnow(),
            score=data.get("score"),
            statut=data.get("statut"),
            commentaire=data.get("commentaire")
        )
        db.session.add(pr)
        db.session.commit()
        print(f"[INSERT] PR insérée avec succès : {pr}")
        return jsonify({"message": "✅ Insertion réussie"}), 200
    except Exception as e:
        print(f"[ERREUR INSERT] {e}")
        return jsonify({"error": str(e)}), 500
