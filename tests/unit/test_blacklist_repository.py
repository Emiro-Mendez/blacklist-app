import pytest
from src.db.database import db
from src.repositories.blacklist_repository import BlacklistRepository
from src.models.blacklist import Blacklist

def test_create_entry(client):   # <--- añadir client
    repo = BlacklistRepository()
    entry = repo.create("test@repo.com", "123e4567-e89b-12d3-a456-426614174000", "test reason")
    assert entry.id is not None
    assert entry.email == "test@repo.com"
    assert entry.reason == "test reason"

def test_get_by_email_found(client):   # <--- añadir client
    repo = BlacklistRepository()
    entry = repo.create("findme@repo.com", "123e4567-e89b-12d3-a456-426614174000")
    found = repo.get_by_email("findme@repo.com")
    assert found is not None
    assert found.id == entry.id

def test_get_by_email_not_found(client):   # <--- añadir client
    repo = BlacklistRepository()
    found = repo.get_by_email("notfound@repo.com")
    assert found is None