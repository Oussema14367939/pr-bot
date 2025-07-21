import jwt
import time
import requests

# Remplace par ton App ID (trouvé dans ta GitHub App settings)
APP_ID = '1640744'  # ← ton vrai ID ici

# Charge ta clé privée (.pem) générée via GitHub
with open("prhelper.2025-07-21.private-key.pem", "r") as key_file:
    private_key = key_file.read()

# Crée un JWT valable 10 minutes
payload = {
    "iat": int(time.time()) - 60,
    "exp": int(time.time()) + (10 * 60),
    "iss": APP_ID
}

jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

# Appelle l’API GitHub pour récupérer l’installation
headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Accept": "application/vnd.github+json"
}

response = requests.get("https://api.github.com/app/installations", headers=headers)

if response.status_code == 200:
    installations = response.json()
    for inst in installations:
        print(f"Installation ID: {inst['id']}")
        print(f"Account: {inst['account']['login']}")
        print(f"Repositories: {inst['target_type']}")
else:
    print("Erreur:", response.status_code)
    print(response.text)
