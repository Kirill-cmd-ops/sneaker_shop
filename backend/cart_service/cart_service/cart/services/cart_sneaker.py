from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models.cart import Cart
from cart_service.cart.models.cart_sneaker import CartSneakerAssociation



async def create_sneaker_to_cart(
    session: AsyncSession,
    cart_id: int,
    sneaker_id: int,
    sneaker_size: float,
):
    new_sneaker = CartSneakerAssociation(
        cart_id=cart_id,
        sneaker_id=sneaker_id,
        sneaker_size=sneaker_size,
    )
    session.add(new_sneaker)
    await session.commit()
    await session.refresh(new_sneaker)
    return new_sneaker


async def update_sneaker_to_cart(
    session: AsyncSession, association_id: int, sneaker_size: float
) -> CartSneakerAssociation:
    current_sneaker = await session.get(CartSneakerAssociation, association_id)
    if not current_sneaker:
        raise HTTPException(status_code=404, detail="Элемент корзины не найден")
    current_sneaker.sneaker_size = sneaker_size
    await session.commit()
    await session.refresh(current_sneaker)
    return current_sneaker


async def delete_sneaker_to_cart(
    session: AsyncSession,
    user_id: int,
    sneaker_id: int,
) -> None:
    stmt = (
        select(CartSneakerAssociation)
        .join(Cart)
        .where(
            Cart.user_id == user_id,
            CartSneakerAssociation.sneaker_id == sneaker_id,
        )
    )
    result = await session.execute(stmt)
    association = result.scalar_one_or_none()

    if not association:
        raise HTTPException(status_code=404, detail="Объект корзины не найден")

    await session.delete(association)
    await session.commit()
