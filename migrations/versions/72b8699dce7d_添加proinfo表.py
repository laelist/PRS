"""添加proinfo表

Revision ID: 72b8699dce7d
Revises: c80ac25d2364
Create Date: 2021-10-26 18:27:19.014467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72b8699dce7d'
down_revision = 'c80ac25d2364'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pro_information',
    sa.Column('info_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('introduction', sa.String(length=500), nullable=False),
    sa.Column('file_path', sa.String(length=200), nullable=False),
    sa.Column('pro_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pro_id'], ['project.pro_id'], ),
    sa.PrimaryKeyConstraint('info_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pro_information')
    # ### end Alembic commands ###
