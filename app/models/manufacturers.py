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
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={'onupdate': lambda: datetime.now(timezone.utc)}
    )
    created_by: uuid.UUID = Field(foreign_key='users.pk')
    updated_by: uuid.UUID = Field(foreign_key='users.pk')


class ManufacturerCreate(ManufacturerBase):
    pass


class ManufacturerPublic(ManufacturerBase):
    pk: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: uuid.UUID
    updated_by: uuid.UUID


class ManufacturerUpdate(ManufacturerBase):
    is_active: bool


class ManufacturerPartialUpdate(ManufacturerBase):
    name: str | None = None
    is_active: bool | None = None

    @field_validator('name')
    @classmethod
    def name_not_none(cls, v: str | None) -> str | None:
        if v is None:
            raise ValueError('name field cannot be null')
        return v

    @field_validator('is_active')
    @classmethod
    def is_active_not_none(cls, v: bool | None) -> bool | None:
        if v is None:
            raise ValueError('is_active field cannot be null')
        return v
