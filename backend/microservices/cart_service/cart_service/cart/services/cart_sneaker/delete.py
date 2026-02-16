from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.cart_service.cart_service.cart.models import CartSneakerAssociation, Cart


async def delete_sneaker_from_cart_service(
        session: AsyncSession,
        cart_sneaker_id: int,
        user_id: int,
) -> str:
    async with session.begin():
        stmt = delete(CartSneakerAssociation).where(
            CartSneakerAssociation.id == cart_sneaker_id,
            CartSneakerAssociation.cart_id.in_(
                select(Cart.id).where(Cart.user_id == user_id)
            ),
        )
        await session.execute(stmt)
    return "Элемент удалён"
