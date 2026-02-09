from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from microservices.cart_service.cart_service.cart.domain.exceptions import CartNotFound
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
        raise CartNotFound

    return cart


async def get_user_cart_id_service(
        session: AsyncSession,
        user_id: int,
):
    cart_id = await session.scalar(select(Cart.id).filter(Cart.user_id == user_id))
    if not cart_id:
        raise CartNotFound

    return cart_id
