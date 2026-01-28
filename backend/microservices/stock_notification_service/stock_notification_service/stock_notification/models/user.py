from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from microservices.stock_notification_service.stock_notification_service.stock_notification.models.base import Base
from microservices.stock_notification_service.stock_notification_service.stock_notification.models.mixins import \
    IntIdPkMixin

if TYPE_CHECKING:
    from .user_sneaker_subscription import UserSneakerSubscription
    from .user_sneaker_one_time_subscription import UserSneakerOneTimeSubscription
    from .sneaker import Sneaker
    from .size import Size


class User(Base, IntIdPkMixin):
    email: Mapped[str] = mapped_column(
        String(length=320),
        nullable=False,
        unique=True,
    )
    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )
    is_verified: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    sneaker_size_subscriptions: Mapped[list["UserSneakerSubscription"]] = relationship(
        "UserSneakerSubscription",
        back_populates="user",
    )

    sneaker_size_one_time_subscriptions: Mapped[list["UserSneakerOneTimeSubscription"]] = relationship(
        "UserSneakerOneTimeSubscription",
        back_populates="user"
    )

    available_sneakers: Mapped[list["Sneaker"]] = relationship(
        secondary="user_sneaker_subscriptions",
        viewonly=True,
    )

    available_sizes: Mapped[list["Size"]] = relationship(
        secondary="user_sneaker_subscriptions",
        viewonly=True,
    )
