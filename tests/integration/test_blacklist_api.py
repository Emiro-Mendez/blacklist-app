import json
import os
os.environ['BEARER_TOKEN'] = 'test-token'

def test_post_blacklist_success(client):
    response = client.post('/blacklists/', 
        headers={'Authorization': 'Bearer test-token'},
        json={"email": "test@example.com", "app_uuid": "123e4567-e89b-12d3-a456-426614174000"}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Email added to blacklist'

import json
import os
os.environ['BEARER_TOKEN'] = 'dev-token-12345'

def test_post_blacklist_success(client):
    response = client.post('/blacklists/',
        headers={'Authorization': 'Bearer dev-token-12345'},
        json={"email": "test@example.com", "app_uuid": "123e4567-e89b-12d3-a456-426614174000"}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Email added to blacklist'
    assert data['data']['email'] == 'test@example.com'

def test_get_blacklist_exists(client):
    # Primero agregar
    client.post('/blacklists/',
        headers={'Authorization': 'Bearer dev-token-12345'},
        json={"email": "test2@example.com", "app_uuid": "123e4567-e89b-12d3-a456-426614174000"}
    )
    response = client.get('/blacklists/test2@example.com',
        headers={'Authorization': 'Bearer dev-token-12345'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['is_blacklisted'] == True

def test_get_blacklist_not_exists(client):
    response = client.get('/blacklists/notexists@example.com',
        headers={'Authorization': 'Bearer dev-token-12345'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['is_blacklisted'] == False

def test_post_conflict(client):
    # Agregar email primero
    client.post('/blacklists/',
        headers={'Authorization': 'Bearer dev-token-12345'},
        json={"email": "duplicate@example.com", "app_uuid": "123e4567-e89b-12d3-a456-426614174000"})
    # Intentar agregar de nuevo
    response = client.post('/blacklists/',
        headers={'Authorization': 'Bearer dev-token-12345'},
        json={"email": "duplicate@example.com", "app_uuid": "123e4567-e89b-12d3-a456-426614174000"})
    assert response.status_code == 409
    assert 'already in blacklist' in response.json['message']

def test_post_invalid_email(client):
    response = client.post('/blacklists/',
        headers={'Authorization': 'Bearer dev-token-12345'},
        json={"email": "invalid", "app_uuid": "123e4567-e89b-12d3-a456-426614174000"})
    assert response.status_code == 400
    assert 'Invalid email format' in response.json['message']

def test_post_missing_fields(client):
    response = client.post('/blacklists/',
        headers={'Authorization': 'Bearer dev-token-12345'},
        json={"email": "a@b.com"})  # Falta app_uuid
    assert response.status_code == 400
    assert 'email and app_uuid are required' in response.json['message']

def test_post_invalid_app_uuid(client):
    response = client.post('/blacklists/',
        headers={'Authorization': 'Bearer dev-token-12345'},
        json={"email": "test@example.com", "app_uuid": "not-a-uuid"})
    assert response.status_code == 400
    assert 'Invalid app_uuid format' in response.json['message']

def test_post_reason_too_long(client):
    long_reason = "a" * 260
    response = client.post('/blacklists/',
        headers={'Authorization': 'Bearer dev-token-12345'},
        json={"email": "test@example.com", "app_uuid": "123e4567-e89b-12d3-a456-426614174000", "reason": long_reason})
    assert response.status_code == 400
    assert 'reason must be at most 255 characters' in response.json['message']

def test_get_invalid_email(client):
    response = client.get('/blacklists/invalid-email',
        headers={'Authorization': 'Bearer dev-token-12345'})
    assert response.status_code == 400
    assert 'Invalid email format' in response.json['message']