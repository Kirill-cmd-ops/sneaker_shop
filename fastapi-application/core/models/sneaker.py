from typing import TYPE_CHECKING

from sqlalchemy import String, CheckConstraint, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth.models.base import Base

if TYPE_CHECKING:
    from .brand import Brand
    from .size import Size
    from .sneaker_size import SneakerSizeAssociation


class Sneaker(Base):
    __table_args__ = (CheckConstraint("price > 0", name="check_price_positive"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(400))
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), index=True)
    image_url: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    brand: Mapped["Brand"] = relationship(
        back_populates="sneakers",
    )

    size_associations: Mapped[list["SneakerSizeAssociation"]] = relationship(
        back_populates="sneaker",
    )

    sizes: Mapped[list["Size"]] = relationship(
        secondary="sneaker_size_associations",
        viewonly=True,
    )
