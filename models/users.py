from datetime import datetime
import uuid

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
    # created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=datetime.now()))
    # updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), onupdate=datetime.now(), default=datetime.now()))
