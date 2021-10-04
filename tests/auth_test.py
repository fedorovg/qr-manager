from time import sleep
from tests import client
from werkzeug.security import generate_password_hash
from app.models import User
from app import db


def test_registration(client):
    response = client.post('/auth/register', json={
        'email': 'test@mail.com',
        'password': 'notreallyahash'
    })
    assert response.status_code == 201
    
    response = client.post('/auth/register', json={
        'email': 'test@mail.com',
        'password': 'notreallyahash'
    })
    assert response.status_code == 401
    assert b'This email is already registered.' in response.data
    
    response = client.post('/auth/register', json={
        'email': 'new_test@mail.com',
        'password': '123'
    })
    assert response.status_code == 401
    assert b'Password is too short.' in response.data
    
    response = client.post('/auth/register', json={
        'password': '123'
    })
    assert response.status_code == 401
    assert b'To register, you need to specify email and password.' in response.data


def test_login(client):
    response = client.post('/auth/login', json={
        'email': 'test@mail.com',
    })
    assert response.status_code == 401
    assert b'To log in, you need to specify email and password.' in response.data
    
    response = client.post('/auth/login', json={
        'email': 'test@mail.com',
        'password': 'notreallyahash'
    })
    assert response.status_code == 401
    assert b'Wrong email or password.' in response.data, "Couldn't detect duplicated email."
    
    db.session.add(User(email='test@mail.com', password_hash=generate_password_hash('notreallyahash')))
    db.session.commit()
    
    response = client.post('/auth/login', json={
        'email': 'test@mail.com',
        'password': 'notreallyahash'
    })
    assert response.status_code == 200
    
    response = client.post('/auth/login', json={
        'email': 'test@mail.com',
        'password': '12345'
    })
    assert response.status_code == 401
    assert b'Wrong email or password.' in response.data, "Couldn't detect wrong password."


def test_automatic_user_loading(client):
    # Create user
    response = client.post('/auth/register', json={
        'email': 'test@mail.com',
        'password': 'notreallyahash'
    })
    assert response.status_code == 201
    # Log in
    response = client.post('/auth/login', json={
        'email': 'test@mail.com',
        'password': 'notreallyahash'
    })
    assert response.status_code == 200
    
    body = response.get_json()
    access_token = body['access_token']
    refresh_token = body['refresh_token']
    
    # Authenticate with the received token
    response = client.get('/auth/protected', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert refresh_token
    assert b'test@mail.com' in response.data


def test_refresh(client):
    # Create user
    response = client.post('/auth/register', json={
        'email': 'test@mail.com',
        'password': 'notreallyahash'
    })
    assert response.status_code == 201
    # Log in
    response = client.post('/auth/login', json={
        'email': 'test@mail.com',
        'password': 'notreallyahash'
    })
    
    # Get refresh token
    assert response.status_code == 200
    refresh_token = response.get_json()['refresh_token']
    
    # Get new access_token
    response = client.post('/auth/refresh', headers={'Authorization': f'Bearer {refresh_token}'})
    assert response.status_code == 200
    access_token = response.get_json()['access_token']

    # Try to authenticate with the new access token
    response = client.get('/auth/protected', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
