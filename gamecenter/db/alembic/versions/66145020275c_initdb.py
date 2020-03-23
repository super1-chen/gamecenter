"""initdb

Revision ID: 66145020275c
Revises: 
Create Date: 2020-03-22 22:40:34.669286

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '66145020275c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('games',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_time', sa.DateTime(), nullable=True),
                    sa.Column('update_time', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_time', sa.DateTime(), nullable=True),
                    sa.Column('uid', sa.VARCHAR(length=255), server_default=sa.text(u"''"), nullable=False),
                    sa.Column('name', sa.VARCHAR(length=255), server_default=sa.text(u"''"), nullable=False),
                    sa.Column('channel', sa.VARCHAR(length=128), server_default=sa.text(u"''"), nullable=False),
                    sa.Column('icon', sa.VARCHAR(length=1024), server_default=sa.text(u"''"), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('uid', 'channel', name='uid_channel_uc_name')
                    )
    op.create_table('rooms',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('create_time', sa.DateTime(), nullable=True),
                    sa.Column('status', sa.Boolean(), nullable=True),
                    sa.Column('people', sa.Integer(), nullable=True),
                    sa.Column('game_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('user_room_association',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('room_id', sa.Integer(), nullable=False),
                    sa.Column('status', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('user_id', 'room_id')
                    )


def downgrade():
    op.drop_table('user_room_association')
    op.drop_table('rooms')
    op.drop_table('users')
    op.drop_table('games')
