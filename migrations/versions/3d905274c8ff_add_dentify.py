"""add dentify

Revision ID: 3d905274c8ff
Revises: 0bb6b1438d39
Create Date: 2022-11-01 16:32:59.130620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d905274c8ff'
down_revision = '0bb6b1438d39'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('orders', sa.Column('number', sa.Integer, sa.Identity(start=1)))


def downgrade() -> None:
    pass
