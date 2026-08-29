def test_missing_token(client):
    response = client.post('/blacklists/', json={"email": "a@b.com", "app_uuid": "123"})
    assert response.status_code == 401
    assert 'Missing Authorization header' in response.json['message']

def test_invalid_token_format(client):
    response = client.post('/blacklists/',
        headers={'Authorization': 'Basic 123'},  # Formato incorrecto
        json={"email": "a@b.com", "app_uuid": "123"})
    assert response.status_code == 401
    assert 'Invalid Authorization header format' in response.json['message']

def test_invalid_token(client):
    response = client.post('/blacklists/',
        headers={'Authorization': 'Bearer wrong-token'},
        json={"email": "a@b.com", "app_uuid": "123"})
    assert response.status_code == 401
    assert 'Invalid token' in response.json['message']