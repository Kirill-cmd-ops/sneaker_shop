from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.schemas import SneakerUpdate
from stock_notification_service.stock_notification.models import Sneaker


async def update_sneaker(
    session: AsyncSession, sneaker_id: int, sneaker_update: SneakerUpdate
):
    sneaker = await session.get(Sneaker, sneaker_id)
    update_data = sneaker_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sneaker, field, value)

    session.add(sneaker)
    await session.commit()