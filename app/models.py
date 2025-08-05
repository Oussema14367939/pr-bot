# app/models.py

from . import db

class PullRequest(db.Model):
    __tablename__ = 'pr_analysees'

    id = db.Column(db.Integer, primary_key=True)
    repo = db.Column(db.String(255), nullable=False)
    titre = db.Column(db.String(255), nullable=False)
    auteur = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    statut = db.Column(db.String(100), nullable=False)
    commentaire = db.Column(db.Text, nullable=False)
