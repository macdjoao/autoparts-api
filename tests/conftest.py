import pytest
from fastapi.testclient import TestClient
from faker import Faker
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from main import app
from utils.database import get_session


# @pytest.fixture(name='fixture_name')
# Pode-se usar o parametro "name" para definir o nome da fixture e usá-la nos testes,
# do contrário deve-se usar o nome da função da fixture
@pytest.fixture
def session():
    engine = create_engine(
        'sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture
def users_url():
    return '/api/v1/users'
