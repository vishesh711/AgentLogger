"""Fix api_keys user_id foreign key constraint

Revision ID: fix_api_key_user_id_fkey
Revises: update_user_model
Create Date: 2025-01-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fix_api_key_user_id_fkey'
down_revision = 'update_user_model'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # This migration is no longer needed since both columns are now String
    # The foreign key constraint should already work correctly
    pass


def downgrade() -> None:
    # This migration is no longer needed since both columns are now String
    pass 