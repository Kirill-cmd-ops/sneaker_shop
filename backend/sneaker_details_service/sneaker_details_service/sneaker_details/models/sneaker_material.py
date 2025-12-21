from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .material import Material


class SneakerMaterialAssociation(Base, IntIdPkMixin):
    sneaker_id: Mapped[int] = mapped_column(
        ForeignKey("sneakers.id", ondelete="CASCADE"),
        nullable=False,
    )
    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id", ondelete="RESTRICT"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "sneaker_id",
            "material_id",
            name="uq_sneaker_material",
        ),
    )

    sneaker: Mapped["Sneaker"] = relationship(
        "Sneaker",
        back_populates="material_associations",
    )

    material: Mapped["Material"] = relationship(
        "Material",
        back_populates="sneaker_associations",
    )
