from datetime import datetime, timezone
import uuid

from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel, Field

# Only inherit from data models, don't inherit from table models. (https://sqlmodel.tiangolo.com/tutorial/fastapi/multiple-models/#inheritance-and-table-models)


class UserBase(SQLModel):
    email: EmailStr
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
        timezone.utc), nullable=False, sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)})
    hashed_password: str = Field(nullable=False)


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    pk: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(UserBase):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None

# class UserSchema(BaseModel):
#     # Para trafegar dados do tipo data, usarei strings com formatação ISO-8601, padrão que RESTful segue
#     pk: Optional[str] = str(uuid.uuid4)
#     is_active: Optional[bool] = True
#     created_by: Optional[str] = None
#     created_at: Optional[str] = datetime.now().isoformat()
#     updated_by: Optional[str] = None
#     updated_at: Optional[str] = datetime.now().isoformat()
#     email: EmailStr
#     first_name: str
#     last_name: str
#     password: str
#     role: str

#     @field_validator('first_name', 'last_name')
#     @classmethod
#     def capitalize_names(cls, v: str) -> str:
#         return v.capitalize()

#     @field_validator('password')
#     @classmethod
#     def validate_password_length(cls, v: str) -> str:
#         if len(v) < 5:
#             raise ValueError('password must have at least 5 characters')
#         return v
