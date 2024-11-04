from fastapi import status

from settings.settings import settings


def test_get_users(client):

    response = client.get(f'{settings.URI_PREFIX}/users')
    status_code = response.status_code
    content = response.json()

    assert status_code == status.HTTP_200_OK
    assert isinstance(content, list)


def test_get_user():
    pass


def test_post_user(client, fake):

    url = f'{settings.URI_PREFIX}/users'
    json = {
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'password': fake.password()
    }
    response = client.post(url=url, json=json)
    status_code = response.status_code
    content = response.json()

    assert status_code == status.HTTP_201_CREATED
    assert 'email' in content
    assert 'first_name' in content
    assert 'last_name' in content
    assert 'pk' in content
    assert 'is_active' in content
    assert 'created_at' in content
    assert 'updated_at' in content
