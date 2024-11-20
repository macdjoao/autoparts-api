import pytest
from fastapi.testclient import TestClient
from faker import Faker
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.models.manufacturers import Manufacturer
from app.models.users import User
from app.utils.dependencies import get_session
from app.security.auth import get_password_hash


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
def create_user(fake, session):
    def _create_user():
        user = User(
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            hashed_password=get_password_hash(fake.password())
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    return _create_user


@pytest.fixture
# Recebe outras fixtures como parametro
def create_specific_user(session):
    # Recebe parametros "comuns"
    def _create_specific_user(email, first_name, last_name, hashed_password, is_admin=False):
        user = User(
            email=email,
            first_name=first_name.capitalize(),
            last_name=last_name.capitalize(),
            hashed_password=get_password_hash(hashed_password),
            is_admin=is_admin
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    return _create_specific_user


@pytest.fixture
def token(create_specific_user, fake, client):
    def _token(is_admin=False):
        password = fake.password()
        user = create_specific_user(
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            hashed_password=password,
            is_admin=is_admin
        )

        data = {
            'username': user.email,
            'password': password
        }
        response = client.post(
            '/api/v1/auth/token',
            data=data
        )

        return response.json()['access_token']
    return _token


@pytest.fixture
def create_named_user(session, fake):
    def _create_named_user(first_name, is_active=True, is_admin=False):
        user = User(
            email=fake.email(),
            first_name=first_name.capitalize(),
            last_name=fake.last_name(),
            hashed_password=get_password_hash(fake.password()),
            is_active=is_active,
            is_admin=is_admin
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    return _create_named_user


@pytest.fixture
def create_manufacturer(fake, session, create_user):
    def _create_manufacturer():
        user = create_user()
        manufacturer = Manufacturer(
            name=fake.word().capitalize(),
            created_by=user.pk,
            updated_by=user.pk
        )
        session.add(manufacturer)
        session.commit()
        session.refresh(manufacturer)
        return manufacturer
    return _create_manufacturer
