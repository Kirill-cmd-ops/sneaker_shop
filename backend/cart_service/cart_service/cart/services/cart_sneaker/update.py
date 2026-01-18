from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import (
    CartSneakerAssociation,
    Cart,
    SneakerSizeAssociation,
    db_helper,
)


async def update_sneaker_in_cart_service(
    session: AsyncSession,
    cart_sneaker_id: int,
    size_id: int,
    user_id: int,
) -> CartSneakerAssociation:
    async with session.begin():
        current_sneaker = await session.scalar(
            select(CartSneakerAssociation).where(
                CartSneakerAssociation.id == cart_sneaker_id,
                CartSneakerAssociation.cart_id.in_(
                    select(Cart.id).where(Cart.user_id == user_id),
                ),
            )
        )

        result_sneaker_sizes = await session.scalars(
            select(SneakerSizeAssociation.size_id).where(
                SneakerSizeAssociation.sneaker_id == current_sneaker.sneaker_id
            )
        )
        allowed_sneaker_sizes = result_sneaker_sizes.all()

        if size_id in allowed_sneaker_sizes:
            current_sneaker.size_id = size_id
        else:
            raise HTTPException(
                status_code=404,
                detail="У данной модели кроссовок этот размер отсутствует",
            )

    return current_sneaker


async def increment_sneaker_quantity_in_cart_service(
    cart_sneaker_id: int,
    cart_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    sneaker_record = await session.scalar(
        select(CartSneakerAssociation).where(
            CartSneakerAssociation.id == cart_sneaker_id,
            CartSneakerAssociation.cart_id == cart_id,
        )
    )

    if sneaker_record:
        sneaker_record.quantity += 1

        return {"status": "quantity += 1"}
    return {"status": "there is no such record"}


async def decrement_sneaker_quantity_in_cart_service(
    cart_sneaker_id: int,
    cart_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    sneaker_record = await session.scalar(
        select(CartSneakerAssociation).where(
            CartSneakerAssociation.id == cart_sneaker_id,
            CartSneakerAssociation.cart_id == cart_id,
            CartSneakerAssociation.quantity > 1,
        )
    )

    if sneaker_record:
        sneaker_record.quantity -= 1

        return {"status": "quantity -= 1"}
    return {"status": "quantity = 1"}
