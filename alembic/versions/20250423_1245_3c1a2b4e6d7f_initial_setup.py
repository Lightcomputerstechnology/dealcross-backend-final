"""Initial Alembic migration for Dealcross platform. Creates core tables: users, wallets, deals, kyc, disputes, fraud alerts, audit logs."""

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'down_revision = None'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('role', sa.String, nullable=False, default='user'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    # Wallets table
    op.create_table(
        'wallets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('balance', sa.Float, default=0.0),
        sa.Column('currency', sa.String, default='USD'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    # Deals table
    op.create_table(
        'deals',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('buyer_id', sa.Integer, sa.ForeignKey('users.id', ondelete='SET NULL')),
        sa.Column('seller_id', sa.Integer, sa.ForeignKey('users.id', ondelete='SET NULL')),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('status', sa.String, default='pending'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    # KYC table
    op.create_table(
        'kyc',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('document_type', sa.String, nullable=False),
        sa.Column('document_url', sa.String, nullable=False),
        sa.Column('status', sa.String, default='pending'),
        sa.Column('submitted_at', sa.DateTime, server_default=sa.func.now()),
    )

    # Disputes table
    op.create_table(
        'disputes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('deal_id', sa.Integer, sa.ForeignKey('deals.id', ondelete='CASCADE')),
        sa.Column('reason', sa.String, nullable=False),
        sa.Column('submitted_by', sa.Integer, sa.ForeignKey('users.id', ondelete='SET NULL')),
        sa.Column('status', sa.String, default='open'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    # Fraud Alerts table
    op.create_table(
        'fraud_alerts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('deal_id', sa.Integer, sa.ForeignKey('deals.id', ondelete='CASCADE')),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    # Audit Logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('action', sa.String, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='SET NULL')),
        sa.Column('timestamp', sa.DateTime, server_default=sa.func.now()),
    )

def downgrade():
    op.drop_table('audit_logs')
    op.drop_table('fraud_alerts')
    op.drop_table('disputes')
    op.drop_table('kyc')
    op.drop_table('deals')
    op.drop_table('wallets')
    op.drop_table('users')
