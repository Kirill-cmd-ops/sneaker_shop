from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from stock_notification_service.stock_notification.models import Base

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .user import User


class UserSneakerSubscription(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id"))

    __table_args__ = (
        UniqueConstraint("sneaker_id", "user_id", name="uq_user_sneaker"),
    )

    sneaker: Mapped["Sneaker"] = relationship(
        "Sneaker",
        back_populates="user_associations",
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="sneaker_associations",
    )
