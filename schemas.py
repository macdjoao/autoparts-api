from pydantic import BaseModel


class User(BaseModel):
    pk: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
