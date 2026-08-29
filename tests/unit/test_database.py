import os
import pytest
from flask import Flask
from src.db.database import init_db, create_tables

def test_init_db_without_env():
    # Eliminar DATABASE_URL para que use el valor por defecto
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']
    
    app = Flask(__name__)  # App nueva, no la global
    db = init_db(app)
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///blacklist.db'
    assert db is not None

def test_init_db_with_env():
    os.environ['DATABASE_URL'] = 'sqlite:///test.db'
    app = Flask(__name__)
    db = init_db(app)
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///test.db'
    assert db is not None
    # Limpiar
    del os.environ['DATABASE_URL']

def test_create_tables():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_db(app)
    with app.app_context():
        create_tables(app)  # debería ejecutar sin errores