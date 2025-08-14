# test.py

import requests
from datetime import datetime

# URL de ton API Flask en local ou sur serveur
API_URL = "http://127.0.0.1:5000/api/prs"

# Exemple de donnée à insérer
data = {
    "repo": "mon-repo",
    "titre": "Test PR via test.py",
    "auteur": "Oussema Cherni",
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "score": 10,
    "statut": "à réviser",
    "commentaire": "Test d'insertion depuis test.py",
    "pr_url": "https://github.com/Oussema14367939/pr-bot/pull/1"
}

try:
    response = requests.post(API_URL, json=data)
    if response.status_code == 200:
        print("✅ Insertion réussie :", response.json())
    else:
        print("❌ Erreur :", response.status_code, response.json())
except Exception as e:
    print("❌ Exception :", e)
