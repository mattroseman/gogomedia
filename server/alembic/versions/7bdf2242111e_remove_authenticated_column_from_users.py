"""remove authenticated column from users

Revision ID: 7bdf2242111e
Revises: 29d49a45b453
Create Date: 2018-02-25 16:28:43.889815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bdf2242111e'
down_revision = '29d49a45b453'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('users', 'authenticated')


def downgrade():
    op.add_column('users', sa.Column('authenticated', sa.Boolean, default=False))
    op.execute(
        """
        UPDATE users
        SET authenticated='f';
        """
    )
