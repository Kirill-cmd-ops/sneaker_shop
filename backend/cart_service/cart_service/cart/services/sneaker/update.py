from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import Sneaker
from cart_service.cart.schemas import SneakerUpdate


async def update_sneaker_service(
    session: AsyncSession,
    sneaker_id: int,
    sneaker_update: SneakerUpdate,
):
    sneaker = await session.get(Sneaker, sneaker_id)
    update_data = sneaker_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sneaker, field, value)

    session.add(sneaker)
    await session.commit()
