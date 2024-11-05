import pytest
from fastapi.testclient import TestClient
from faker import Faker
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from main import app
from models.users import User
from utils.database import get_session


# @pytest.fixture(name='fixture_name')
# Pode-se usar o parametro "name" para definir o nome da fixture e usá-la nos testes,
# do contrário deve-se usar o nome da função da fixture
@pytest.fixture
def session():
    engine = create_engine(
        'sqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
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


@pytest.fixture
def create_user(fake, session):
    def _create_user():
        user = User(
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            hashed_password=fake.password()
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    return _create_user
