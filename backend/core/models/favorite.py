from sqlalchemy import ForeignKey
from backend.auth_servicee import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.auth_servicee import User
    from .favorite_sneaker import FavoriteSneakerAssociation
    from .sneaker import Sneaker



class Favorite(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)

    user: Mapped["User"] = relationship(
        back_populates="favorite",
    )

    sneaker_associations: Mapped[list["FavoriteSneakerAssociation"]] = relationship(
        back_populates="favorite",
    )

    sneakers: Mapped[list["Sneaker"]] = relationship(
        secondary="favorite_sneaker_associations",
        viewonly=True,
    )