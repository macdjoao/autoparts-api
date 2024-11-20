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
