# reply_bot.py

import os
import requests

# Récupération des données d'environnement
token = os.getenv("GITHUB_TOKEN")
repo = os.getenv("REPO")
issue_number = os.getenv("ISSUE_NUMBER")
comment_body = os.getenv("COMMENT_BODY")
comment_author = os.getenv("COMMENT_AUTHOR")

# Ligne temporaire à tester (force un nom de bot différent de comment_author)
bot_username = "mon-vrai-bot"  # Remplace par le nom GitHub de ton bot (ou un autre nom unique)

# Ligne actuelle à commenter temporairement
# response_user = requests.get("https://api.github.com/user", headers={"Authorization": f"Bearer {token}"})
# bot_username = response_user.json().get("login")

print(f"[DEBUG] Comment author: {comment_author}, bot username: {bot_username}")
print(f"[DEBUG] Comment body: {comment_body}")

# Empêche le bot de répondre à lui-même
if comment_author == bot_username:
    print(f"⛔ Ignoré : le commentaire vient du bot lui-même ({bot_username}).")
    exit(0)

# Prépare la réponse
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

if response.status_code in [200, 201]:
    print("✅ Réponse postée avec succès")
else:
    print("❌ Erreur :", response.status_code)
    print(response.text)
