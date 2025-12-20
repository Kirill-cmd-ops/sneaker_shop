from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .size import Size
    from .sneaker import Sneaker


class SneakerSizeAssociation(Base, IntIdPkMixin):
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id", ondelete="CASCADE"), index=True)
    size_id: Mapped[int] = mapped_column(ForeignKey("sizes.id", ondelete="RESTRICT"), index=True)
    quantity: Mapped[int] = mapped_column(default=0)

    __table_args__ = (
        UniqueConstraint("sneaker_id", "size_id", name="uq_sneaker_size"),
    )

    sneaker: Mapped["Sneaker"] = relationship(
        "Sneaker",
        back_populates="size_associations",
    )

    size: Mapped["Size"] = relationship(
        "Size",
        back_populates="sneaker_associations",
    )
