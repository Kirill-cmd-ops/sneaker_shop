from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.services.cart.fetch import get_cart_service
from cart_service.cart.services.cart.price import get_cart_total_service


async def get_cart_orchestrator(session: AsyncSession, user_id: int):
    async with session.begin():
        items = await get_cart_service(
            session=session,
            user_id=user_id,
        )

        total_price = get_cart_total_service(items=items)

        return {"Цена корзины: ": total_price, "Кроссовки": items}
