from sqlalchemy.ext.asyncio import AsyncSession

from microservices.cart_service.cart_service.cart.models import CartSneakerAssociation


async def add_sneaker_to_cart_service(
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
