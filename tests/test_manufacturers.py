manufacturers_url = '/api/v1/manufacturers'

# Nomenclatura: test_recurso_verbo_informacaoExtra


def test_manufacturers_get_list(client, create_manufacturer, token):

    create_manufacturer()
    headers = {'Authorization': f'Bearer {token()}'}

    response = client.get(url=manufacturers_url, headers=headers)
    content = response.json()
    manufacturer = content[0]

    assert response.status_code == 200
    assert isinstance(content, list)
    assert 'pk' in manufacturer
    assert 'created_at' in manufacturer
    assert 'updated_at' in manufacturer
    assert 'created_by' in manufacturer
    assert 'updated_by' in manufacturer
    assert 'name' in manufacturer
    assert 'is_active' in manufacturer


def test_manufacturers_get_filtered(client, create_manufacturer, token):

    headers = {'Authorization': f'Bearer {token()}'}

    pk_manufacturer = create_manufacturer()
    pk_response = client.get(
        url=manufacturers_url,
        headers=headers,
        params={'pk': pk_manufacturer.pk}
    )
    pk_content = pk_response.json()[0]

    name_manufacturer = create_manufacturer()
    name_response = client.get(
        url=manufacturers_url,
        headers=headers,
        params={'name': name_manufacturer.name}
    )
    name_content = name_response.json()[0]

    is_active_manufacturer = create_manufacturer()
    is_active_response = client.get(
        url=manufacturers_url,
        headers=headers,
        params={'is_active': is_active_manufacturer.is_active}
    )
    is_active_content = is_active_response.json()[0]

    assert pk_response.status_code == 200
    assert str(pk_manufacturer.pk) == pk_content.get('pk')

    assert name_response.status_code == 200
    assert name_manufacturer.name == name_content.get('name')

    assert is_active_response.status_code == 200
    assert is_active_manufacturer.is_active == is_active_content.get(
        'is_active'
    )


def test_manufacturers_post(client, token, fake):

    headers = {'Authorization': f'Bearer {token()}'}
    name = fake.word()
    json = {'name': name}

    response = client.post(url=manufacturers_url, headers=headers, json=json)
    content = response.json()

    assert response.status_code == 201
    assert content['name'] == name.capitalize()
    assert 'pk' in content
    assert 'is_active' in content
    assert 'created_at' in content
    assert 'updated_at' in content
    assert 'created_by' in content
    assert 'updated_by' in content


def test_manufacturers_post_name_already_registered(client, token, create_manufacturer):

    manufacturer = create_manufacturer()
    headers = {'Authorization': f'Bearer {token()}'}
    json = {'name': manufacturer.name}

    response = client.post(url=manufacturers_url, headers=headers, json=json)
    content = response.json()

    assert response.status_code == 409
    assert content['detail'] == f'Name {manufacturer.name} already registered'


def test_manufacturers_get_one(client, create_manufacturer, token):

    manufacturer = create_manufacturer()
    headers = {'Authorization': f'Bearer {token()}'}

    response = client.get(
        url=f'{manufacturers_url}/{manufacturer.pk}',
        headers=headers
    )
    content = response.json()

    assert response.status_code == 200
    assert content['pk'] == str(manufacturer.pk)
    assert content['name'] == manufacturer.name
    assert content['is_active'] == manufacturer.is_active
    assert content['created_by'] == str(manufacturer.created_by)
    assert content['updated_by'] == str(manufacturer.updated_by)
    assert 'created_at' in content
    assert 'updated_at' in content
