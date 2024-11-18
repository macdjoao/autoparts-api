"""add email and lastname in User table

Revision ID: edab2731e46a
Revises: 7de011b2d5a4
Create Date: 2024-10-17 20:11:03.330203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'edab2731e46a'
down_revision: Union[str, None] = '7de011b2d5a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.add_column('users', sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###