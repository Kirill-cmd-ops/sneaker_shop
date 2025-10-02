"""creating the sneaker views histories

Revision ID: d66a9a2fc136
Revises: 
Create Date: 2025-10-01 08:24:20.707790

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d66a9a2fc136"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE TABLE sneaker_views_histories (
            user_id UInt32,
            sneaker_id UInt32,
            view_timestamp DateTime DEFAULT now(),
            sign Int8 DEFAULT 1,
            version UInt64 DEFAULT 1
        )
        ENGINE = VersionedCollapsingMergeTree(sign, version)
        ORDER BY (user_id, sneaker_id)
        PRIMARY KEY (user_id, sneaker_id)
    """)

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE sneaker_views_histories")
