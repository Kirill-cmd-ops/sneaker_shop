from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import Cart


async def check_cart_exists(
    session: AsyncSession,
    user_id: int,
):
    cart_id = await session.scalar(select(Cart.id).filter(Cart.user_id == user_id))
    if not cart_id:
        raise HTTPException(status_code=404, detail="Корзина пользователя не найдена")
    return cart_id
