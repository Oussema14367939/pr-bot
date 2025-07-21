import os
import requests
import jwt
import time
from flask import Flask, request, jsonify

# CONFIGURATION
APP_ID = os.environ.get("APP_ID")
INSTALLATION_ID = os.environ.get("INSTALLATION_ID")
REPO = os.environ.get("REPO")

# Charger la clé privée depuis un fichier local ou depuis les variables d'environnement
def load_private_key():
    if 'PRIVATE_KEY' in os.environ:
        return os.environ['PRIVATE_KEY']
    else:
        with open("private-key.pem", "r") as key_file:
            return key_file.read()

PRIVATE_KEY = load_private_key()

# GÉNÉRER UN JWT
def generate_jwt():
    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + (10 * 60),
        "iss": APP_ID
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

# RÉCUPÉRER LE TOKEN D’ACCÈS
def get_installation_token(jwt_token):
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }
    url = f"https://api.github.com/app/installations/{INSTALLATION_ID}/access_tokens"
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()["token"]

# COMMENTER UNE PR
def comment_on_pr(token, pr_number, repo, message):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    data = {"body": message}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

# FLASK APP POUR WEBHOOK
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    event = request.headers.get("X-GitHub-Event")
    payload = request.get_json()

    if event == "pull_request" and payload["action"] in ["opened", "reopened"]:
        pr_number = payload["pull_request"]["number"]
        repo_full_name = payload["repository"]["full_name"]

        jwt_token = generate_jwt()
        access_token = get_installation_token(jwt_token)

        message = "✅ Merci pour votre Pull Request ! Elle sera examinée bientôt."
        comment_on_pr(access_token, pr_number, repo_full_name, message)

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000)
