"""empty message

Revision ID: 84bf6e26d411
Revises: 3fba85b3fdc2
Create Date: 2020-07-14 18:43:30.700922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84bf6e26d411'
down_revision = '3fba85b3fdc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('link', sa.Column('record', sa.String(length=4), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('link', 'record')
    # ### end Alembic commands ###