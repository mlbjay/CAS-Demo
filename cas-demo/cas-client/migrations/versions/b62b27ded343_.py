"""empty message

Revision ID: b62b27ded343
Revises: 03a87cce8398
Create Date: 2018-12-29 14:16:01.491733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b62b27ded343'
down_revision = '03a87cce8398'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('service_ticket',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('st', sa.String(length=100), nullable=False),
    sa.Column('validate', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('service_ticket')
    # ### end Alembic commands ###
