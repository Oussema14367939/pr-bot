# reply_bot.py

import os
import requests

token = os.getenv("GITHUB_TOKEN")
repo = os.getenv("REPO")
issue_number = os.getenv("ISSUE_NUMBER")
comment_body = os.getenv("COMMENT_BODY")
comment_author = os.getenv("COMMENT_AUTHOR")

# Vérifie si le commentaire vient du bot lui-même
# Remplace ce nom par celui de ton bot GitHub s'il est différent
BOT_USERNAME = "github-actions[bot]"

if comment_author == BOT_USERNAME:
    print("🤖 Le commentaire vient du bot. Pas de réponse nécessaire.")
    exit(0)

# Génère la réponse
reply = f"🔥 Merci @{comment_author} pour ton commentaire :\n> {comment_body}"

# Envoie la réponse
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
    print("❌ Échec :", response.status_code)
    print(response.text)
