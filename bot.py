# bot.py

import argparse
import os
import requests
from datetime import datetime

from get_modified_files import get_modified_files
from generate_comment import generate_comment
from post_comment import post_comment

# Lire les arguments depuis GitHub Actions
parser = argparse.ArgumentParser()
parser.add_argument("--pr_number", required=True, type=int, help="Pull request number")
parser.add_argument("--repo", required=True, help="Repository name (e.g. user/repo)")
args = parser.parse_args()

# Extraire infos
pr_number = args.pr_number
repo = args.repo
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GITHUB_TOKEN non défini dans les secrets")

# Étape 1 : Obtenir les fichiers modifiés
print("📁 Récupération des fichiers modifiés depuis GitHub...")
modified_files = get_modified_files(token, repo, pr_number)
print("✅ Fichiers modifiés :", modified_files)

# Étape 2 : Récupérer infos sur l’auteur et la date de la PR
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}
pr_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
response = requests.get(pr_url, headers=headers)
if response.status_code != 200:
    raise Exception("Erreur lors de la récupération des détails de la PR")

pr_data = response.json()
author = pr_data["user"]["login"]
created_at = pr_data["created_at"]
created_at_formatted = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M UTC")

# Étape 3 : Générer un commentaire
comment = generate_comment(modified_files, author, created_at_formatted)
print("📝 Commentaire généré :\n", comment)

# Étape 4 : Poster le commentaire sur la PR
print("🚀 Envoi du commentaire sur la Pull Request...")
post_comment(token, repo, pr_number, comment)
