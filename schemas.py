from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    pk: str
    is_active: Optional[bool] = True
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
