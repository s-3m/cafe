"""add table status and column in order

Revision ID: 0bb6b1438d39
Revises: a1bdb3e37397
Create Date: 2022-11-01 12:56:59.221053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bb6b1438d39'
down_revision = 'a1bdb3e37397'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('orders', sa.Column('status', sa.Integer, sa.ForeignKey("status.id")))


def downgrade() -> None:
    op.drop_column('orders', 'status')
