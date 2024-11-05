from models.users import User


def test_get_users(client, users_url):
    response = client.get(users_url)
    status_code = response.status_code
    content = response.json()

    assert status_code == 200
    assert isinstance(content, list)


def test_get_user(fake, session, client, users_url):
    user = User(
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        hashed_password=fake.password()
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    response = client.get(f'{users_url}/{user.pk}')
    status_code = response.status_code
    content = response.json()

    assert status_code == 200
    assert content['email'] == user.email
    assert content['first_name'] == user.first_name
    assert content['last_name'] == user.last_name
    assert content['is_active'] == user.is_active
    assert 'pk' in content
    assert 'created_at' in content
    assert 'updated_at' in content


def test_post_user(client, fake, users_url):
    json = {
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'password': fake.password()
    }

    response = client.post(url=users_url, json=json)
    status_code = response.status_code
    content = response.json()

    assert status_code == 201
    assert 'email' in content
    assert 'first_name' in content
    assert 'last_name' in content
    assert 'pk' in content
    assert 'is_active' in content
    assert 'created_at' in content
    assert 'updated_at' in content
