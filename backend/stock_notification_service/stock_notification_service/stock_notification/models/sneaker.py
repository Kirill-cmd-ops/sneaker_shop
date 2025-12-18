from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from stock_notification_service.stock_notification.models.base import Base

if TYPE_CHECKING:
    from .brand import Brand
    from .user import User
    from .size import Size
    from .sneaker_size import SneakerSizeAssociation
    from .user_sneaker_subscription import UserSneakerSubscription


class Sneaker(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id", ondelete="RESTRICT"), index=True)
    image_url: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    brand: Mapped["Brand"] = relationship(
        "Brand",
        back_populates="sneakers",
    )

    user_size_subscriptions: Mapped[list["UserSneakerSubscription"]] = relationship(
        "UserSneakerSubscription",
        back_populates="sneaker",
    )

    subscribed_users: Mapped[list["User"]] = relationship(
        secondary="user_sneaker_subscriptions",
        viewonly=True,
    )

    available_sizes: Mapped[list["Size"]] = relationship(
        secondary="user_sneaker_subscriptions",
        viewonly=True,
    )

    size_associations: Mapped[list["SneakerSizeAssociation"]] = relationship(
        "SneakerSizeAssociation",
        back_populates="sneaker",
    )

    available_sizes_in_stock: Mapped[list["Size"]] = relationship(
        secondary="sneaker_size_associations",
        viewonly=True,
    )
