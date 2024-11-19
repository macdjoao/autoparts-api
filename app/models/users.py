from datetime import datetime, timezone
import uuid
from typing import Optional

from pydantic import EmailStr, field_validator, BaseModel
from sqlmodel import SQLModel, Field

# Only inherit from data models, don't inherit from table models. (https://sqlmodel.tiangolo.com/tutorial/fastapi/multiple-models/#inheritance-and-table-models)


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True)
    first_name: str
    last_name: str

    @field_validator('first_name', 'last_name')
    @classmethod
    def capitalize_names(cls, v: str) -> str:
        return v.capitalize()


class User(UserBase, table=True):
    __tablename__ = 'users'

    pk: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(
        timezone.utc), nullable=False, sa_column_kwargs={'onupdate': lambda: datetime.now(timezone.utc)})
    hashed_password: str = Field(nullable=False)


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    pk: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(UserBase):
    email: EmailStr
    first_name: str
    last_name: str


class UserPartialUpdate(UserBase):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None

    @field_validator('email')
    @classmethod
    def email_not_none(cls, v: EmailStr | None) -> EmailStr | None:
        if v is None:
            raise ValueError('email field cannot be null')
        return v


class UserFilter(BaseModel):
    pk: Optional[uuid.UUID] = Field(None, description='Chave primária')
    email: Optional[EmailStr] = Field(None, description='Email')
    first_name: Optional[str] = Field(None, description='Primeiro nome')
    last_name: Optional[str] = Field(None, description='Último nome')
    is_active: Optional[bool] = Field(True, description='Ativo')
