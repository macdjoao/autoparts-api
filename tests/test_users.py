users_url = '/api/v1/users'


def test_get_users_200_ok(client, create_user, token):

    create_user()
    headers = {'Authorization': f'Bearer {token()}'}

    response = client.get(url=users_url, headers=headers)
    status_code = response.status_code
    content = response.json()
    user = content[0]

    assert status_code == 200
    assert isinstance(content, list)
    assert 'pk' in user
    assert 'created_at' in user
    assert 'updated_at' in user
    assert 'email' in user
    assert 'first_name' in user
    assert 'last_name' in user
    assert 'is_active' in user


def test_get_user_200_ok(client, create_user, token):

    user = create_user()
    headers = {'Authorization': f'Bearer {token()}'}

    response = client.get(url=f'{users_url}/{user.pk}', headers=headers)
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


def test_post_user_201_created(client, fake, token):

    headers = {'Authorization': f'Bearer {token()}'}
    json = {
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'password': fake.password()
    }

    response = client.post(url=users_url, json=json, headers=headers)
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


def test_patch_user_202_accepted(client, create_user, fake, token):

    user = create_user()
    json = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name()
    }
    headers = {'Authorization': f'Bearer {token()}'}

    response = client.patch(
        url=f'{users_url}/{user.pk}',
        json=json,
        headers=headers
    )
    status_code = response.status_code
    content = response.json()

    assert status_code == 202
    assert content['first_name'] == json['first_name']
    assert content['last_name'] == json['last_name']
    assert content['updated_at'] > content['created_at']


def test_delete_user_204_no_content(client, create_user, token):

    user = create_user()
    headers = {'Authorization': f'Bearer {token()}'}

    response = client.delete(url=f'{users_url}/{user.pk}', headers=headers)
    status_code = response.status_code

    assert status_code == 204


def test_put_user_200_ok(client, create_user, fake, token):

    user = create_user()
    json = {
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name()
    }
    headers = {'Authorization': f'Bearer {token()}'}

    response = client.put(
        url=f'{users_url}/{user.pk}',
        json=json,
        headers=headers
    )
    status_code = response.status_code
    content = response.json()

    assert status_code == 200
    assert content['email'] == json['email']
    assert content['first_name'] == json['first_name']
    assert content['last_name'] == json['last_name']
    assert content['updated_at'] > content['created_at']


def test_put_user_422_missing_fields(client, create_user, fake, token):

    user = create_user()
    json = {'email': fake.email()}
    headers = {'Authorization': f'Bearer {token()}'}

    response = client.put(f'{users_url}/{user.pk}', json=json, headers=headers)
    status_code = response.status_code
    content = response.json()

    assert status_code == 422
    assert len(content['detail']) == 2
    assert content['detail'][0]['type'] == 'missing'


def test_user_422_invalid_pk(client, fake, token):

    invalid_pk = fake.word()
    headers = {'Authorization': f'Bearer {token()}'}

    get = client.get(url=f'{users_url}/{invalid_pk}', headers=headers)
    put = client.put(url=f'{users_url}/{invalid_pk}', headers=headers)
    patch = client.patch(url=f'{users_url}/{invalid_pk}', headers=headers)
    delete = client.delete(url=f'{users_url}/{invalid_pk}', headers=headers)

    get_response = get.json()['detail'][0]
    put_response = put.json()['detail'][0]
    patch_response = patch.json()['detail'][0]
    delete_response = delete.json()['detail'][0]

    assert get.status_code == 422 and get_response['type'] == 'uuid_parsing'
    assert put.status_code == 422 and put_response['type'] == 'uuid_parsing'
    assert patch.status_code == 422 and patch_response['type'] == 'uuid_parsing'
    assert delete.status_code == 422 and delete_response['type'] == 'uuid_parsing'


def test_user_404_pk_not_found(client, fake, token):

    valid_pk = fake.uuid4()
    headers = {'Authorization': f'Bearer {token()}'}
    # Prover json válido para PUT e PATCH não retornarem erro 422
    json = {
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name()
    }

    get = client.get(url=f'{users_url}/{valid_pk}', headers=headers)
    delete = client.delete(url=f'{users_url}/{valid_pk}', headers=headers)
    put = client.put(url=f'{users_url}/{valid_pk}', headers=headers, json=json)
    patch = client.patch(
        url=f'{users_url}/{valid_pk}',
        headers=headers,
        json=json
    )

    get_response = get.json()['detail']
    delete_response = delete.json()['detail']
    put_response = put.json()['detail']
    patch_response = patch.json()['detail']

    assert get.status_code == 404 and get_response == f'No record with pk {valid_pk}'
    assert delete.status_code == 404 and delete_response == f'No record with pk {valid_pk}'
    assert put.status_code == 404 and put_response == f'No record with pk {valid_pk}'
    assert patch.status_code == 404 and patch_response == f'No record with pk {valid_pk}'


def test_user_409_email_already_registered(client, fake, create_specific_user, create_user, token):

    email = fake.email()
    create_specific_user(
        email=email,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        hashed_password=fake.password()
    )
    user = create_user()
    headers = {'Authorization': f'Bearer {token()}'}
    json = {
        'email': email,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'password': fake.password()
    }

    post = client.post(url=users_url, json=json, headers=headers)
    put = client.put(url=f'{users_url}/{user.pk}', headers=headers, json=json)
    patch = client.patch(
        url=f'{users_url}/{user.pk}',
        headers=headers,
        json=json
    )

    post_response = post.json()['detail']
    put_response = put.json()['detail']
    patch_response = patch.json()['detail']

    assert post.status_code == 409 and post_response == f'Email {email} already registered'
    assert put.status_code == 409 and put_response == f'Email {email} already registered'
    assert patch.status_code == 409 and patch_response == f'Email {email} already registered'


def test_user_422_invalid_email(client, fake, token, create_user):

    email = fake.word()
    user = create_user()
    headers = {'Authorization': f'Bearer {token()}'}
    json = {
        'email': email,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'password': fake.password()
    }

    post = client.post(url=users_url, json=json, headers=headers)
    put = client.put(url=f'{users_url}/{user.pk}', headers=headers, json=json)
    patch = client.patch(
        url=f'{users_url}/{user.pk}',
        headers=headers,
        json=json
    )

    post_response = post.json()['detail'][0]['msg']
    put_response = put.json()['detail'][0]['msg']
    patch_response = patch.json()['detail'][0]['msg']

    assert post.status_code == 422 and post_response == 'value is not a valid email address: An email address must have an @-sign.'
    assert put.status_code == 422 and put_response == 'value is not a valid email address: An email address must have an @-sign.'
    assert patch.status_code == 422 and patch_response == 'value is not a valid email address: An email address must have an @-sign.'


def test_user_422_email_not_null(client, create_user, token):

    user = create_user()
    headers = {'Authorization': f'Bearer {token()}'}
    json = {'email': None}

    put = client.put(url=f'{users_url}/{user.pk}', json=json, headers=headers)
    patch = client.patch(
        url=f'{users_url}/{user.pk}',
        json=json,
        headers=headers
    )

    put_response = put.json()['detail'][0]['msg']
    patch_response = patch.json()['detail'][0]['msg']

    assert put.status_code == 422 and put_response == 'Input should be a valid string'
    assert patch.status_code == 422 and patch_response == 'Value error, email field cannot be null'
