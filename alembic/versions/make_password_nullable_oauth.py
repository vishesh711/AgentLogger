"""Make password nullable for OAuth users

Revision ID: make_password_nullable_oauth
Revises: make_updated_at_nullable
Create Date: 2024-01-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'make_password_nullable_oauth'
down_revision = 'make_updated_at_nullable'
branch_labels = None
depends_on = None


def upgrade():
    # Make hashed_password nullable for OAuth users
    op.alter_column('users', 'hashed_password',
                    existing_type=sa.String(),
                    nullable=True)


def downgrade():
    # Make hashed_password not nullable (original state)
    op.alter_column('users', 'hashed_password',
                    existing_type=sa.String(),
                    nullable=False) 