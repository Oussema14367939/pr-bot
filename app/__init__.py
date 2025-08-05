from flask import Flask
from .extensions import db
from dotenv import load_dotenv
import os

def create_app():
    # 📥 Charger les variables d'environnement depuis le fichier .env
    load_dotenv()

    app = Flask(__name__)

    # 🔧 Configuration de la base de données via une variable d'environnement
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ⚙️ Initialisation des extensions
    db.init_app(app)

    # 🛠️ Création des tables si elles n'existent pas
    with app.app_context():
        db.create_all()

    # 🔁 Importer et enregistrer le blueprint des routes
    from .routes import bp
    app.register_blueprint(bp)

    return app
