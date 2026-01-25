from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cart_service.cart.models.base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .sneaker_size import SneakerSizeAssociation


class Size(Base, IntIdPkMixin):
    eu_size: Mapped[float] = mapped_column(
        Numeric(3, 1),
        nullable=False,
        unique=True,
    )

    sneaker_associations: Mapped[list["SneakerSizeAssociation"]] = relationship(
        "SneakerSizeAssociation",
        back_populates="size",
    )

    sneakers: Mapped[list["Sneaker"]] = relationship(
        secondary="sneaker_size_associations",
        viewonly=True,
    )
