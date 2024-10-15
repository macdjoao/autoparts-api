from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, EmailStr, field_validator


class User(BaseModel):
    # Para trafegar dados do tipo data, usarei strings com formatação ISO-8601, padrão que RESTful segue
    pk: Optional[str] = str(uuid.uuid4)
    is_active: Optional[bool] = True
    created_by: Optional[str] = None
    created_at: Optional[str] = datetime.now().isoformat()
    updated_by: Optional[str] = None
    updated_at: Optional[str] = datetime.now().isoformat()
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    role: str

    @field_validator('first_name', 'last_name')
    @classmethod
    def capitalize_names(cls, v: str) -> str:
        return v.capitalize()

    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v: str) -> str:
        if len(v) < 5:
            raise ValueError('password must have at least 5 characters')
        return v
