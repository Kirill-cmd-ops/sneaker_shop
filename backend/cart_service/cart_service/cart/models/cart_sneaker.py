from sqlalchemy import ForeignKey

from cart_service.cart.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cart import Cart

class CartSneakerAssociation(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    quantity: Mapped[int] = mapped_column(default=1)
    sneaker_id: Mapped[int]
    sneaker_size: Mapped[float]

    cart: Mapped["Cart"] = relationship(
        "Cart",
        back_populates="sneaker_associations",
    )
