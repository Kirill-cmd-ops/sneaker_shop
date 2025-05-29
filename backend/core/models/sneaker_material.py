from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth_service.auth.models.base import Base

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .material import Material


class SneakerMaterialAssociation(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id"))
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"))

    __table_args__ = (
        UniqueConstraint("sneaker_id", "material_id", name="uq_sneaker_material"),
    )

    sneaker: Mapped["Sneaker"] = relationship(
        back_populates="material_associations",
    )

    material: Mapped["Material"] = relationship(
        back_populates="sneaker_associations",
    )
