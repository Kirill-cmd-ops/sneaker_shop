from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import CartSneakerAssociation
from cart_service.cart.schemas import CartSneakerCreate


async def check_sneaker_in_cart_exists(
    session: AsyncSession,
    cart_id: int,
    item_create: CartSneakerCreate,
):
    stmt = select(CartSneakerAssociation).where(
        CartSneakerAssociation.cart_id == cart_id,
        CartSneakerAssociation.sneaker_id == item_create.sneaker_id,
        CartSneakerAssociation.size_id == item_create.size_id,
    )
    result = await session.execute(stmt)
    sneaker_record = result.scalar_one_or_none()
    return sneaker_record
