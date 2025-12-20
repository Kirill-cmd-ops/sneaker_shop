from cart_service.cart.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .cart_sneaker import CartSneakerAssociation
    from .sneaker import Sneaker


class Cart(Base, IntIdPkMixin):
    user_id: Mapped[int] = mapped_column(nullable=False, unique=True)

    sneaker_associations: Mapped[list["CartSneakerAssociation"]] = relationship(
        "CartSneakerAssociation",
        back_populates="cart",
    )

    sneakers: Mapped[list["Sneaker"]] = relationship(
        secondary="cart_sneaker_associations",
        viewonly=True,
    )
