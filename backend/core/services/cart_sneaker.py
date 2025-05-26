from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.models import CartSneakerAssociation


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
    session: AsyncSession, association_id: int
) -> None:
    current_sneaker = await session.get(CartSneakerAssociation, association_id)
    if not current_sneaker:
        raise HTTPException(status_code=404, detail="Элемент корзины не найден")
    await session.delete(current_sneaker)
    await session.commit()
