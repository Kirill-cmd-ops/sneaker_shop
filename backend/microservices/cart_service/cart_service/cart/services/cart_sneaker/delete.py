from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.cart_service.cart_service.cart.domain.exceptions import SneakerNotFoundInCart
from microservices.cart_service.cart_service.cart.models import CartSneakerAssociation, Cart


async def delete_sneaker_from_cart_service(
        session: AsyncSession,
        cart_sneaker_id: int,
        user_id: int,
) -> None:
    async with session.begin():
        stmt = delete(CartSneakerAssociation).where(
            CartSneakerAssociation.id == cart_sneaker_id,
            CartSneakerAssociation.cart_id.in_(
                select(Cart.id).where(Cart.user_id == user_id)
            ),
        )
        result = await session.execute(stmt)

        if result.rowcount == 0:
            raise SneakerNotFoundInCart()
