"""empty message

Revision ID: 59d56a6da735
Revises: 891d98d37488
Create Date: 2020-07-06 16:08:00.223780

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59d56a6da735'
down_revision = '891d98d37488'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'genres')
    # ### end Alembic commands ###
