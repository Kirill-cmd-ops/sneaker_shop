from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import Sneaker, SneakerSizeAssociation
from cart_service.cart.schemas import CartSneakerCreate


async def check_sneaker_size_exists(
    session: AsyncSession,
    item_create: CartSneakerCreate,
):
    check_sizes_stmt = (
        select(Sneaker)
        .join(SneakerSizeAssociation)
        .where(
            Sneaker.id == item_create.sneaker_id,
            SneakerSizeAssociation.size_id == item_create.size_id,
        )
    )
    result = await session.execute(check_sizes_stmt)
    sneaker_size = result.scalar_one_or_none()

    if not sneaker_size:
        raise HTTPException(status_code=404, detail="Размер данной модели не найден")
