from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.auth.models.base import Base

if TYPE_CHECKING:
    from .size import Size
    from .sneaker import Sneaker


class SneakerSizeAssociation(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id"))
    size_id: Mapped[int] = mapped_column(ForeignKey("sizes.id"))
    quantity: Mapped[int] = mapped_column(default=0)

    __table_args__ = (
        UniqueConstraint("sneaker_id", "size_id", name="uq_sneaker_size"),
    )

    sneaker: Mapped["Sneaker"] = relationship(
        back_populates="size_associations",
    )

    size: Mapped["Size"] = relationship(
        back_populates="sneaker_associations",
    )
