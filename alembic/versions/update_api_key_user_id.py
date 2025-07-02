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
    # Drop the existing foreign key constraint
    op.drop_constraint('api_keys_user_id_fkey', 'api_keys', type_='foreignkey')
    
    # Change the user_id column type from UUID to String
    op.alter_column('api_keys', 'user_id',
                   existing_type=postgresql.UUID(),
                   type_=sa.String(),
                   existing_nullable=False)
    
    # Recreate the foreign key constraint
    op.create_foreign_key('api_keys_user_id_fkey', 'api_keys', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    # Drop the foreign key constraint
    op.drop_constraint('api_keys_user_id_fkey', 'api_keys', type_='foreignkey')
    
    # Change the user_id column type back from String to UUID
    op.alter_column('api_keys', 'user_id',
                   existing_type=sa.String(),
                   type_=postgresql.UUID(),
                   existing_nullable=False)
    
    # Recreate the foreign key constraint
    op.create_foreign_key('api_keys_user_id_fkey', 'api_keys', 'users', ['user_id'], ['id']) 