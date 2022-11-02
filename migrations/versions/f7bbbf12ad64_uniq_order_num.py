"""uniq order num

Revision ID: f7bbbf12ad64
Revises: 3d905274c8ff
Create Date: 2022-11-02 17:43:43.389720

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7bbbf12ad64'
down_revision = '3d905274c8ff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('orders', sa.Column('number', sa.Integer, sa.Identity(start=1), unique=True))


def downgrade() -> None:
    pass
