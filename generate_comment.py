import requests
import os

def generate_comment(fichiers, auteur, date):
    if not fichiers:
        return f"📝 Aucun fichier modifié détecté.\n\n👤 Auteur : **{auteur}**\n📅 Créé le : **{date}**"

    commentaire = "🧠 **Revue intelligente des fichiers modifiés**\n\n"

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

        prompt = f"""
Tu es un assistant intelligent pour la revue de code. Voici le contenu du fichier `{fichier}` soumis dans une Pull Request :

{contenu}

Analyse ce fichier et génère un retour structuré avec les sections suivantes (utilise le format Markdown avec des emojis) :

📌 Résumé : une ou deux phrases sur l’état global du fichier  
🐞 Problèmes détectés : liste des problèmes potentiels ou points à améliorer  
💡 Suggestions : améliorations possibles  
✅ Code correct : parties positives à conserver  
🧽 Nettoyage : indentation, lignes vides, commentaires, etc.

Commence ta réponse directement sans phrases inutiles. Donne un contenu lisible et bien structuré.
"""

        data = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        response = requests.post(endpoint, headers=headers, json=data)

        if response.status_code != 200:
            commentaire += f"\n❌ Erreur Gemini pour `{fichier}` : {response.status_code} - {response.text}\n"
            continue

        try:
            content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            commentaire += f"\n⚠️ Erreur de parsing de réponse Gemini pour `{fichier}` : {e}\n"
            continue

        commentaire += f"---\n\n🗂️ **Fichier : `{fichier}`**\n\n{content.strip()}\n\n"

    commentaire += f"---\n\n👤 Auteur : **{auteur}**\n📅 Créé le : **{date}**"
    return commentaire
