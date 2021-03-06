"""Confirmed users

Revision ID: 40337e48c56
Revises: 184f80c6135
Create Date: 2015-03-31 16:42:04.761114

"""

# revision identifiers, used by Alembic.
revision = '40337e48c56'
down_revision = '184f80c6135'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    ### end Alembic commands ###
