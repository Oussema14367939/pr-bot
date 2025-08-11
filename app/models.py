# app/models.py
from .extensions import db

class PullRequest(db.Model):
    __tablename__ = 'pr_analysees'

    id = db.Column(db.Integer, primary_key=True)
    repo = db.Column(db.String(255))
    titre = db.Column(db.String(255))
    auteur = db.Column(db.String(255))
    date = db.Column(db.String(255))  # c'est une chaîne, donc on ne fait pas strftime
    score = db.Column(db.Integer)
    statut = db.Column(db.String(50))
    commentaire = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "repo": self.repo,
            "titre": self.titre,
            "auteur": self.auteur,
            "date": self.date,  # déjà une chaîne
            "score": self.score,
            "statut": self.statut,
            "commentaire": self.commentaire
        }
