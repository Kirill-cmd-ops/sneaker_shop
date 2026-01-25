from sqlalchemy import String
from typing import TYPE_CHECKING
from .base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .sneaker_material import SneakerMaterialAssociation


class Material(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        unique=True,
    )
    sneaker_associations: Mapped[list["SneakerMaterialAssociation"]] = relationship(
        "SneakerMaterialAssociation",
        back_populates="material",
    )

    sneakers: Mapped[list["Sneaker"]] = relationship(
        secondary="sneaker_material_associations",
        viewonly=True,
    )
