from sqlalchemy import String
from typing import TYPE_CHECKING
from .base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .sneaker import Sneaker


class Country(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        unique=True,
        index=True,
    )

    sneakers: Mapped[list["Sneaker"]] = relationship(
        "Sneaker",
        back_populates="country"
    )
