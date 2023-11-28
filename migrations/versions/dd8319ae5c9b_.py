"""empty message

Revision ID: dd8319ae5c9b
Revises: dac69e7b8cfb
Create Date: 2023-11-28 19:58:58.215129

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dd8319ae5c9b'
down_revision = 'dac69e7b8cfb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_token', schema=None) as batch_op:
        batch_op.add_column(sa.Column('login_time', sa.DateTime(), nullable=True))
        batch_op.drop_column('create_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_token', schema=None) as batch_op:
        batch_op.add_column(sa.Column('create_time', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('login_time')

    # ### end Alembic commands ###