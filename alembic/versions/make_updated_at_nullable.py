"""Make updated_at nullable

Revision ID: make_updated_at_nullable
Revises: update_user_model
Create Date: 2025-06-30 09:30:00.175562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'make_updated_at_nullable'
down_revision = 'update_user_model'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Make updated_at nullable in all tables
    op.alter_column('users', 'updated_at', nullable=True)
    op.alter_column('api_keys', 'updated_at', nullable=True)
    op.alter_column('analysis_requests', 'updated_at', nullable=True)
    op.alter_column('fix_requests', 'updated_at', nullable=True)
    op.alter_column('github_prs', 'updated_at', nullable=True)


def downgrade() -> None:
    # Make updated_at non-nullable again
    op.alter_column('users', 'updated_at', nullable=False)
    op.alter_column('api_keys', 'updated_at', nullable=False)
    op.alter_column('analysis_requests', 'updated_at', nullable=False)
    op.alter_column('fix_requests', 'updated_at', nullable=False)
    op.alter_column('github_prs', 'updated_at', nullable=False) 