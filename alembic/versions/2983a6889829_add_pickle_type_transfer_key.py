"""Add Pickle Type Transfer Key

Revision ID: 2983a6889829
Revises: f24371202013
Create Date: 2016-02-13 05:56:31.456652

"""

# revision identifiers, used by Alembic.
revision = '2983a6889829'
down_revision = 'f24371202013'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('transfers', sa.Column('transfer_list', sa.PickleType))


def downgrade():
    op.drop_column('transfers', 'stpkey')
    
