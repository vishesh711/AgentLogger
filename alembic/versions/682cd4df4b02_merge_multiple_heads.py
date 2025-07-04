"""merge multiple heads

Revision ID: 682cd4df4b02
Revises: make_password_nullable_oauth, fix_api_key_user_id_fkey
Create Date: 2025-07-04 01:08:45.832464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '682cd4df4b02'
down_revision = ('make_password_nullable_oauth', 'fix_api_key_user_id_fkey')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass 