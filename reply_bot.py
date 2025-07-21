import os
import sys
import time
import jwt  # PyJWT
import requests

# 🔧 Récupération sécurisée des variables
def get_env_var(name):
    value = os.getenv(name)
    if value is None:
        print(f"❌ Erreur : la variable d'environnement '{name}' est introuvable.")
        sys.exit(1)
    return value

# 🔐 Variables GitHub App
app_id = get_env_var("APP_ID")
installation_id = get_env_var("INSTALLATION_ID")
private_key_path = get_env_var("PRIVATE_KEY_PATH")

# 📄 Variables de l'événement GitHub
repo = get_env_var("REPO")
issue_number = get_env_var("ISSUE_NUMBER")
comment_body = get_env_var("COMMENT_BODY")
comment_author = get_env_var("COMMENT_AUTHOR")
bot_username = get_env_var("BOT_USERNAME")

# 🤖 Ignorer les commentaires du bot lui-même
if comment_author == bot_username:
    print(f"⛔ Ignoré : commentaire fait par le bot lui-même ({bot_username})")
    sys.exit(0)

# 🔐 Étape 1 : Générer le JWT
with open(private_key_path, "r") as f:
    private_key = f.read()

now = int(time.time())
payload = {
    "iat": now,
    "exp": now + (10 * 60),
    "iss": app_id
}

jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

# 🪪 Étape 2 : Obtenir le token d'installation
access_token_url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
headers_jwt = {
    "Authorization": f"Bearer {jwt_token}",
    "Accept": "application/vnd.github+json"
}

response = requests.post(access_token_url, headers=headers_jwt)
if response.status_code != 201:
    print(f"❌ Impossible d'obtenir le token d'installation : {response.status_code}")
    print(response.text)
    sys.exit(1)

token = response.json()["token"]

# ✍️ Étape 3 : Poster le commentaire
reply = f"🔥 Merci @{comment_author} pour ton commentaire :\n> {comment_body}"
comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}
payload = {"body": reply}

print("💬 Envoi de la réponse :", reply)
resp = requests.post(comment_url, headers=headers, json=payload)

if resp.status_code == 201:
    print("✅ Réponse postée avec succès")
else:
    print(f"❌ Erreur {resp.status_code} : {resp.text}")

print(f"Repo: {repo}")
print(f"Issue number: {issue_number}")
print(f"Comment body: {comment_body}")
print(f"Comment author: {comment_author}")
print(f"Bot username: {bot_username}")
