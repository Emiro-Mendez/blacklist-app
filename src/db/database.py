import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def init_db(app):
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        database_url = "sqlite:///blacklist.db"
        os.environ["DATABASE_URL"] = database_url
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return db

def create_tables(app):
    with app.app_context():
        db.create_all()
        print("✅ Tablas creadas correctamente")