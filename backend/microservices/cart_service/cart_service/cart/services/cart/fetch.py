from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from microservices.cart_service.cart_service.cart.models import Cart


async def get_cart_service(session: AsyncSession, user_id: int):
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


async def get_user_cart_id_service(
        session: AsyncSession,
        user_id: int,
):
    cart_id = await session.scalar(select(Cart.id).filter(Cart.user_id == user_id))
    if not cart_id:
        raise HTTPException(status_code=404, detail="Корзина пользователя не найдена")
    return cart_id
