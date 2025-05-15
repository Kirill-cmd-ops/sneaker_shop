from sqlalchemy import String
from typing import TYPE_CHECKING
from backend.auth.models import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .sneaker_material import SneakerMaterialAssociation


class Material(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        unique=True,
        index=True,
    )
    sneaker_associations: Mapped[list["SneakerMaterialAssociation"]] = relationship(
        back_populates="material",
    )

    sneakers: Mapped[list["Sneaker"]] = relationship(
        secondary="sneaker_material_associations",
        viewonly=True,
    )
