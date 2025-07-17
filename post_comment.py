# post_comment.py

import requests

def post_comment(token, repo, pr_number, comment):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    payload = {
        "body": comment
    }

    print(f"💬 Envoi du commentaire à {url}")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print("✅ Commentaire posté avec succès")
    else:
        print("❌ Erreur lors du post du commentaire :", response.status_code)
        print("🪵 Réponse :", response.text)

    print("❌ Erreur :", response.status_code)
    print("Réponse brute:", response.text)

