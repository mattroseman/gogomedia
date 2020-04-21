"""add order column to media

Revision ID: bdc68ba685c5
Revises: 2ce850686273
Create Date: 2018-03-16 20:14:21.338750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdc68ba685c5'
down_revision = '2ce850686273'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('media', sa.Column('order', sa.Integer, default=0))


def downgrade():
    op.drop_column('media', 'order')
