import os
import requests
import sys

def get_env_var(name):
    value = os.getenv(name)
    if value is None:
        print(f"❌ Erreur : la variable d'environnement '{name}' est introuvable.")
        sys.exit(1)
    return value

# 🔐 Récupération des variables
token = get_env_var("GITHUB_TOKEN")
repo = get_env_var("REPO")
issue_number = get_env_var("ISSUE_NUMBER")
comment_body = get_env_var("COMMENT_BODY")
comment_author = get_env_var("COMMENT_AUTHOR")


bot_username = get_env_var("BOT_USERNAME")

if comment_author == bot_username:
    print(f"⛔ Ignoré : commentaire fait par le bot lui-même ({bot_username})")
    sys.exit(0)


# 🧠 Préparer la réponse
reply = f"🔥 Merci @{comment_author} pour ton commentaire :\n> {comment_body}"

# 📤 Envoi de la réponse
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
