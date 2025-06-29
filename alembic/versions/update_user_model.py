"""Update user model

Revision ID: update_user_model
Revises: 83870bd3255c
Create Date: 2025-06-30 08:15:00.175562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'update_user_model'
down_revision = '83870bd3255c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Update users table with missing columns
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=True))
    op.add_column('users', sa.Column('full_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('users', sa.Column('github_username', sa.String(), nullable=True))
    op.add_column('users', sa.Column('github_access_token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('last_login', sa.DateTime(timezone=True), nullable=True))
    
    # Update existing name column to full_name if needed
    op.execute("UPDATE users SET full_name = name WHERE full_name IS NULL AND name IS NOT NULL")
    
    # Drop the name column
    op.drop_column('users', 'name')
    
    # Add description column to api_keys
    op.add_column('api_keys', sa.Column('description', sa.Text(), nullable=True))


def downgrade() -> None:
    # Revert changes to users table
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))
    
    # Update name column from full_name if possible
    op.execute("UPDATE users SET name = full_name WHERE name IS NULL AND full_name IS NOT NULL")
    
    op.drop_column('users', 'hashed_password')
    op.drop_column('users', 'full_name')
    op.drop_column('users', 'is_superuser')
    op.drop_column('users', 'github_username')
    op.drop_column('users', 'github_access_token')
    op.drop_column('users', 'last_login')
    
    # Drop description column from api_keys
    op.drop_column('api_keys', 'description') 