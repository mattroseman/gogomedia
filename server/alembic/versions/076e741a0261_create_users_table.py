"""create users table

Revision ID: 076e741a0261
Revises:
Create Date: 2017-12-19 15:45:49.742333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '076e741a0261'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
    )


def downgrade():
    op.drop_table('users')
