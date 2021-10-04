from tests import client_with_data


def test_get_codes(client_with_data):
    response = client_with_data.post('/auth/login', json={
        'email': 'test@mail.com',
        'password': 'test_password'
    })
    assert response.status_code == 200
    access_token = response.get_json()['access_token']
    response = client_with_data.get('/api/v1/codes', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    body = response.get_json()
    assert len(body['codes']) == 3


def test_get_code(client_with_data):
    response = client_with_data.post('/auth/login', json={
        'email': 'test@mail.com',
        'password': 'test_password'
    })
    assert response.status_code == 200
    access_token = response.get_json()['access_token']
    
    response = client_with_data.get('/api/v1/codes/1', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    body = response.get_json()
    assert body['id'] == 1
    
    response = client_with_data.get('/api/v1/codes/12', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 404


def test_create_code(client_with_data):
    response = client_with_data.post('/auth/login', json={
        'email': 'test@mail.com',
        'password': 'test_password'
    })
    assert response.status_code == 200
    access_token = response.get_json()['access_token']
    
    response = client_with_data.post(
        '/api/v1/codes',
        json={
            'code_value': 'Some_value',
            'name': 'Why not',
            'embedded_value': 'this will do',
            'user_id': 1,
        },
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == 201


def test_update_code(client_with_data):
    response = client_with_data.post('/auth/login', json={
        'email': 'test@mail.com',
        'password': 'test_password'
    })
    assert response.status_code == 200
    access_token = response.get_json()['access_token']
    
    response = client_with_data.put(
        '/api/v1/codes/1',
        json={
            'code_value': 'This will change nothing.',
            'name': 'New Name',
            'embedded_value': 'YEP',
            'user_id': 1,  # This will be ignored
        },
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == 204


def test_delete_code(client_with_data):
    response = client_with_data.post('/auth/login', json={
        'email': 'test@mail.com',
        'password': 'test_password'
    })
    assert response.status_code == 200
    access_token = response.get_json()['access_token']
    
    response = client_with_data.delete(
        '/api/v1/codes/3',
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == 204
    response = client_with_data.get(
        '/api/v1/codes',
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert len(response.get_json()['codes']) == 2
