"""accounting tables

Revision ID: 0003_accounting
Revises: 0002_rbac_and_crm_indexes
Create Date: 2025-10-06
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0003_accounting'
down_revision = '0002_rbac_and_crm_indexes'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'acc_invoices',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('number', sa.String(length=50), nullable=False, unique=True),
        sa.Column('customer_name', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='draft'),
        sa.Column('issue_date', sa.Date(), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('currency', sa.String(length=10), nullable=False, server_default='USD'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('total', sa.Numeric(12,2), nullable=False, server_default='0'),
        sa.Column('tenant_id', sa.Integer(), sa.ForeignKey('tenants.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'acc_invoice_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('invoice_id', sa.Integer(), sa.ForeignKey('acc_invoices.id'), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=False),
        sa.Column('quantity', sa.Numeric(10,2), nullable=False, server_default='1'),
        sa.Column('unit_price', sa.Numeric(12,2), nullable=False, server_default='0'),
        sa.Column('line_total', sa.Numeric(12,2), nullable=False, server_default='0'),
    )
    op.create_table(
        'acc_payments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('invoice_id', sa.Integer(), sa.ForeignKey('acc_invoices.id'), nullable=False),
        sa.Column('amount', sa.Numeric(12,2), nullable=False),
        sa.Column('method', sa.String(length=50), nullable=True),
        sa.Column('paid_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_acc_invoices_status', 'acc_invoices', ['status'])
    op.create_index('ix_acc_invoices_number', 'acc_invoices', ['number'])


def downgrade() -> None:
    op.drop_index('ix_acc_invoices_number', table_name='acc_invoices')
    op.drop_index('ix_acc_invoices_status', table_name='acc_invoices')
    op.drop_table('acc_payments')
    op.drop_table('acc_invoice_items')
    op.drop_table('acc_invoices')
