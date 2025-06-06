from sqlalchemy import String
from typing import TYPE_CHECKING
from catalog_service.catalog.models.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship

if TYPE_CHECKING:
    from .sneaker import Sneaker


class Country(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        unique=True,
        index=True,
    )

    sneakers: Mapped[list["Sneaker"]] = relationship(back_populates="country")
