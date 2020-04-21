"""add consumed column to media

Revision ID: 96d7aa4b4895
Revises: 7e43b75b7a9b
Create Date: 2017-12-21 19:54:28.613492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96d7aa4b4895'
down_revision = '7e43b75b7a9b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('media', sa.Column('consumed', sa.Boolean, default=False))
    op.execute(
        """
        UPDATE media
        SET consumed = 'f';
        """
    )


def downgrade():
    op.drop_column('media', 'consumed')
