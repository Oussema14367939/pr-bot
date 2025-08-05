# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # ✅ Connection à Supabase PostgreSQL
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:TON_MDP@db.dntvridtsvpckqpstzvm.supabase.co:5432/postgres"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(bp)

    with app.app_context():
        from .models import PullRequest
        db.create_all()

    return app
