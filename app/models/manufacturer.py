from datetime import datetime, timezone
import uuid

from pydantic import field_validator
from sqlmodel import SQLModel, Field


class ManufacturerBase(SQLModel):
    name: str

    @field_validator('name')
    @classmethod
    def capitalize_name(cls, v: str) -> str:
        return v.capitalize()


class Manufacturer(ManufacturerBase, table=True):
    __tablename__ = 'manufacturers'

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
    # created_by
    # updated_by
