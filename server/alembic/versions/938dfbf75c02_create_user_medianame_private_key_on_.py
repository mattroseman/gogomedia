"""create user/medianame private key on media table

Revision ID: 938dfbf75c02
Revises: 96d7aa4b4895
Create Date: 2017-12-21 20:29:27.843531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '938dfbf75c02'
down_revision = '96d7aa4b4895'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('media_pkey', 'media', 'primary')
    op.drop_column('media', 'id')
    op.create_primary_key('media_pkey', 'media', ['medianame', 'user'])


def downgrade():
    op.drop_constraint('media_pkey', 'media', 'primary')
    op.add_column('media', sa.Column('id', sa.Integer, primary_key=True))
    op.create_primary_key('media_pkey', 'media', ['id'])
