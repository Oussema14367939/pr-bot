import os
import requests

# ✅ Récupération des variables d'environnement
token = os.getenv("GITHUB_TOKEN")
repo = os.getenv("REPO")
issue_number = os.getenv("ISSUE_NUMBER")
comment_body = os.getenv("COMMENT_BODY")
comment_author = os.getenv("COMMENT_AUTHOR")
bot_username = os.getenv("GITHUB_ACTOR")

# ✅ Debug
print(f"[DEBUG] Comment author: {comment_author}, bot username: {bot_username}")
print(f"[DEBUG] Repo: {repo}, Issue: {issue_number}")
print(f"[DEBUG] Comment body: {comment_body}")

# 🔒 Répond uniquement aux commentaires de 'oussema'
if comment_author != "oussema":
    print(f"ℹ️ Ignoré : le commentaire vient de {comment_author}, pas de oussema.")
    exit(0)

# 🧠 Préparer la réponse
reply = f"🔥 Merci @{comment_author} pour ton commentaire :\n> {comment_body}"

# 📤 Envoie la réponse
url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}
payload = {"body": reply}

print("💬 Réponse envoyée :", reply)
response = requests.post(url, headers=headers, json=payload)

if response.status_code == 201:
    print("✅ Réponse postée avec succès")
else:
    print("❌ Erreur :", response.status_code)
    print(response.text)
