from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .user import User
    from .user_sneaker_subscription import UserSneakerSubscription
    from .sneaker_size import SneakerSizeAssociation


class Size(Base):
    __table_args__ = (
        CheckConstraint("eu_size BETWEEN 15 AND 50", name="check_eu_size_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    eu_size: Mapped[float] = mapped_column(
        Numeric(3, 1),
        nullable=False,
        unique=True,
    )

    user_sneaker_notifications: Mapped[list["UserSneakerSubscription"]] = relationship(
        "UserSneakerSubscription",
        back_populates="size",
    )

    available_sneakers: Mapped[list["Sneaker"]] = relationship(
        secondary="user_sneaker_subscriptions",
        viewonly=True,
    )

    subscribed_users: Mapped[list["User"]] = relationship(
        secondary="user_sneaker_subscriptions",
        viewonly=True,
    )

    sneaker_associations: Mapped[list["SneakerSizeAssociation"]] = relationship(
        "SneakerSizeAssociation",
        back_populates="size",
    )

    available_sneakers_in_stock: Mapped[list["Sneaker"]] = relationship(
        secondary="sneaker_size_associations",
        viewonly=True,
    )
