"""Creating the user_sneaker_one_time_subscriptions table

Revision ID: 58bcd63a9077
Revises: 10729e6b24d3
Create Date: 2025-12-28 21:20:36.785336

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "58bcd63a9077"
down_revision: Union[str, None] = "10729e6b24d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
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

    op.create_table(
        "user_sneaker_one_time_subscriptions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("sneaker_id", sa.Integer(), nullable=False),
        sa.Column("size_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(
                "ACTIVE",
                "INACTIVE_BY_USER",
                "INACTIVE_BY_SYSTEM",
                name="subscriptionstatus",
                create_type=False
            ),
            server_default="ACTIVE",
            nullable=False,
        ),
        sa.Column("is_sent", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.ForeignKeyConstraint(
            ["size_id"],
            ["sizes.id"],
            name=op.f("fk_user_sneaker_one_time_subscriptions_size_id_sizes"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["sneaker_id"],
            ["sneakers.id"],
            name=op.f(
                "fk_user_sneaker_one_time_subscriptions_sneaker_id_sneakers"
            ),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_sneaker_one_time_subscriptions_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_user_sneaker_one_time_subscriptions")
        ),
        sa.UniqueConstraint(
            "user_id", "sneaker_id", "size_id",
            name="uq_user_sneaker_one_time_subscription"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user_sneaker_one_time_subscriptions")
    # ### end Alembic commands ###