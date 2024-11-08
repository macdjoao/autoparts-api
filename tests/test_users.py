users_url = '/api/v1/users'


def test_get_users_200_ok(client):

    response = client.get(users_url)
    status_code = response.status_code
    content = response.json()

    assert status_code == 200
    assert isinstance(content, list)


def test_get_user_200_ok(client, create_user):

    user = create_user()

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


def test_get_user_422_invalid_pk(client, fake):

    invalid_pk = fake.word()

    response = client.get(f'{users_url}/{invalid_pk}')
    status_code = response.status_code

    assert status_code == 422


def test_get_user_404_pk_not_found(client, fake):

    random_valid_pk = fake.uuid4()

    response = client.get(f'{users_url}/{random_valid_pk}')
    status_code = response.status_code
    content = response.json()

    assert status_code == 404
    assert content['detail'] == f'No record with pk {random_valid_pk}'


def test_post_user_201_created(client, fake):

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
