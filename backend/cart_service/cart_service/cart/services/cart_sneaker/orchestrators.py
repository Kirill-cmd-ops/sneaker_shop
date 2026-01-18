from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.services.cart.fetch import get_user_cart_id_service
from cart_service.cart.services.cart_sneaker.create import add_sneaker_to_cart_service
from cart_service.cart.services.cart_sneaker.fetch import get_sneaker_in_cart_service
from cart_service.cart.services.sneaker.checkers import check_sneaker_exists_service
from cart_service.cart.services.sneaker_size.checkers import (
    check_sneaker_has_size_service,
)


async def add_sneaker_to_cart_orchestrator(
    session: AsyncSession,
    user_id: int,
    sneaker_id: int,
    size_id: int,
):
    async with session.begin():
        cart_id = await get_user_cart_id_service(
            session=session,
            user_id=user_id,
        )
        await check_sneaker_exists_service(
            session=session,
            sneaker_id=sneaker_id,
        )
        await check_sneaker_has_size_service(
            session=session,
            sneaker_id=sneaker_id,
            size_id=size_id,
        )
        sneaker_record = await get_sneaker_in_cart_service(
            session=session,
            cart_id=cart_id,
            sneaker_id=sneaker_id,
            size_id=size_id,
        )

        if sneaker_record is None:
            await add_sneaker_to_cart_service(
                session=session,
                cart_id=cart_id,
                sneaker_id=sneaker_id,
                size_id=size_id,
            )
            return {"status": "Элемент добавлен"}

    return {"status": "Товар уже есть в корзине"}
