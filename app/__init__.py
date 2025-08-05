from flask import Flask
from .routes import bp
from .extensions import db  # ✅

def create_app():
    app = Flask(__name__)

    # 🔐 Ajoute ta vraie URL Supabase ici (copiée depuis la plateforme)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Oussema-cherni2002@db.dntvridtsvpckqpstzvm.supabase.co:5432/postgres"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()  # 📦 Création des tables si elles n'existent pas

    return app
