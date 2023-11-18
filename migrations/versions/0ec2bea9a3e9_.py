"""empty message

Revision ID: 0ec2bea9a3e9
Revises: 
Create Date: 2023-11-18 20:31:28.077729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ec2bea9a3e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('uid', sa.String(length=20), nullable=False, comment='工号'),
    sa.Column('username', sa.String(length=64), nullable=False, comment='用户名'),
    sa.Column('department_id', sa.String(length=20), nullable=False, comment='部门编号'),
    sa.Column('password_hash', sa.String(length=128), nullable=True, comment='密码'),
    sa.Column('email', sa.String(length=120), nullable=False, comment='邮箱'),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###