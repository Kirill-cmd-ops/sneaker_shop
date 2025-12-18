from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from stock_notification_service.stock_notification.models import Base

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .user import User
    from .size import Size


class UserSneakerSubscription(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id", ondelete="RESTRICT"))
    size_id: Mapped[int] = mapped_column(ForeignKey("sizes.id", ondelete="RESTRICT"))

    __table_args__ = (
        UniqueConstraint("sneaker_id", "user_id", "size_id", name="uq_user_sneaker_size"),
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
        back_populates="user_sneaker_notifications"
    )
