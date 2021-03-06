"""v0.4

Revision ID: 2401771d6b4e
Revises: 
Create Date: 2021-10-26 18:24:33.641505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2401771d6b4e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pro_class',
    sa.Column('class_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('class_name', sa.String(length=30), nullable=False),
    sa.Column('pro_class_name', sa.String(length=30), nullable=False),
    sa.Column('over_time', sa.DateTime(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('exist_time', sa.DateTime(), nullable=False),
    sa.Column('department', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('class_id'),
    sa.UniqueConstraint('pro_class_name')
    )
    op.create_table('user_t',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('status', sa.String(length=1), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_user_t_username'), 'user_t', ['username'], unique=True)
    op.create_table('applicant',
    sa.Column('app_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('app_name', sa.String(length=20), nullable=False),
    sa.Column('phone_number', sa.String(length=11), nullable=False),
    sa.Column('professional', sa.String(length=20), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_t.user_id'], ),
    sa.PrimaryKeyConstraint('app_id')
    )
    op.create_index(op.f('ix_applicant_app_name'), 'applicant', ['app_name'], unique=False)
    op.create_table('expert',
    sa.Column('expert_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('expert_name', sa.String(length=20), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_t.user_id'], ),
    sa.PrimaryKeyConstraint('expert_id')
    )
    op.create_index(op.f('ix_expert_expert_name'), 'expert', ['expert_name'], unique=False)
    op.create_table('organization',
    sa.Column('org_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('org_name', sa.String(length=30), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_t.user_id'], ),
    sa.PrimaryKeyConstraint('org_id')
    )
    op.create_index(op.f('ix_organization_org_name'), 'organization', ['org_name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_organization_org_name'), table_name='organization')
    op.drop_table('organization')
    op.drop_index(op.f('ix_expert_expert_name'), table_name='expert')
    op.drop_table('expert')
    op.drop_index(op.f('ix_applicant_app_name'), table_name='applicant')
    op.drop_table('applicant')
    op.drop_index(op.f('ix_user_t_username'), table_name='user_t')
    op.drop_table('user_t')
    op.drop_table('pro_class')
    # ### end Alembic commands ###
