from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import Cart


async def create_cart(session: AsyncSession, user_id: int):
    new_cart = Cart(user_id=user_id)
    session.add(new_cart)
    await session.commit()
    await session.refresh(new_cart)