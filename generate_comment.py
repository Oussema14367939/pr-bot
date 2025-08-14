import requests
import os
import random

def generate_comment(fichiers, auteur, date, titre_pr):
    if not fichiers:
        return (
            f"📝 Aucun fichier modifié détecté.\n\n"
            f"📌 Titre de la PR : **{titre_pr}**\n"
            f"👤 Auteur : **{auteur}**\n"
            f"📅 Créé le : **{date}**"
        )

    # Simuler un score IA (pour l'instant aléatoire)
    score = random.randint(60, 100)
    statut = "Approuvée" if score >= 80 else "À réviser"


    commentaire = f"""\
🧠 **Revue intelligente de la Pull Request**

📌 **Titre de la PR** : `{titre_pr}`
👤 **Auteur** : {auteur}
📅 **Date de création** : {date}

📊 **Score IA** : {score}/100
📈 **Statut proposé** : {statut}

🔍 **Fichiers analysés** : {len(fichiers)} fichier(s) modifié(s)
"""

    api_key = os.getenv("DEEPSEEK_API_KEY") 
    if not api_key:
        return "❌ Clé API Gemini manquante."

    model = "models/gemini-2.0-flash"
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={api_key}"
    headers = { "Content-Type": "application/json" }

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
            raw_content = response.json()["candidates"][0]["content"]
            content = "".join(part.get("text", "") for part in raw_content.get("parts", []))
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
    return commentaire, score, statut
