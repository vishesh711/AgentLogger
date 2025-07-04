"""merge heads after fixing uuid types

Revision ID: f6811421a598
Revises: make_password_nullable_oauth, fix_api_key_user_id_fkey
Create Date: 2025-07-04 01:15:48.563744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6811421a598'
down_revision = ('make_password_nullable_oauth', 'fix_api_key_user_id_fkey')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass 