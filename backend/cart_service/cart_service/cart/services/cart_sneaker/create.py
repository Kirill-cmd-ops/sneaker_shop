from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import CartSneakerAssociation


async def create_sneaker_to_cart(
    session: AsyncSession,
    cart_id: int,
    sneaker_id: int,
    size_id: int,
):
    new_sneaker = CartSneakerAssociation(
        cart_id=cart_id,
        sneaker_id=sneaker_id,
        size_id=size_id,
    )
    session.add(new_sneaker)
    return new_sneaker