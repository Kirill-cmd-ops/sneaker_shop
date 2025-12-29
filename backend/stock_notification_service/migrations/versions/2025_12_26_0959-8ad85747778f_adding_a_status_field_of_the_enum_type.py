"""Adding a status field of the Enum type

Revision ID: 8ad85747778f
Revises: 263a4db61f4a
Create Date: 2025-12-26 09:59:08.434827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8ad85747778f'
down_revision: Union[str, None] = '263a4db61f4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'subscriptionstatus') THEN
                CREATE TYPE subscriptionstatus AS ENUM (
                    'ACTIVE',
                    'INACTIVE_BY_USER', 
                    'INACTIVE_BY_SYSTEM'
                );
            END IF;
        END $$;
    """)

    op.add_column('user_sneaker_subscriptions',
        sa.Column('status',
            postgresql.ENUM('ACTIVE', 'INACTIVE_BY_USER', 'INACTIVE_BY_SYSTEM',
                          name='subscriptionstatus', create_type=False),
            nullable=True
        )
    )

    op.execute("""
        UPDATE user_sneaker_subscriptions 
        SET status = 'ACTIVE'::subscriptionstatus
        WHERE status IS NULL
    """)

    op.alter_column('user_sneaker_subscriptions', 'status',
        nullable=False,
        server_default='ACTIVE'
    )


def downgrade() -> None:
    op.drop_column('user_sneaker_subscriptions', 'status')

    op.execute("DROP TYPE subscriptionstatus")