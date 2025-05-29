from sqlalchemy import ForeignKey

from backend.auth_servicee import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .favorite import Favorite

class FavoriteSneakerAssociation(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    favorite_id: Mapped[int] = mapped_column(ForeignKey("favorites.id"))
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id"))

    sneaker: Mapped["Sneaker"] = relationship(
        back_populates="favorite_associations",
    )

    favorite: Mapped["Favorite"] = relationship(
        back_populates="sneaker_associations",
    )
