from pydantic import field_validator
from sqlmodel import SQLModel, Field


class VehicleBase(SQLModel):
    name: str
    # Primeiro carro foi fabricado em 1886
    year: int = Field(nullable=False, ge=1886)
    transmission: str
    fuel: str

    @field_validator('name')
    @classmethod
    def capitalize_name(cls, v: str) -> str:
        return v.capitalize()
