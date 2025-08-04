# db_utils.py
import requests
import os

# Exemple : remplace cette URL par celle de ton ngrok ou localhost
FLASK_API_URL = os.environ.get("FLASK_API_URL", "http://localhost:5000")

def insert_pr(repo, titre, auteur, date, score, statut, commentaire):
    payload = {
        "repo": repo,
        "titre": titre,
        "auteur": auteur,
        "date": date,
        "score": score,
        "statut": statut,
        "commentaire": commentaire
    }
    url = f"{FLASK_API_URL}/insert_pr"
    print(f"🌐 Appel HTTP POST vers {url}...")
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Insertion distante réussie")
    else:
        raise Exception(f"❌ Insertion échouée : {response.status_code} {response.text}")
