import requests
import os

def split_summary_and_detail(text):
    # Sépare la réponse Gemini en résumé et détail avec une ligne '---'
    if '---' in text:
        summary, detail = text.split('---', 1)
    else:
        summary, detail = "", text
    return summary.strip(), detail.strip()

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

Donne d'abord un résumé structuré du fichier avec les rubriques suivantes :
📌 Résumé :
🐞 Problèmes détectés :
💡 Suggestions :
✅ Code correct :
🧽 Nettoyage :

Ensuite, donne une revue détaillée complète du fichier.
Sépare bien le résumé et la revue détaillée avec une ligne contenant uniquement ---
Réponds uniquement pour ce fichier.
"""

        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        response = requests.post(endpoint, headers=headers, json=data)

        if response.status_code != 200:
            commentaire += f"\n❌ Erreur Gemini pour `{fichier}` : {response.status_code} - {response.text}\n"
            continue

        try:
            raw_content = response.json()["candidates"][0]["content"]
            content = "".join(part.get("text", "") for part in raw_content.get("parts", []))
        except Exception as e:
            commentaire += f"\n⚠️ Erreur de parsing de réponse Gemini pour `{fichier}` : {e}\n"
            continue

        summary, detail = split_summary_and_detail(content)

        commentaire += (
            f"\n🗂️ Fichier : `{fichier}`\n\n"
            f"{summary}\n\n"
            f"<details>\n"
            f"<summary>🧠 Revue détaillée du fichier `{fichier}`</summary>\n\n"
            f"{detail}\n"
            f"</details>\n"
        )

    commentaire += f"\n---\n👤 Auteur : **{auteur}**\n📅 Créé le : **{date}**"
    return commentaire
