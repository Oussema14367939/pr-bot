# get_modified_files.py

import requests

def get_modified_files(token, repo, pr_number):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    print(f"🔗 Appel à l'API GitHub : {url}")

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Erreur lors de la récupération des fichiers :", response.status_code)
        print("🪵 Réponse :", response.text)
        return []

    data = response.json()
    modified_files = [file["filename"] for file in data]
    return modified_files
