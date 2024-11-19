from sqlmodel import create_engine, Session

from app.utils.settings import settings


engine = create_engine(settings.DB_URL, echo=True)
session = Session(engine)


def get_session():
    try:
        yield session
    finally:
        session.close()
