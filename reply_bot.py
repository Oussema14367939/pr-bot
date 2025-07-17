import os
import requests
import sys

# ✅ Fonction utilitaire pour récupérer une variable obligatoire
def get_env_var(name):
    value = os.getenv(name)
    if value is None:
        print(f"❌ Erreur : la variable d'environnement '{name}' est introuvable.")
        sys.exit(1)
    return value

# 🔐 Récupération sécurisée des variables d'environnement
token = get_env_var("GITHUB_TOKEN")
repo = get_env_var("REPO")
issue_number = get_env_var("ISSUE_NUMBER")
comment_body = get_env_var("COMMENT_BODY")
comment_author = get_env_var("COMMENT_AUTHOR")
bot_username = os.getenv("GITHUB_ACTOR") or "unknown"

# 🪵 Debug log
print(f"[DEBUG] Comment author: {comment_author}, bot username: {bot_username}")
print(f"[DEBUG] Repo: {repo}, Issue #: {issue_number}")
print(f"[DEBUG] Comment body: {comment_body}")

# 🛑 Ignore les commentaires venant d'autres que oussema
if comment_author != "oussema":
    print(f"ℹ️ Ignoré : le commentaire vient de {comment_author}, pas de oussema.")
    sys.exit(0)

# 🧠 Préparer la réponse
reply = f"🔥 Merci @{comment_author} pour ton commentaire :\n> {comment_body}"

# 📤 Envoie la réponse
url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}
payload = {"body": reply}

print("💬 Envoi de la réponse :", reply)
response = requests.post(url, headers=headers, json=payload)

if response.status_code == 201:
    print("✅ Réponse postée avec succès")
else:
    print(f"❌ Erreur {response.status_code} : {response.text}")
