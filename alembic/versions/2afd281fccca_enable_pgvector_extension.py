"""enable_pgvector_extension

Revision ID: 2afd281fccca
Revises: 3ee2331ded36
Create Date: 2026-07-19 21:01:47.705831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2afd281fccca'
down_revision: Union[str, Sequence[str], None] = '3ee2331ded36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS vector;")
