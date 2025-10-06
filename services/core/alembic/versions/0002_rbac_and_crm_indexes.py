"""rbac and crm indexes

Revision ID: 0002_rbac_and_crm_indexes
Revises: 0001_init
Create Date: 2025-10-06
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_rbac_and_crm_indexes'
down_revision = '0001_init'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # RBAC tables
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True),
        sa.Column('description', sa.String(length=255), nullable=True),
    )
    op.create_table(
        'permissions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('code', sa.String(length=150), nullable=False, unique=True),
        sa.Column('description', sa.String(length=255), nullable=True),
    )
    op.create_table(
        'user_roles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id'), nullable=False),
        sa.UniqueConstraint('user_id','role_id', name='uq_user_role'),
    )
    op.create_table(
        'role_permissions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id'), nullable=False),
        sa.Column('permission_id', sa.Integer(), sa.ForeignKey('permissions.id'), nullable=False),
        sa.UniqueConstraint('role_id','permission_id', name='uq_role_perm'),
    )
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('actor_user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('action', sa.String(length=150), nullable=False),
        sa.Column('entity', sa.String(length=150), nullable=True),
        sa.Column('entity_id', sa.String(length=100), nullable=True),
        sa.Column('meta', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # CRM helpful indexes
    op.create_index('ix_crm_leads_status', 'crm_leads', ['status'])
    op.create_index('ix_crm_leads_email', 'crm_leads', ['email'])


def downgrade() -> None:
    op.drop_index('ix_crm_leads_email', table_name='crm_leads')
    op.drop_index('ix_crm_leads_status', table_name='crm_leads')
    op.drop_table('audit_logs')
    op.drop_table('role_permissions')
    op.drop_table('user_roles')
    op.drop_table('permissions')
    op.drop_table('roles')
