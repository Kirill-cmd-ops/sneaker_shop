from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from catalog_service.catalog.models.base import Base

if TYPE_CHECKING:
    from backend.catalog_service.catalog_service.catalog.models.sneaker import Sneaker
    from backend.core.models.color import Color

class SneakerColorAssociation(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id"))
    color_id: Mapped[int] = mapped_column(ForeignKey("colors.id"))

    __table_args__ = (
        UniqueConstraint("sneaker_id", "color_id", name="uq_sneaker_color"),
    )

    sneaker: Mapped["Sneaker"] = relationship(
        back_populates="color_associations",
    )

    color: Mapped["Color"] = relationship(
        back_populates="sneaker_associations",
    )
