from sqlmodel import select

from app.models.users import User
from app.security.auth import get_password_hash
from app.utils.settings import settings
from app.utils.dependencies import session


def register_admin():

    admin_already_registered = session.exec(
        select(User).where(User.email == settings.ADMIN_EMAIL)).first()
    if admin_already_registered or settings.CREATE_ADMIN == False:
        pass
    else:
        admin = User(
            email=settings.ADMIN_EMAIL,
            first_name='Admin',
            last_name='Admin',
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            is_admin=True
        )
        session.add(admin)
        session.commit()
        session.refresh(admin)
