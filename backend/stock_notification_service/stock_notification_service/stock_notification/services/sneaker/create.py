from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.schemas import SneakerCreate
from stock_notification_service.stock_notification.models import Sneaker


async def create_sneaker_service(
    session: AsyncSession,
    sneaker_create: SneakerCreate,
):
    sneaker = Sneaker(**sneaker_create.dict())
    session.add(sneaker)
    await session.flush()

    await session.commit()
