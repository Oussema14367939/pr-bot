from db_utils import insert_pr

# Exemple de données
insert_pr(
    repo="Oussema14367939/test-bot-pr",
    titre="Ajout d'une nouvelle fonctionnalité",
    auteur="Oussema14367939",
    date="2025-08-04 15:12",
    score=82,
    statut="approuvée",
    commentaire="✅ Code propre.\n💡 Suggestion : ajouter des tests unitaires."
)
