# bot.py

import argparse
import sys
import os
import requests
from datetime import datetime

# Ajouter le chemin du répertoire contenant ce fichier dans sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 📦 Importation des modules de ton app Flask
from app import create_app
from app.extensions import db
from app.models import PullRequest

from get_modified_files import get_modified_files
from generate_comment import generate_comment
from post_comment import post_comment

from auth import generate_jwt, get_installation_token, APP_ID, INSTALLATION_ID, PRIVATE_KEY_PATH

# 🔧 Lire les arguments depuis GitHub Actions
parser = argparse.ArgumentParser()
parser.add_argument("--pr_number", required=True, type=int, help="Pull request number")
parser.add_argument("--repo", required=True, help="Repository name (e.g. user/repo)")
args = parser.parse_args()

# Extraire infos
pr_number = args.pr_number
repo = args.repo

# 🔐 Authentification avec GitHub App
jwt_token = generate_jwt(APP_ID, PRIVATE_KEY_PATH)
token = get_installation_token(jwt_token, INSTALLATION_ID)

# 📁 Récupération des fichiers modifiés depuis GitHub
print("📁 Récupération des fichiers modifiés depuis GitHub...")
modified_files = get_modified_files(token, repo, pr_number)
print("✅ Fichiers modifiés :", modified_files)

# 🧾 Récupérer infos sur l’auteur, la date, et le titre de la PR
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}
pr_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
response = requests.get(pr_url, headers=headers)
if response.status_code != 200:
    raise Exception("❌ Erreur lors de la récupération des détails de la PR")

pr_data = response.json()
author = pr_data["user"]["login"]
created_at = pr_data["created_at"]
titre_pr = pr_data["title"]
created_at_formatted = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M UTC")

# 🧠 Générer un commentaire automatique
comment, score, statut = generate_comment(modified_files, author, created_at_formatted, titre_pr)
print("📝 Commentaire généré :\n", comment)

# 🗃️ Créer l'app Flask et insérer en base PostgreSQL
app = create_app()

print("⏳ Insertion de la PR en base PostgreSQL...")
try:
    with app.app_context():
        pr = PullRequest(
            repo=repo,
            titre=titre_pr,
            auteur=author,
            date=created_at_formatted,
            score=score,
            statut=statut,
            commentaire=comment
        )
        db.session.add(pr)
        db.session.commit()
    print("✅ Insertion en base réussie")
except Exception as e:
    print(f"❌ Erreur lors de l'insertion en base : {e}")

# 🚀 Poster le commentaire sur la PR
print("🚀 Envoi du commentaire sur la Pull Request...")
post_comment(token, repo, pr_number, comment)
