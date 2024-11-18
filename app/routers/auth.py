from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.models.token import Login, Token
from app.models.users import User
from app.settings.settings import settings
from app.utils.dependencies import get_session
from app.utils.exceptions import raise_incorrect_email_or_password_exception, raise_internal_server_error_exception
from app.utils.security import authenticate_user, create_access_token


router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


@router.post(
    '/token',
    response_model=Token,
    status_code=status.HTTP_202_ACCEPTED,
    summary='Resgata token',
    description='Resgata token de acesso ao sistema.'
)
async def get_token(credentials: Login, session: Session = Depends(get_session)):
    try:
        user = session.exec(select(User).where(
            User.email == credentials.email)).first()
        if not user:
            raise_incorrect_email_or_password_exception()
        authenticated = authenticate_user(user, credentials.password)
        if not authenticated:
            raise_incorrect_email_or_password_exception()
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={'sub': user.email}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token)
    except HTTPException as exc:
        raise exc
    except Exception:
        raise_internal_server_error_exception()
