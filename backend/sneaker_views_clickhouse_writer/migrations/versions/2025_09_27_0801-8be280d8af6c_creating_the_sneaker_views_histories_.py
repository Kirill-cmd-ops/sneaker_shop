"""creating the sneaker_views_histories table

Revision ID: 8be280d8af6c
Revises:
Create Date: 2025-09-27 08:01:31.437561

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8be280d8af6c"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create sneaker_views_histories table with ReplacingMergeTree engine"""
    op.execute("""
        CREATE TABLE IF NOT EXISTS sneaker_views_histories
        (
            id UInt64,
            user_id UInt32,
            sneaker_id UInt32,
            view_timestamp DateTime
        )
        ENGINE = ReplacingMergeTree(view_timestamp)
        ORDER BY (user_id, sneaker_id)
    """)


def downgrade() -> None:
    """Drop sneaker_views_histories table"""
    op.execute("DROP TABLE IF EXISTS sneaker_views_histories")

