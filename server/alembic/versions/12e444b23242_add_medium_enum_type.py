"""add medium enum type

Revision ID: 12e444b23242
Revises: f3a640b8e14b
Create Date: 2018-02-28 15:22:10.869953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12e444b23242'
down_revision = 'f3a640b8e14b'
branch_labels = None
depends_on = None

medium_type = sa.Enum('film', 'audio', 'literature', 'other', name='medium_type', validate_strings=True)


def upgrade():
    medium_type.create(op.get_bind())

    op.add_column('media', sa.Column('medium', medium_type, default='other'))
    op.execute(
        """
        UPDATE media
        SET medium='other';
        """
    )


def downgrade():
    op.drop_column('media', 'medium')
    medium_type.drop(op.get_bind())
