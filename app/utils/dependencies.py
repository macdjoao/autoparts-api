import redis
from sqlmodel import create_engine, Session

from app.utils.settings import settings


engine = create_engine(settings.DB_URL, echo=True)
session = Session(engine)


def get_session():
    try:
        yield session
    finally:
        session.close()


def get_redis() -> redis.Redis:
    r = redis.Redis(
        # host=settings.CACHE_HOST,
        # port=settings.CACHE_DB,
        db=settings.CACHE_DB,
        decode_responses=True
    )
    return r
