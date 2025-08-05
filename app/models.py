# app/models.py
from .extensions import db

class PullRequest(db.Model):
    __tablename__ = 'pr_analysees'

    id = db.Column(db.Integer, primary_key=True)
    repo = db.Column(db.String(255))
    titre = db.Column(db.String(255))
    auteur = db.Column(db.String(255))
    date = db.Column(db.String(255))
    score = db.Column(db.Integer)
    statut = db.Column(db.String(50))
    commentaire = db.Column(db.Text)
