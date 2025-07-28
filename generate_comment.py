# generate_comment.py

import requests
import os

def generate_comment(fichiers, auteur, date):
    if not fichiers:
        return f"📝 Aucun fichier modifié détecté.\n\n👤 Auteur : **{auteur}**\n📅 Créé le : **{date}**"

    commentaire = f"🧠 Revue intelligente des fichiers modifiés :\n"

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "❌ Clé API DeepSeek manquante."

    for fichier in fichiers:
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                contenu = f.read()
        except Exception as e:
            commentaire += f"\n⚠️ Impossible de lire le fichier `{fichier}` : {e}\n"
            continue

        prompt = f"""Tu es un assistant intelligent pour la revue de code.
Voici le contenu du fichier `{fichier}` soumis dans une Pull Request :

{contenu}

Donne une revue utile de ce fichier (bugs potentiels, clarté du code, améliorations possibles).
Réponds uniquement pour ce fichier.
"""

        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Tu es un expert en revue de code."},
                    {"role": "user", "content": prompt}
                ]
            }
        )

        if response.status_code != 200:
            commentaire += f"\n❌ Erreur DeepSeek pour `{fichier}` : {response.status_code}\n"
            continue

        data = response.json()
        content = data["choices"][0]["message"]["content"]
        commentaire += f"\n🗂️ **{fichier}**\n{content}\n"

    commentaire += f"\n---\n👤 Auteur : **{auteur}**\n📅 Créé le : **{date}**"
    return commentaire

