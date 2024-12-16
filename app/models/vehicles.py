from datetime import datetime, timezone
from enum import Enum
import uuid

from pydantic import field_validator
from sqlmodel import Relationship, SQLModel, Field

from app.models.manufacturers import Manufacturer
from app.models.users import User


class Transmission(str, Enum):
    automatic = 'automatic'
    manual = 'manual'


class VehicleBase(SQLModel):
    name: str
    year: int = Field(nullable=False, ge=1886) # Primeiro carro foi fabricado em 1886
    transmission: Transmission

    @field_validator('name')
    @classmethod
    def capitalize_name(cls, v: str) -> str:
        return v.capitalize()
    

class Vehicle(VehicleBase, table=True):
    __tablename__ = 'vehicles'

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
    created_by: uuid.UUID = Field(foreign_key='users.pk', ondelete='CASCADE')
    updated_by: uuid.UUID = Field(foreign_key='users.pk', ondelete='CASCADE')
    manufacturer_pk: uuid.UUID = Field(foreign_key='manufacturers.pk', ondelete='CASCADE')

    creator: User = Relationship(
        back_populates='vehicle_creator',
        sa_relationship_kwargs={'foreign_keys': 'Vehicle.created_by'}
    )
    updater: User = Relationship(
        back_populates='vehicle_updater',
        sa_relationship_kwargs={'foreign_keys': 'Vehicle.updated_by'}
    )
    manufacturer: Manufacturer = Relationship(
        back_populates='vehicle_manufacturer',
        sa_relationship_kwargs={'foreign_keys': 'Vehicle.manufacturer_pk'}
    )
