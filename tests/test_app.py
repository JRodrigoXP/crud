from http import HTTPStatus


def test_read_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_list_users(client, monkeypatch):
    monkeypatch.setattr('fast_zero.app.database', [])
    user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    }
    client.post('/users/', json=user)

    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user': [
            {
                'id': 1,
                'username': 'testuser',
                'email': 'testuser@example.com',
            }
        ]
    }


def test_get_user(client, monkeypatch):
    monkeypatch.setattr('fast_zero.app.database', [])
    user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    }
    client.post('/users/', json=user)

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'testuser',
        'email': 'testuser@example.com',
    }


def test_get_user_not_found(client, monkeypatch):
    monkeypatch.setattr('fast_zero.app.database', [])

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_create_user(client):
    user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    }
    response = client.post('/users/', json=user)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'testuser',
        'email': 'testuser@example.com',
    }


def test_create_user_username_existing(client):
    user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    }
    client.post('/users/', json=user)

    duplicate_user = {**user, 'email': 'other@example.com'}
    response = client.post('/users/', json=duplicate_user)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already registered'}


def test_create_user_email_existing(client):
    user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    }
    client.post('/users/', json=user)

    duplicate_user = {
        **user,
        'username': 'otheruser',
    }
    response = client.post('/users/', json=duplicate_user)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already registered'}


def test_update_user(client):
    user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    }
    client.post('/users/', json=user)
    response = client.put(
        '/users/1',
        json={
            'username': 'Jorge',
            'email': 'Jorge@example.com',
            'password': 'testpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Jorge',
        'email': 'Jorge@example.com',
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'Jorge',
            'email': 'Jorge@example.com',
            'password': 'testpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, monkeypatch):
    monkeypatch.setattr('fast_zero.app.database', [])
    user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    }
    client.post('/users/', json=user)

    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client, monkeypatch):
    monkeypatch.setattr('fast_zero.app.database', [])

    response = client.delete('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_invalid_id(client, monkeypatch):
    monkeypatch.setattr('fast_zero.app.database', [])

    response = client.delete('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_twice_returns_not_found(client, monkeypatch):
    monkeypatch.setattr('fast_zero.app.database', [])
    user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    }
    client.post('/users/', json=user)

    first_response = client.delete('/users/1')
    assert first_response.status_code == HTTPStatus.OK

    second_response = client.delete('/users/1')
    assert second_response.status_code == HTTPStatus.NOT_FOUND
    assert second_response.json() == {'detail': 'User not found'}
