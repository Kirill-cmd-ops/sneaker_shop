from favorite_service.favorite.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .favorite_sneaker import FavoriteSneakerAssociation
    from .sneaker import Sneaker


class Favorite(Base, IntIdPkMixin):
    user_id: Mapped[int] = mapped_column(unique=True, index=True)

    sneaker_associations: Mapped[list["FavoriteSneakerAssociation"]] = relationship(
        "FavoriteSneakerAssociation",
        back_populates="favorite",
    )

    sneakers: Mapped[list["Sneaker"]] = relationship(
        secondary="favorite_sneaker_associations",
        viewonly=True,
    )
