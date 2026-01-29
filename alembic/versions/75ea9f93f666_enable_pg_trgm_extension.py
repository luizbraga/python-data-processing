"""enable_pg_trgm_extension

Revision ID: 75ea9f93f666
Revises: 0a4ad49c18bd
Create Date: 2026-01-29 01:27:46.140335

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "75ea9f93f666"
down_revision: Union[str, None] = "0a4ad49c18bd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS pg_trgm")
