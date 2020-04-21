"""add blacklisted_tokens table

Revision ID: f3a640b8e14b
Revises: 7bdf2242111e
Create Date: 2018-02-25 16:31:19.638415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3a640b8e14b'
down_revision = '7bdf2242111e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'blacklisted_tokens',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('token', sa.String(500), unique=True, nullable=False),
        sa.Column('blacklisted_on', sa.DateTime, nullable=False)
    )


def downgrade():
    op.drop_table('blacklisted_tokens')
