from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, CheckConstraint, Numeric, ForeignKey, func, nullsfirst
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .country import Country
    from .brand import Brand
    from .size import Size
    from .color import Color
    from .material import Material
    from .sneaker_size import SneakerSizeAssociation
    from .sneaker_color import SneakerColorAssociation
    from .sneaker_material import SneakerMaterialAssociation


class Sneaker(Base, IntIdPkMixin):
    __table_args__ = (CheckConstraint("price > 0", name="check_price_positive"),)

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(400), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id", ondelete="RESTRICT"), nullable=False, index=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="RESTRICT"), nullable=False, index=True)
    image_url: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False, server_default=func.now()
    )
    gender: Mapped[str] = mapped_column(String(10), nullable=False, default="унисекс")

    country: Mapped["Country"] = relationship(
        "Country",
        back_populates="sneakers",
    )

    brand: Mapped["Brand"] = relationship(
        "Brand",
        back_populates="sneakers",
    )

    size_associations: Mapped[list["SneakerSizeAssociation"]] = relationship(
        "SneakerSizeAssociation",
        back_populates="sneaker",
    )

    color_associations: Mapped[list["SneakerColorAssociation"]] = relationship(
        "SneakerColorAssociation",
        back_populates="sneaker",
    )

    material_associations: Mapped[list["SneakerMaterialAssociation"]] = relationship(
        "SneakerMaterialAssociation",
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
