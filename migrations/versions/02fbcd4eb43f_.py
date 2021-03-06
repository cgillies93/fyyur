"""empty message

Revision ID: 02fbcd4eb43f
Revises: 59d56a6da735
Create Date: 2020-07-06 18:21:14.528668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02fbcd4eb43f'
down_revision = '59d56a6da735'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_performances', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('seeking_performers', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'seeking_performers')
    op.drop_column('Artist', 'seeking_performances')
    # ### end Alembic commands ###
