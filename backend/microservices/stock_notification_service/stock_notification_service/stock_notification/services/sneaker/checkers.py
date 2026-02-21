from sqlalchemy.ext.asyncio import AsyncSession

from microservices.stock_notification_service.stock_notification_service.stock_notification.domain.exceptions import \
    SneakerNotFound, SneakerIsInactive
from microservices.stock_notification_service.stock_notification_service.stock_notification.models import Sneaker


async def check_sneaker_active_service(
        session: AsyncSession,
        sneaker_id: int,
) -> None:
    current_sneaker = await session.get(Sneaker, sneaker_id)

    if not current_sneaker:
        raise SneakerNotFound()

    if not current_sneaker.is_active:
        raise SneakerIsInactive()
