"""Add deal_fee column to deals table"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '20250422_add_deal_fee_column'
down_revision = None  # Change this to the previous revision ID if you have one
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('deals', sa.Column('deal_fee', sa.Numeric(10, 2), nullable=True))

def downgrade():
    op.drop_column('deals', 'deal_fee')
