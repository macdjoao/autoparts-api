from datetime import datetime, timezone
import uuid
from typing import Optional

from pydantic import EmailStr, field_validator, BaseModel
from sqlmodel import Relationship, SQLModel, Field

# Only inherit from data models, don't inherit from table models. (https://sqlmodel.tiangolo.com/tutorial/fastapi/multiple-models/#inheritance-and-table-models)


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True)
    first_name: str
    last_name: str
    is_admin: bool = Field(default=False)

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
        timezone.utc), nullable=False, sa_column_kwargs={'onupdate': lambda: datetime.now(timezone.utc)})
    hashed_password: str = Field(nullable=False)

    # Relacionamentos
    # https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/define-relationships-attributes/#declare-relationship-attributes
    # https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/back-populates/
    # cascade_delete serve para o SQLModel deletar manufacturers ligadas ao user quando este for deletado
    # https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/cascade-delete-relationships/#set-ondelete-to-cascade
    manufacturer_creator: list['Manufacturer'] = Relationship(
        back_populates='creator',
        cascade_delete=True,
        sa_relationship_kwargs={'foreign_keys': 'Manufacturer.created_by'}
    )
    manufacturer_updater: list['Manufacturer'] = Relationship(
        back_populates='updater',
        cascade_delete=True,
        sa_relationship_kwargs={'foreign_keys': 'Manufacturer.updated_by'}
    )
    vehicle_creator: list['Vehicle'] = Relationship(
        back_populates='creator',
        cascade_delete=True,
        sa_relationship_kwargs={'foreign_keys': 'Vehicle.created_by'}
    )
    vehicle_updater: list['Vehicle'] = Relationship(
        back_populates='updater',
        cascade_delete=True,
        sa_relationship_kwargs={'foreign_keys': 'Vehicle.updated_by'}
    )
    part_creator: list['Part'] = Relationship(
        back_populates='creator',
        cascade_delete=True,
        sa_relationship_kwargs={'foreign_keys': 'Part.created_by'}
    )
    part_updater: list['Part'] = Relationship(
        back_populates='updater',
        cascade_delete=True,
        sa_relationship_kwargs={'foreign_keys': 'Part.updated_by'}
    )


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    pk: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(UserBase):
    email: EmailStr
    first_name: str
    last_name: str


class UserPartialUpdate(UserBase):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None

    @field_validator('email')
    @classmethod
    def email_not_none(cls, v: EmailStr | None) -> EmailStr | None:
        if v is None:
            raise ValueError('email field cannot be null')
        return v


class UserFilter(BaseModel):
    pk: Optional[uuid.UUID] = Field(None, description='Chave primária')
    email: Optional[EmailStr] = Field(None, description='Email')
    first_name: Optional[str] = Field(None, description='Primeiro nome')
    last_name: Optional[str] = Field(None, description='Último nome')
    is_active: Optional[bool] = Field(None, description='Ativo')
    is_admin: Optional[bool] = Field(None, description='Administrador')
