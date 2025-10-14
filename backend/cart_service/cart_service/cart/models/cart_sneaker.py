from sqlalchemy import ForeignKey

from cart_service.cart.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cart import Cart
    from .sneaker import Sneaker

class CartSneakerAssociation(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    quantity: Mapped[int] = mapped_column(default=1)
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id"))
    size_id: Mapped[float] = mapped_column(ForeignKey("sizes.id"))

    cart: Mapped["Cart"] = relationship(
        "Cart",
        back_populates="sneaker_associations",
    )

    sneaker: Mapped["Sneaker"] = relationship(
        "Sneaker",
        back_populates="cart_associations"
    )
