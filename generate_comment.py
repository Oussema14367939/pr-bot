# generate_comment.py

def generate_comment(fichiers, auteur, date):
    if not fichiers:
        return f"📝 Aucun fichier modifié détecté.\n\n👤 Auteur : **{auteur}**\n📅 Créé le : **{date}**"

    commentaire = f"📝 Fichiers modifiés dans cette PR :\n"
    for f in fichiers:
        commentaire += f"- `{f}`\n"

    commentaire += f"\n---\n👤 Auteur : **{auteur}**\n📅 Créé le : **{date}**"
    return commentaire
