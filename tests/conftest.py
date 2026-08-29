import os
import pytest
from src.main import app
from src.db.database import db

@pytest.fixture
def client():
    os.environ['BEARER_TOKEN'] = 'dev-token-12345'
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()