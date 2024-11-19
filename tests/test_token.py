token_url = '/api/v1/auth/token'


def test_success_post_token(client, create_specific_user, fake):

    email = fake.email()
    password = fake.password()
    create_specific_user(
        email=email,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        hashed_password=password
    )
    data = {
        'username': email,
        'password': password
    }

    response = client.post(url=token_url, data=data)
    content = response.json()

    assert response.status_code == 202
    assert isinstance(content.get('access_token'), str)
    assert content.get('token_type') == 'bearer'


def test_fail_post_token_incorrect_email_or_password(client, fake):

    data = {
        'username': fake.email(),
        'password': fake.password()
    }

    response = client.post(url=token_url, data=data)
    content = response.json()

    assert response.status_code == 401
    assert content.get('detail') == 'Incorrect email or password'
