"""change consumed column into a consumed_state column

Revision ID: 75647cfb1050
Revises: 12e444b23242
Create Date: 2018-03-06 14:29:49.617489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75647cfb1050'
down_revision = '12e444b23242'
branch_labels = None
depends_on = None

consumed_state_type = sa.Enum('not started', 'started', 'finished', name='consumed_state_type', validate_strings=True)


def upgrade():
    consumed_state_type.create(op.get_bind())

    op.add_column('media', sa.Column('consumed_state', consumed_state_type, default='not started'))
    op.execute(
        """
        UPDATE media
        SET consumed_state='not started'
        WHERE consumed=false;
        """
    )
    op.execute(
        """
        UPDATE media
        SET consumed_state='finished'
        WHERE consumed=true;
        """
    )

    op.drop_column('media', 'consumed')


def downgrade():
    op.add_column('media', sa.Column('consumed', sa.Boolean, default=False))
    op.execute(
        """
        UPDATE media
        SET consumed=false;
        """
    )
    op.execute(
        """
        UPDATE media
        SET consumed=true
        WHERE consumed_state='finished';
        """
    )

    op.drop_column('media', 'consumed_state')
    consumed_state_type.drop(op.get_bind())
