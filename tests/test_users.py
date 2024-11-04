from fastapi.testclient import TestClient
from fastapi import status

from main import app
from settings.settings import settings

client = TestClient(app)


def test_get_users():
    client = TestClient(app)

    response = client.get(f'{settings.URI_PREFIX}/users')

    status_code = response.status_code
    content = response.json()

    assert status_code == status.HTTP_200_OK
    assert isinstance(content, list)
