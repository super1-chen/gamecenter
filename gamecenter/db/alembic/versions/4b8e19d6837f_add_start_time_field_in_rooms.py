"""add start_time field in rooms

Revision ID: 4b8e19d6837f
Revises: 66145020275c
Create Date: 2020-03-25 09:41:14.423042

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '4b8e19d6837f'
down_revision = '66145020275c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('rooms', sa.Column('start_time', sa.BigInteger(), nullable=True))


def downgrade():
    op.drop_column('rooms', 'start_time')
