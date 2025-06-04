from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from cart_service.cart.models.cart import Cart


async def create_cart(session: AsyncSession, user_id: int):
    new_cart = Cart(user_id=user_id)
    session.add(new_cart)
    await session.commit()
    await session.refresh(new_cart)

async def read_cart(session: AsyncSession, user_id: int):
    stmt = select(Cart).where(Cart.user_id == user_id).options(selectinload(Cart.sneakers))
    result = await session.execute(stmt)
    cart = result.scalar_one_or_none()
    if cart is None:
        return []

    return cart.sneakers