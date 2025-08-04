import requests
import os

def generate_comment(fichiers, auteur, date):
    if not fichiers:
        return f"📝 Aucun fichier modifié détecté.\n\n👤 Auteur : **{auteur}**\n📅 Créé le : **{date}**"

    commentaire = f"🧠 **Revue intelligente des fichiers modifiés :**\n"

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "❌ Clé API Gemini manquante."

    model = "models/gemini-2.0-flash"
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

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

        data = {
            "prompt": {
                "text": prompt
            },
            "temperature": 0.2,
            "maxOutputTokens": 512
        }

        try:
            response = requests.post(endpoint, headers=headers, json=data)
        except Exception as e:
            commentaire += f"\n❌ Erreur réseau lors de la requête Gemini pour `{fichier}` : {e}\n"
            continue

        if response.status_code != 200:
            commentaire += f"\n❌ Erreur Gemini pour `{fichier}` : {response.status_code} - {response.text}\n"
            continue

        try:
            result_json = response.json()
            content = result_json.get("candidates", [{}])[0].get("content", "")
            if not content:
                raise ValueError("Réponse vide")
        except Exception as e:
            commentaire += f"\n⚠️ Erreur de parsing de réponse Gemini pour `{fichier}` : {e}\n"
            continue

        commentaire += (
            f"\n<details>\n"
            f"<summary>🗂️ Revue détaillée du fichier `{fichier}`</summary>\n\n"
            f"{content}\n"
            f"</details>\n"
        )

    commentaire += f"\n---\n👤 Auteur : **{auteur}**\n📅 Créé le : **{date}**"
    return commentaire
