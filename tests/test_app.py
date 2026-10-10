from http import HTTPStatus


def test_read_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


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
