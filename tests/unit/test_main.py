import pytest
from src.main import app
from src.models.errors import NotFoundError, UnauthorizedError

def test_404_error(client):
    response = client.get('/ruta-inexistente')
    assert response.status_code == 404
    assert 'Not Found' in response.json['error']

def test_health_route(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_generic_error_handler(client, mocker):
    mocker.patch('src.services.blacklist_service.BlacklistService.add_email', side_effect=Exception("Forced error"))
    response = client.post('/blacklists/',
        headers={'Authorization': 'Bearer dev-token-12345'},
        json={"email": "a@b.com", "app_uuid": "123e4567-e89b-12d3-a456-426614174000"})
    assert response.status_code == 500
    assert 'Internal Server Error' in response.json['error']

def test_not_found_error_handler(client, mocker):
    mocker.patch('src.services.blacklist_service.BlacklistService.add_email', side_effect=NotFoundError("Not found"))
    response = client.post('/blacklists/',
        headers={'Authorization': 'Bearer dev-token-12345'},
        json={"email": "a@b.com", "app_uuid": "123e4567-e89b-12d3-a456-426614174000"})
    assert response.status_code == 404
    assert 'Not Found' in response.json['error']

def test_unauthorized_error_handler(client, mocker):
    mocker.patch('src.services.blacklist_service.BlacklistService.add_email', side_effect=UnauthorizedError("Unauthorized"))
    response = client.post('/blacklists/',
        headers={'Authorization': 'Bearer dev-token-12345'},
        json={"email": "a@b.com", "app_uuid": "123e4567-e89b-12d3-a456-426614174000"})
    assert response.status_code == 401
    assert 'Unauthorized' in response.json['error']