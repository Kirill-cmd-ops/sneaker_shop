from sqlalchemy import String
from typing import TYPE_CHECKING
from .base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .sneaker_color import SneakerColorAssociation


class Color(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
        index=True,
    )
    sneaker_associations: Mapped[list["SneakerColorAssociation"]] = relationship(
        back_populates="color",
    )

    sneakers: Mapped[list["Sneaker"]] = relationship(
        secondary="sneaker_color_associations",
        viewonly=True,
    )
