from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.models.token import TokenData
from app.models.users import User
from app.utils.settings import settings
from app.utils.dependencies import get_session
from app.utils.exceptions import raise_credentials_exception


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(user: User, password: str):
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get('sub')
        if username is None:
            raise_credentials_exception()
        token_data = TokenData(email=username)
    except jwt.InvalidTokenError:
        raise_credentials_exception()
    db_user = session.exec(select(User).where(
        User.email == token_data.email)).first()
    if db_user is None:
        raise_credentials_exception()
    return db_user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user


async def is_admin(current_user: User = Depends(get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail='Only admin users can perform this action')
    return current_user
