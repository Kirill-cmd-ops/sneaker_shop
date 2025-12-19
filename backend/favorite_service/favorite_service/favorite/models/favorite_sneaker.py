from sqlalchemy import ForeignKey

from favorite_service.favorite.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .favorite import Favorite
    from .sneaker import Sneaker


class FavoriteSneakerAssociation(Base, IntIdPkMixin):
    favorite_id: Mapped[int] = mapped_column(ForeignKey("favorites.id", ondelete="CASCADE"))
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id", ondelete="RESTRICT"))
    size_id: Mapped[int] = mapped_column(ForeignKey("sizes.id", ondelete="RESTRICT"))

    favorite: Mapped["Favorite"] = relationship(
        "Favorite",
        back_populates="sneaker_associations",
    )

    sneaker: Mapped["Sneaker"] = relationship(
        "Sneaker",
        back_populates="favorite_associations",
    )
