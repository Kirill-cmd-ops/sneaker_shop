from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from cart_service.cart.models import Cart


async def read_cart(session: AsyncSession, user_id: int):
    cart = await session.scalar(
        select(Cart)
        .where(Cart.user_id == user_id)
        .options(
            selectinload(Cart.sneaker_associations),
            selectinload(Cart.sneakers),
        )
    )
    if cart is None:
        raise HTTPException(
            status_code=404, detail="У данного пользователя нету корзины"
        )

    return cart
