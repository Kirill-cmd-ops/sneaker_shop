from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from stock_notification_service.stock_notification.models.base import Base
from stock_notification_service.stock_notification.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .user_sneaker_subscription import UserSneakerSubscription
    from .sneaker import Sneaker
    from .size import Size


class User(Base, IntIdPkMixin):
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    sneaker_size_subscriptions: Mapped[list["UserSneakerSubscription"]] = relationship(
        "UserSneakerSubscription",
        back_populates="user",
    )

    available_sneakers: Mapped[list["Sneaker"]] = relationship(
        secondary="user_sneaker_subscriptions",
        viewonly=True,
    )

    available_sizes: Mapped[list["Size"]] = relationship(
        secondary="user_sneaker_subscriptions",
        viewonly=True,
    )
