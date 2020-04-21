"""add id pk column to media

Revision ID: 084b664be4eb
Revises: 75647cfb1050
Create Date: 2018-03-12 19:49:48.698348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '084b664be4eb'
down_revision = '75647cfb1050'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('media_pkey', 'media', 'primary')
    op.add_column('media', sa.Column('id', sa.Integer, primary_key=True))
    op.create_primary_key('media_pkey', 'media', ['id'])


def downgrade():
    op.drop_constraint('media_pkey', 'media', 'primary')
    op.drop_column('media', 'id')
    op.create_primary_key('media_pkey', 'media', ['medianame', 'user'])
