"""create password hash column in users

Revision ID: 31a043de32ae
Revises: 938dfbf75c02
Create Date: 2018-02-22 14:33:06.236423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31a043de32ae'
down_revision = '938dfbf75c02'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('passhash', sa.String(60)))
    op.add_column('users', sa.Column('passsalt', sa.String(29)))


def downgrade():
    op.drop_column('users', 'passhash')
    op.drop_column('users', 'passsalt')
