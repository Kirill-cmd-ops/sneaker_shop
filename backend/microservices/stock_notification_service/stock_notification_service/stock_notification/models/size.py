from typing import TYPE_CHECKING

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .user import User
    from .user_sneaker_subscription import UserSneakerSubscription
    from .sneaker_size import SneakerSizeAssociation
    from .user_sneaker_one_time_subscription import UserSneakerOneTimeSubscription


class Size(Base, IntIdPkMixin):
    eu_size: Mapped[float] = mapped_column(
        Numeric(3, 1),
        nullable=False,
        unique=True,
    )

    user_sneaker_notifications: Mapped[list["UserSneakerSubscription"]] = relationship(
        "UserSneakerSubscription",
        back_populates="size",
    )

    user_sneaker_one_time_notifications: Mapped[list["UserSneakerOneTimeSubscription"]] = relationship(
        "UserSneakerOneTimeSubscription",
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
