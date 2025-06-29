"""Update API key user_id to UUID

Revision ID: update_api_key_user_id
Revises: make_updated_at_nullable
Create Date: 2025-06-30 10:00:00.175562

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'update_api_key_user_id'
down_revision = 'make_updated_at_nullable'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Temporarily drop the foreign key constraint
    op.drop_constraint('api_keys_user_id_fkey', 'api_keys', type_='foreignkey')
    
    # Alter the column type
    op.alter_column('api_keys', 'user_id', 
                    existing_type=sa.String(),
                    type_=UUID(as_uuid=False),
                    postgresql_using='user_id::uuid')
    
    # Re-add the foreign key constraint
    op.create_foreign_key('api_keys_user_id_fkey', 'api_keys', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    # Temporarily drop the foreign key constraint
    op.drop_constraint('api_keys_user_id_fkey', 'api_keys', type_='foreignkey')
    
    # Alter the column type back to String
    op.alter_column('api_keys', 'user_id', 
                    existing_type=UUID(as_uuid=False),
                    type_=sa.String(),
                    postgresql_using='user_id::text')
    
    # Re-add the foreign key constraint
    op.create_foreign_key('api_keys_user_id_fkey', 'api_keys', 'users', ['user_id'], ['id']) 