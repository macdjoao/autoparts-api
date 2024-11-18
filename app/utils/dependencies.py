from sqlmodel import create_engine, Session

from app.settings.settings import settings


engine = create_engine(settings.DB_URL, echo=True)
session = Session(engine)


def get_session():
    try:
        yield session
    finally:
        session.close()