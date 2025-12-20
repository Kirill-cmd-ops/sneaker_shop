from sqlalchemy import ForeignKey, UniqueConstraint

from cart_service.cart.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .cart import Cart
    from .sneaker import Sneaker

class CartSneakerAssociation(Base, IntIdPkMixin):
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id", ondelete="RESTRICT"), nullable=False, index=True)
    size_id: Mapped[int] = mapped_column(ForeignKey("sizes.id", ondelete="RESTRICT"), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("cart_id", "sneaker_id", "ç", name="uq_cart_sneaker_size")
    )
    cart: Mapped["Cart"] = relationship(
        "Cart",
        back_populates="sneaker_associations",
    )

    sneaker: Mapped["Sneaker"] = relationship(
        "Sneaker",
        back_populates="cart_associations"
    )
