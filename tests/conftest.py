import pytest
from fastapi.testclient import TestClient
from faker import Faker

from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def fake():
    return Faker(locale='pt_BR')
