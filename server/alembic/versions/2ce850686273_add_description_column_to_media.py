"""add description column to media

Revision ID: 2ce850686273
Revises: 084b664be4eb
Create Date: 2018-03-13 20:39:59.624623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ce850686273'
down_revision = '084b664be4eb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('media', sa.Column('description', sa.String(500)))


def downgrade():
    op.drop_column('media', 'description')
