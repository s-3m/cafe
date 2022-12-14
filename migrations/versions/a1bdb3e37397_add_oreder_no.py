"""add oreder no

Revision ID: a1bdb3e37397
Revises: 137a2b1ff108
Create Date: 2022-10-31 16:17:20.240245

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.schema import Sequence, CreateSequence


# revision identifiers, used by Alembic.
revision = 'a1bdb3e37397'
down_revision = '137a2b1ff108'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(text("""ALTER TABLE orders ADD number SERIAL"""))


def downgrade() -> None:
    op.drop_column('orders', 'order_number')
