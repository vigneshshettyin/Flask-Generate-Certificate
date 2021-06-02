"""empty message

Revision ID: 83ee0e3f7f53
Revises: 5c027f8caf84
Create Date: 2021-06-02 22:54:20.514400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83ee0e3f7f53'
down_revision = '5c027f8caf84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fonts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fonts')
    # ### end Alembic commands ###
