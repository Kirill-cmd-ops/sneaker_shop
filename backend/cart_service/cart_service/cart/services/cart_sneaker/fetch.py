from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import CartSneakerAssociation
from cart_service.cart.schemas import CartSneakerCreate


async def get_sneaker_in_cart_service(
    session: AsyncSession,
    cart_id: int,
    sneaker_id: int,
    size_id: int,
):
    return await session.scalar(
        select(CartSneakerAssociation).where(
            CartSneakerAssociation.cart_id == cart_id,
            CartSneakerAssociation.sneaker_id == sneaker_id,
            CartSneakerAssociation.size_id == size_id,
        )
    )
