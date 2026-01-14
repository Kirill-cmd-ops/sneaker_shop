from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.models import Sneaker


async def check_sneaker_active_service(
    session: AsyncSession,
    sneaker_id: int,
):
    current_sneaker = await session.get(Sneaker, sneaker_id)
    if not current_sneaker.is_active:
        raise HTTPException(
            status_code=404,
            detail="Данный товар неактивен, подписка невозможна",
        )
