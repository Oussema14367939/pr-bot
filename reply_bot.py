# reply_bot.py

import os
import requests

# Récupération des données d'environnement
token = os.getenv("GITHUB_TOKEN")
repo = os.getenv("REPO")
issue_number = os.getenv("ISSUE_NUMBER")
comment_body = os.getenv("COMMENT_BODY")
comment_author = os.getenv("COMMENT_AUTHOR")
bot_username = os.getenv("GITHUB_ACTOR")  # C'est l'identité du bot dans le contexte du workflow

# 🔒 Empêche le bot de répondre à lui-même
if comment_author == bot_username:
    print(f"⛔ Ignoré : le commentaire vient du bot lui-même ({bot_username}).")
    exit(0)

# 🧠 Prépare la réponse
reply = f"🔥 Merci @{comment_author} pour ton commentaire :\n> {comment_body}"

# 📤 Envoie la réponse
url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}
payload = {
    "body": reply
}

print("💬 Réponse envoyée :", reply)
response = requests.post(url, headers=headers, json=payload)

if response.status_code == 201:
    print("✅ Réponse postée avec succès")
else:
    print("❌ Erreur :", response.status_code)
    print(response.text) 