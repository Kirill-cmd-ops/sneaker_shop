from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth.models.base import Base

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .sneaker_size import SneakerSizeAssociation


class Size(Base):
    __table_args__ = (
        CheckConstraint("eu_size BETWEEN 15 AND 50", name="check_eu_size_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    eu_size: Mapped[float] = mapped_column(
        Numeric(3, 1),
        nullable=False,
        unique=True,
    )

    sneaker_associations: Mapped[list["SneakerSizeAssociation"]] = relationship(
        back_populates="size",
        overlaps="sneakers",
    )
    sneakers: Mapped[list["Sneaker"]] = relationship(
        secondary="sneaker_size_association",
        back_populates="sizes",
        overlaps="sneaker_associations",
    )
