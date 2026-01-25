from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from stock_notification_service.stock_notification.models.base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .brand import Brand
    from .user import User
    from .size import Size
    from .sneaker_size import SneakerSizeAssociation
    from .user_sneaker_subscription import UserSneakerSubscription
    from .user_sneaker_one_time_subscription import UserSneakerOneTimeSubscription


class Sneaker(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )
    brand_id: Mapped[int] = mapped_column(
        ForeignKey("brands.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    image_url: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        unique=True,
    )
    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )

    brand: Mapped["Brand"] = relationship(
        "Brand",
        back_populates="sneakers",
    )

    user_size_subscriptions: Mapped[list["UserSneakerSubscription"]] = relationship(
        "UserSneakerSubscription",
        back_populates="sneaker",
    )

    user_size_one_time_subscriptions: Mapped[list["UserSneakerOneTimeSubscription"]] = relationship(
        "UserSneakerOneTimeSubscription",
        back_populates="sneaker"
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
