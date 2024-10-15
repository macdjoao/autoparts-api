from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = 'users'

    pk: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )
    is_active: bool = Field(default=True)
    first_name: str
    created_at: datetime = Field(sa_column=Column(
        DateTime(timezone=True), default=datetime.now()))
    updated_at: datetime = Field(sa_column=Column(
        DateTime(timezone=True), onupdate=datetime.now(), default=datetime.now()))


# from datetime import datetime
# from typing import Optional
# import uuid

# from pydantic import BaseModel, EmailStr, field_validator


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
