# auth.py

import jwt
import time
import requests

# 🔧 Remplace par les vraies infos de ton app
APP_ID = '1640744'  # ex: 123456
INSTALLATION_ID = '76873413'  # ex: 789012
PRIVATE_KEY_PATH = 'prhelper.2025-07-21.private-key.pem'  # le fichier téléchargé depuis GitHub

def generate_jwt(app_id, private_key_path):
    with open(private_key_path, 'r') as f:
        private_key = f.read()

    now = int(time.time())
    payload = {
        'iat': now - 60,
        'exp': now + (10 * 60),
        'iss': app_id
    }

    return jwt.encode(payload, private_key, algorithm='RS256')

def get_installation_token(jwt_token, installation_id):
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/vnd.github+json'
    }

    url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
    response = requests.post(url, headers=headers)

    if response.status_code == 201:
        return response.json()['token']
    else:
        raise Exception(f"Erreur lors de l'obtention du token : {response.status_code} - {response.text}")
