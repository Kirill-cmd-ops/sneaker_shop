from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, CheckConstraint, Numeric, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from favorite_service.favorite.models.base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .brand import Brand
    from .size import Size
    from .sneaker_size import SneakerSizeAssociation
    from .favorite import Favorite
    from .favorite_sneaker import FavoriteSneakerAssociation


class Sneaker(Base, IntIdPkMixin):
    __table_args__ = (CheckConstraint("price > 0", name="check_price_positive"),)

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id", ondelete="RESTRICT"), nullable=False, index=True)
    image_url: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False, server_default=func.now()
    )
    gender: Mapped[str] = mapped_column(String(10), nullable=False, default="унисекс")

    brand: Mapped["Brand"] = relationship(
        "Brand",
        back_populates="sneakers",
    )

    size_associations: Mapped[list["SneakerSizeAssociation"]] = relationship(
        "SneakerSizeAssociation",
        back_populates="sneaker",
    )

    sizes: Mapped[list["Size"]] = relationship(
        secondary="sneaker_size_associations",
        viewonly=True,
    )

    favorite_associations: Mapped[list["FavoriteSneakerAssociation"]] = relationship(
        "FavoriteSneakerAssociation",
        back_populates="sneaker",
    )

    favorites: Mapped[list["Favorite"]] = relationship(
        secondary="favorite_sneaker_associations",
        viewonly=True,
    )

