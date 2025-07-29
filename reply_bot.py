import requests
import os

def generate_reply(commentaire_utilisateur: str, username: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY")  # Assure-toi que la variable est bien définie dans ton environnement

    if not api_key:
        return "❌ Clé API Gemini manquante."

    model = "models/gemini-2.0-flash"
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    prompt = f"""
Tu es un bot intelligent qui aide les développeurs à revoir les Pull Requests sur GitHub.

Un utilisateur (@{username}) a laissé ce commentaire :
\"{commentaire_utilisateur}\"

Commence ta réponse par : 🔥 Merci @{username} pour ton commentaire :

Puis donne une réponse utile et intelligente à ce commentaire.
"""

    print("🧠 Prompt envoyé à Gemini :\n", prompt)

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(endpoint, headers=headers, json=data)
    except Exception as e:
        return f"❌ Erreur de connexion à l'API Gemini : {e}"

    if response.status_code != 200:
        return f"⚠️ Erreur Gemini : {response.status_code} - {response.text}"

    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"⚠️ Désolé @{username}, je n'ai pas pu générer de réponse utile (erreur de parsing)."

# Exemple de test (à commenter dans l'intégration réelle)
if __name__ == "__main__":
    print(generate_reply("Peux-tu expliquer ce que fait ce code ?", "Oussema14367939"))
