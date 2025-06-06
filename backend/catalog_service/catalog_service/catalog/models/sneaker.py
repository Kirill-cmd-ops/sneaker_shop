from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, CheckConstraint, Numeric, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from catalog_service.catalog.models.base import Base

if TYPE_CHECKING:
    from .country import Country
    from .brand import Brand
    from .size import Size
    from .color import Color
    from .material import Material
    from .sneaker_size import SneakerSizeAssociation
    from .sneaker_color import SneakerColorAssociation
    from .sneaker_material import SneakerMaterialAssociation
    from backend.cart_service.cart_service.cart.models.cart_sneaker import CartSneakerAssociation
    from backend.cart_service.cart_service.cart.models.cart import Cart
    from favorite_service.favorite.models.favorite import Favorite
    from favorite_service.favorite.models.favorite_sneaker import FavoriteSneakerAssociation


class Sneaker(Base):
    __table_args__ = (CheckConstraint("price > 0", name="check_price_positive"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(400))
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), index=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), index=True)
    image_url: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False, server_default=func.now()
    )
    gender: Mapped[str] = mapped_column(String(10), default="Унисекс")

    country: Mapped["Country"] = relationship(
        back_populates="sneakers",
    )

    brand: Mapped["Brand"] = relationship(
        back_populates="sneakers",
    )

    size_associations: Mapped[list["SneakerSizeAssociation"]] = relationship(
        back_populates="sneaker",
    )

    color_associations: Mapped[list["SneakerColorAssociation"]] = relationship(
        back_populates="sneaker",
    )

    material_associations: Mapped[list["SneakerMaterialAssociation"]] = relationship(
        back_populates="sneaker",
    )

    cart_associations: Mapped[list["CartSneakerAssociation"]] = relationship(
        back_populates="sneaker",
    )

    favorite_associations: Mapped[list["FavoriteSneakerAssociation"]] = relationship(
        back_populates="sneaker",
    )

    sizes: Mapped[list["Size"]] = relationship(
        secondary="sneaker_size_associations",
        viewonly=True,
    )

    colors: Mapped[list["Color"]] = relationship(
        secondary="sneaker_color_associations",
        viewonly=True,
    )

    materials: Mapped[list["Material"]] = relationship(
        secondary="sneaker_material_associations",
        viewonly=True,
    )

    carts: Mapped[list["Cart"]] = relationship(
        secondary="cart_sneaker_associations",
        viewonly=True,
    )

    favorites: Mapped[list["Favorite"]] = relationship(
        secondary="favorite_sneaker_associations",
        viewonly=True,
    )
