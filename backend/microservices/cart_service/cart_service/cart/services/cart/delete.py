from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.cart_service.cart_service.cart.models import Cart


async def delete_cart_service(session: AsyncSession, user_id: int):
    async with session.begin():
        stmt = delete(Cart).where(Cart.user_id == user_id)
        await session.execute(stmt)
    return {"Корзина пользователя было удалено успешно"}
