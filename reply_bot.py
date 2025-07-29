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

# 🔐 Clé API Gemini (DEEPSEEK_API_KEY)
gemini_api_key = get_env_var("DEEPSEEK_API_KEY")
gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# 🤖 Ignorer les commentaires du bot lui-même
if comment_author == bot_username:
    print(f"⛔ Ignoré : commentaire fait par le bot lui-même ({bot_username})")
    sys.exit(0)

# ✍️ Étape 1 : Construire le prompt
prompt = f"""
Tu es un reviewer intelligent dans une Pull Request GitHub.
Voici un commentaire de développeur (@{comment_author}) :

\"\"\"{comment_body}\"\"\"

Réponds de manière claire, utile, technique et concise.
"""

# 🧠 Étape 2 : Appeler l'API Gemini
gemini_headers = {
    "Content-Type": "application/json",
    # IMPORTANT : souvent Google attend "Authorization: Bearer <token>", pas x-goog-api-key
    "Authorization": f"Bearer {gemini_api_key}"
}

gemini_data = {
    "prompt": {
        "text": prompt
    },
    "temperature": 0.7,
    "candidateCount": 1,
    "maxOutputTokens": 512
}

try:
    response = requests.post(gemini_url, headers=gemini_headers, json=gemini_data)
    print(f"DEBUG - Status code Gemini : {response.status_code}")
    print(f"DEBUG - Response Gemini : {response.text}")

    if response.status_code != 200:
        print(f"❌ Erreur Gemini {response.status_code} : {response.text}")
        generated_reply = f"⚠️ Désolé @{comment_author}, une erreur est survenue avec le moteur d'IA."
    else:
        response_json = response.json()
        # Extraction sécurisée du texte, suivant la structure retournée par Gemini
        candidates = response_json.get("candidates")
        if candidates and len(candidates) > 0:
            candidate = candidates[0]
            content = candidate.get("content")
            if isinstance(content, dict):
                # Parfois "parts" est une liste de dicts avec "text"
                parts = content.get("parts")
                if parts and len(parts) > 0:
                    generated_reply = parts[0].get("text", "")
                else:
                    generated_reply = ""
            elif isinstance(content, str):
                generated_reply = content
            else:
                generated_reply = ""
        else:
            generated_reply = ""
        if not generated_reply:
            generated_reply = f"⚠️ Désolé @{comment_author}, je n'ai pas pu générer de réponse."
except Exception as e:
    print(f"❌ Exception lors de l'appel à Gemini : {e}")
    generated_reply = f"⚠️ Une erreur est survenue en traitant votre commentaire, @{comment_author}."

# 🔧 Construire le message final à poster
reply = f"""🔥 Merci @{comment_author} pour ton commentaire :
> {comment_body}

🤖 Réponse :
{generated_reply}
"""

# 🔐 Étape 3 : Générer le JWT GitHub
with open(private_key_path, "r") as f:
    private_key = f.read()

now = int(time.time())
payload = {
    "iat": now,
    "exp": now + (10 * 60),
    "iss": app_id
}

jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

# 🪪 Étape 4 : Obtenir le token d'installation GitHub
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

# 💬 Étape 5 : Poster le commentaire sur la PR
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
