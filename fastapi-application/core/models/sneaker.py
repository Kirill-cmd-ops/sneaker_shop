import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, CheckConstraint, Numeric, ForeignKey, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth.models.base import Base

if TYPE_CHECKING:
    from .brand import Brand
    from .size import Size
    from .sneaker_size import SneakerSizeAssociation


class GenderEnum(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    UNISEX = "unisex"

class Sneaker(Base):
    __table_args__ = (CheckConstraint("price > 0", name="check_price_positive"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(400))
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), index=True)
    image_url: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False, server_default=func.now())

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
