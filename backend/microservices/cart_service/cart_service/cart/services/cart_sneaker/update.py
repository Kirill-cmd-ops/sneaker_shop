from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.cart_service.cart_service.cart.domain.exceptions import SneakerNotFoundInCart, \
    SneakerSizeNotAvailable
from microservices.cart_service.cart_service.cart.models import (
    CartSneakerAssociation,
    Cart,
    SneakerSizeAssociation,
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
        if not current_sneaker:
            raise SneakerNotFoundInCart()

        result_sneaker_sizes = await session.scalars(
            select(SneakerSizeAssociation.size_id).where(
                SneakerSizeAssociation.sneaker_id == current_sneaker.sneaker_id
            )
        )
        allowed_sneaker_sizes = result_sneaker_sizes.all()

        if size_id in allowed_sneaker_sizes:
            current_sneaker.size_id = size_id
        else:
            raise SneakerSizeNotAvailable()

    return current_sneaker


async def increment_sneaker_quantity_in_cart_service(
        session: AsyncSession,
        cart_sneaker_id: int,
        cart_id: int,
) -> CartSneakerAssociation:
    sneaker_record = await session.scalar(
        select(CartSneakerAssociation).where(
            CartSneakerAssociation.id == cart_sneaker_id,
            CartSneakerAssociation.cart_id == cart_id,
        )
    )
    if not sneaker_record:
        raise SneakerNotFoundInCart()

    sneaker_record.quantity += 1
    return sneaker_record


async def decrement_sneaker_quantity_in_cart_service(
        session: AsyncSession,
        cart_sneaker_id: int,
        cart_id: int,
) -> CartSneakerAssociation:
    sneaker_record = await session.scalar(
        select(CartSneakerAssociation).where(
            CartSneakerAssociation.id == cart_sneaker_id,
            CartSneakerAssociation.cart_id == cart_id,
            CartSneakerAssociation.quantity > 1,
        )
    )

    if not sneaker_record:
        raise SneakerNotFoundInCart()

    sneaker_record.quantity -= 1
    return sneaker_record
