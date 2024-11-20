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
