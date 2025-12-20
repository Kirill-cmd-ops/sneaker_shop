from sqlalchemy import ForeignKey, UniqueConstraint

from favorite_service.favorite.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .favorite import Favorite
    from .sneaker import Sneaker


class FavoriteSneakerAssociation(Base, IntIdPkMixin):
    favorite_id: Mapped[int] = mapped_column(ForeignKey("favorites.id", ondelete="CASCADE"), nullable=False, index=True)
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id", ondelete="RESTRICT"), nullable=False, index=True)
    size_id: Mapped[int] = mapped_column(ForeignKey("sizes.id", ondelete="RESTRICT"), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("favorite_id", "sneaker_id", "size_id", name="uq_favorite_sneaker_size")
    )
    favorite: Mapped["Favorite"] = relationship(
        "Favorite",
        back_populates="sneaker_associations",
    )

    sneaker: Mapped["Sneaker"] = relationship(
        "Sneaker",
        back_populates="favorite_associations",
    )
