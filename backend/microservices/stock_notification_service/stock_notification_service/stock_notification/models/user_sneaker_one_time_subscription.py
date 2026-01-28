from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint, Enum as PgEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from microservices.stock_notification_service.stock_notification_service.stock_notification.models import Base
from .mixins import IntIdPkMixin
from microservices.stock_notification_service.stock_notification_service.stock_notification.enums import \
    SubscriptionStatus

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .user import User
    from .size import Size


class UserSneakerOneTimeSubscription(Base, IntIdPkMixin):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    sneaker_id: Mapped[int] = mapped_column(
        ForeignKey("sneakers.id", ondelete="RESTRICT"),
        nullable=False,
    )
    size_id: Mapped[int] = mapped_column(
        ForeignKey("sizes.id", ondelete="RESTRICT"),
        nullable=False,
    )
    is_sent: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )
    status: Mapped[SubscriptionStatus] = mapped_column(
        PgEnum(SubscriptionStatus),
        nullable=False,
        default=SubscriptionStatus.ACTIVE,
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "sneaker_id",
            "size_id",
            name="uq_user_sneaker_size",
        ),
    )

    sneaker: Mapped["Sneaker"] = relationship(
        "Sneaker",
        back_populates="user_size_one_time_subscriptions",
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="sneaker_size_one_time_subscriptions",
    )

    size: Mapped["Size"] = relationship(
        "Size",
        back_populates="user_sneaker_one_time_notifications",
    )
