from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from favorite_service.favorite.models.base import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .sneaker import Sneaker


class Brand(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    image_url: Mapped[str] = mapped_column(String(200), nullable=False)

    sneakers: Mapped[list["Sneaker"]] = relationship(
        "Sneaker",
        back_populates="brand"
    )
