"""create media table

Revision ID: 7e43b75b7a9b
Revises: 076e741a0261
Create Date: 2017-12-19 16:03:23.570204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e43b75b7a9b'
down_revision = '076e741a0261'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'media',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('medianame', sa.String(80), nullable=False),
        sa.Column('user', sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    )


def downgrade():
    op.drop_table('media')
