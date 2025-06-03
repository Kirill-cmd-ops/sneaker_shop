from favorite_service.favorite.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .favorite_sneaker import FavoriteSneakerAssociation



class Favorite(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(unique=True, index=True)

    sneaker_associations: Mapped[list["FavoriteSneakerAssociation"]] = relationship(
        back_populates="favorite",
    )
