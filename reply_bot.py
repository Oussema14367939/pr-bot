import os
import sys
import time
import jwt
import requests
import json

def get_env_var(name):
    value = os.getenv(name)
    if value is None:
        print(f"❌ Variable d'environnement manquante : {name}")
        sys.exit(1)
    return value

# 📦 Variables d’environnement
app_id = get_env_var("APP_ID")
installation_id = get_env_var("INSTALLATION_ID")
private_key_path = get_env_var("PRIVATE_KEY_PATH")
repo = get_env_var("REPO")
issue_number = get_env_var("ISSUE_NUMBER")
comment_body = get_env_var("COMMENT_BODY")
comment_author = get_env_var("COMMENT_AUTHOR")
bot_username = get_env_var("BOT_USERNAME")
api_key = get_env_var("DEEPSEEK_API_KEY")

# 🛑 Ignorer les commentaires du bot lui-même
if comment_author == bot_username:
    print(f"⛔ Ignoré : commentaire fait par le bot lui-même ({bot_username})")
    sys.exit(0)

# 🧠 Construction du prompt
prompt = f"""Tu es un reviewer intelligent dans une Pull Request GitHub.
Voici un commentaire d’un développeur (@{comment_author}) :

\"\"\"{comment_body}\"\"\"

Réponds de manière claire, utile, technique et concise.
"""

# 🔥 Appel à Gemini (comme dans le bon script)
model = "models/gemini-2.0-flash"
endpoint = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={api_key}"

headers = {
    "Content-Type": "application/json"
}

data = {
    "contents": [
        {
            "parts": [
                { "text": prompt }
            ]
        }
    ]
}

try:
    response = requests.post(endpoint, headers=headers, json=data)
    print("🔎 Réponse brute Gemini:", json.dumps(response.json(), indent=2))

    if response.status_code != 200:
        generated_reply = f"⚠️ Erreur Gemini ({response.status_code})"
    else:
        content = response.json()["candidates"][0]["content"]
        if isinstance(content, dict) and "parts" in content:
            generated_reply = "".join([part["text"] for part in content["parts"] if "text" in part])
        else:
            generated_reply = str(content)  # fallback

    if not generated_reply.strip():
        generated_reply = f"⚠️ Désolé @{comment_author}, je n'ai pas pu générer de réponse utile."

except Exception as e:
    print(f"❌ Exception Gemini : {e}")
    generated_reply = f"⚠️ Une erreur est survenue, @{comment_author}"

# 🔧 Construction du commentaire à poster
reply = f"""🔥 Merci @{comment_author} pour ton commentaire :
> {comment_body}

🤖 Réponse :
{generated_reply}
"""

# 🔐 Authentification GitHub
with open(private_key_path, "r") as f:
    private_key = f.read()

now = int(time.time())
payload = {
    "iat": now,
    "exp": now + 600,
    "iss": app_id
}

jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

access_token_url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
headers_jwt = {
    "Authorization": f"Bearer {jwt_token}",
    "Accept": "application/vnd.github+json"
}

response = requests.post(access_token_url, headers=headers_jwt)
if response.status_code != 201:
    print(f"❌ Erreur lors de la récupération du token GitHub : {response.status_code}")
    sys.exit(1)

token = response.json()["token"]

# 💬 Poster la réponse sur la PR
comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
headers_post = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}
payload = { "body": reply }

print("💬 Envoi de la réponse :", reply)
post = requests.post(comment_url, headers=headers_post, json=payload)

if post.status_code == 201:
    print("✅ Commentaire posté avec succès")
else:
    print(f"❌ Erreur lors de l'envoi du commentaire : {post.status_code}")
    print(post.text)
