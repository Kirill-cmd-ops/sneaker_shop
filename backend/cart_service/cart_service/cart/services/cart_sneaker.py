from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import (
    Cart,
    CartSneakerAssociation,
    SneakerSizeAssociation,
)


async def create_sneaker_to_cart(
    session: AsyncSession,
    cart_id: int,
    sneaker_id: int,
    size_id: float,
):
    new_sneaker = CartSneakerAssociation(
        cart_id=cart_id,
        sneaker_id=sneaker_id,
        size_id=size_id,
    )
    session.add(new_sneaker)
    await session.commit()
    await session.refresh(new_sneaker)
    return new_sneaker


async def update_sneaker_to_cart(
    session: AsyncSession, cart_sneaker_id: int, size_id: float
) -> CartSneakerAssociation:
    request_get_sneaker = select(CartSneakerAssociation).where(
        CartSneakerAssociation.id == cart_sneaker_id
    )
    result = await session.execute(request_get_sneaker)
    current_sneaker = result.scalar()
    if not current_sneaker.sneaker_id:
        raise HTTPException(status_code=404, detail="Элемент корзины не найден")

    request_get_sneaker_sizes = select(SneakerSizeAssociation.size_id).where(
        SneakerSizeAssociation.sneaker_id == current_sneaker.sneaker_id
    )
    result_sneaker_sizes = await session.execute(request_get_sneaker_sizes)
    allowed_sneaker_sizes = result_sneaker_sizes.scalars().all()

    if size_id in allowed_sneaker_sizes:
        current_sneaker.size_id = size_id
    else:
        raise HTTPException(
            status_code=404, detail="У данной модели кроссовок этот размер отсутствует"
        )

    await session.commit()
    await session.refresh(current_sneaker)
    return current_sneaker


async def delete_sneaker_to_cart(
    session: AsyncSession,
    cart_sneaker_id: int,
    user_id: int,
) -> None:
    stmt = (
        select(CartSneakerAssociation)
        .join(Cart)
        .where(
            Cart.user_id == user_id,
            CartSneakerAssociation.id == cart_sneaker_id,
        )
    )
    result = await session.execute(stmt)
    association = result.scalar_one_or_none()

    if not association:
        raise HTTPException(status_code=404, detail="Объект корзины не найден")

    await session.delete(association)
    await session.commit()
