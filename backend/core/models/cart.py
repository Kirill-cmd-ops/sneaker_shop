from sqlalchemy import ForeignKey
from backend.auth.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.auth.models import User
    from .cart_sneaker import CartSneakerAssociation
    from .sneaker import Sneaker



class Cart(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)

    user: Mapped["User"] = relationship(
        back_populates="cart",
    )

    sneaker_associations: Mapped[list["CartSneakerAssociation"]] = relationship(
        back_populates="cart",
    )

    sneakers: Mapped[list["Sneaker"]] = relationship(
        secondary="cart_sneaker_associations",
        viewonly=True,
    )