"""remove salt column in users

Revision ID: 29d49a45b453
Revises: 65b4ed063804
Create Date: 2018-02-22 18:31:06.916840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29d49a45b453'
down_revision = '65b4ed063804'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('users', 'passsalt')


def downgrade():
    op.add_column('users', sa.Column('passsalt', sa.String(29)))
