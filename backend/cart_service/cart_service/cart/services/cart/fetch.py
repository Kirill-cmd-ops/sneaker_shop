from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from cart_service.cart.models import Cart


async def read_cart(session: AsyncSession, user_id: int):
    stmt = (
        select(Cart)
        .where(Cart.user_id == user_id)
        .options(
            selectinload(Cart.sneaker_associations),
            selectinload(Cart.sneakers),
        )
    )
    result = await session.execute(stmt)
    cart = result.scalar_one_or_none()
    if cart is None:
        raise HTTPException(
            status_code=404, detail="У данного пользователя нету корзины"
        )

    return cart