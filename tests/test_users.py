users_url = '/api/v1/users'

# Nomenclatura: test_recurso_verbo_informacaoExtra


def test_users_get_list(client, create_user, token):

    create_user()
    headers = {'Authorization': f'Bearer {token()}'}

    response = client.get(url=users_url, headers=headers)
    content = response.json()
    user = content[0]

    assert response.status_code == 200
    assert isinstance(content, list)
    assert 'pk' in user
    assert 'created_at' in user
    assert 'updated_at' in user
    assert 'email' in user
    assert 'first_name' in user
    assert 'last_name' in user
    assert 'is_active' in user


def test_users_get_list_filtered(client, create_named_user, token):

    headers = {'Authorization': f'Bearer {token()}'}

    arthur = create_named_user(first_name='arthur')  # pk
    thomas = create_named_user(first_name='thomas')  # email
    john = create_named_user(first_name='john')  # first_name
    ada = create_named_user(first_name='ada')  # last_name
    finn = create_named_user(first_name='finn', is_active=False)  # is_active
    polly = create_named_user(first_name='polly', is_admin=True)  # is_admin

    arthur_response = client.get(
        url=users_url, headers=headers, params={'pk': arthur.pk}
    )
    arthur_content = arthur_response.json()[0]

    thomas_response = client.get(
        url=users_url, headers=headers, params={'email': thomas.email}
    )
    thomas_content = thomas_response.json()[0]

    john_response = client.get(
        url=users_url, headers=headers, params={'first_name': john.first_name}
    )
    john_content = john_response.json()[0]

    ada_response = client.get(
        url=users_url, headers=headers, params={'last_name': ada.last_name}
    )
    ada_content = ada_response.json()[0]

    finn_response = client.get(
        url=users_url, headers=headers, params={'is_active': finn.is_active}
    )
    finn_content = finn_response.json()[0]

    polly_response = client.get(
        url=users_url, headers=headers, params={'is_admin': polly.is_admin}
    )
    polly_content = polly_response.json()[0]

    assert arthur_response.status_code == 200
    assert str(arthur.pk) == arthur_content.get('pk')

    assert thomas_response.status_code == 200
    assert thomas.email == thomas_content.get('email')

    assert john_response.status_code == 200
    assert john.first_name == john_content.get('first_name')

    assert ada_response.status_code == 200
    assert ada.last_name == ada_content.get('last_name')

    assert finn_response.status_code == 200
    assert finn.is_active == finn_content.get('is_active')

    assert polly_response.status_code == 200
    assert polly.is_admin == polly_content.get('is_admin')


def test_users_get_one(client, create_user, token):

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


def test_users_post(client, fake, token):

    headers = {'Authorization': f'Bearer {token(is_admin=True)}'}
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


def test_users_patch(client, create_user, fake, token):

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


def test_users_delete(client, create_user, token):

    user = create_user()
    headers = {'Authorization': f'Bearer {token(is_admin=True)}'}

    response = client.delete(url=f'{users_url}/{user.pk}', headers=headers)
    status_code = response.status_code

    assert status_code == 204


def test_users_put(client, create_user, fake, token):

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


def test_users_put_missing_fields(client, create_user, fake, token):

    user = create_user()
    json = {'email': fake.email()}
    headers = {'Authorization': f'Bearer {token()}'}

    response = client.put(f'{users_url}/{user.pk}', json=json, headers=headers)
    status_code = response.status_code
    content = response.json()

    assert status_code == 422
    assert len(content['detail']) == 2
    assert content['detail'][0]['type'] == 'missing'


def test_users_all_invalid_pk(client, fake, token):

    invalid_pk = fake.word()
    headers = {'Authorization': f'Bearer {token(is_admin=True)}'}

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


def test_users_all_pk_not_found(client, fake, token):

    valid_pk = fake.uuid4()
    headers = {'Authorization': f'Bearer {token(is_admin=True)}'}
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


def test_users_all_email_already_registered(client, fake, create_specific_user, create_user, token):

    email = fake.email()
    create_specific_user(
        email=email,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        hashed_password=fake.password()
    )
    user = create_user()
    headers = {'Authorization': f'Bearer {token(is_admin=True)}'}
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


def test_users_all_invalid_email(client, fake, token, create_user):

    email = fake.word()
    user = create_user()
    headers = {'Authorization': f'Bearer {token(is_admin=True)}'}
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


def test_users_all_email_not_null(client, create_user, token):

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


def test_users_all_not_admin(client, token, fake, create_user):

    headers = {'Authorization': f'Bearer {token(is_admin=False)}'}
    json = {
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'password': fake.password()
    }
    user = create_user()

    post_response = client.post(url=users_url, json=json, headers=headers)
    post_content = post_response.json()

    delete_response = client.delete(
        url=f'{users_url}/{user.pk}',
        headers=headers
    )
    delete_content = delete_response.json()

    assert post_response.status_code == 403
    assert post_content['detail'] == 'Only admin users can perform this action'
    assert delete_response.status_code == 403
    assert delete_content['detail'] == 'Only admin users can perform this action'
