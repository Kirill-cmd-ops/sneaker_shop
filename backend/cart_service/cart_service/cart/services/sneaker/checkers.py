from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import Sneaker
from cart_service.cart.schemas import CartSneakerCreate


async def check_sneaker_exists_service(
    session: AsyncSession,
    item_create: CartSneakerCreate,
):
    sneaker = await session.get(Sneaker, item_create.sneaker_id)
    if not sneaker:
        raise HTTPException(status_code=404, detail="Товар не найден в каталоге")
