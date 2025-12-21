from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from stock_notification_service.stock_notification.models import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .user import User
    from .size import Size


class UserSneakerSubscription(Base, IntIdPkMixin):
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
        back_populates="user_size_subscriptions",
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="sneaker_size_subscriptions",
    )

    size: Mapped["Size"] = relationship(
        "Size",
        back_populates="user_sneaker_notifications",
    )
