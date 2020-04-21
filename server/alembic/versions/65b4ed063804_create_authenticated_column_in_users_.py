"""create authenticated column in users table

Revision ID: 65b4ed063804
Revises: 31a043de32ae
Create Date: 2018-02-22 17:38:13.399189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65b4ed063804'
down_revision = '31a043de32ae'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('authenticated', sa.Boolean, default=False))
    op.execute(
        """
        UPDATE users
        SET authenticated='f';
        """
    )


def downgrade():
    op.drop_column('users', 'authenticated')
