from datetime import datetime, timezone
import uuid

from pydantic import field_validator
from sqlmodel import Relationship, SQLModel, Field

from app.models.users import User
from app.models.vehicles import Vehicle


class PartBase(SQLModel):
    name: str
    quantity: int = Field(default=0)

    @field_validator('name')
    @classmethod
    def capitalize_name(cls, v: str) -> str:
        return v.capitalize()
    

class Part(PartBase, table=True):
    __tablename__ = 'parts'

    pk: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )
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
    vehicle_pk: uuid.UUID = Field(foreign_key='vehicles.pk', ondelete='CASCADE')

    creator: User = Relationship(
        back_populates='part_creator',
        sa_relationship_kwargs={'foreign_keys': 'Part.created_by'}
    )
    updater: User = Relationship(
        back_populates='part_updater',
        sa_relationship_kwargs={'foreign_keys': 'Part.updated_by'}
    )
    vehicle: Vehicle = Relationship(
        back_populates='part_vehicle',
        sa_relationship_kwargs={'foreign_keys': 'Part.vehicle_pk'}
    )