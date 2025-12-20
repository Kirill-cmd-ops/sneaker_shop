from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .color import Color

class SneakerColorAssociation(Base, IntIdPkMixin):
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id", ondelete="CASCADE"), index=True)
    color_id: Mapped[int] = mapped_column(ForeignKey("colors.id", ondelete="RESTRICT"), index=True)

    __table_args__ = (
        UniqueConstraint("sneaker_id", "color_id", name="uq_sneaker_color"),
    )

    sneaker: Mapped["Sneaker"] = relationship(
        "Sneaker",
        back_populates="color_associations",
    )

    color: Mapped["Color"] = relationship(
        "Color",
        back_populates="sneaker_associations",
    )
