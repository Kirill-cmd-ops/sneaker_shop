from sqlalchemy import ForeignKey

from backend.auth_servicee import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sneaker import Sneaker
    from .cart import Cart

class CartSneakerAssociation(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id"))
    sneaker_size: Mapped[float]

    sneaker: Mapped["Sneaker"] = relationship(
        back_populates="cart_associations",
    )

    cart: Mapped["Cart"] = relationship(
        back_populates="sneaker_associations",
    )
