from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.stock_notification_service.stock_notification_service.stock_notification.models import \
    SneakerSizeAssociation


async def check_inactive_sneaker_size_service(
        session: AsyncSession,
        sneaker_id: int,
        size_id: int,
):
    current_sneaker_sizes = await session.scalar(
        select(SneakerSizeAssociation).where(
            SneakerSizeAssociation.sneaker_id == sneaker_id,
            SneakerSizeAssociation.size_id == size_id,
            SneakerSizeAssociation.is_active == False,
        )
    )
    if not current_sneaker_sizes:
        raise HTTPException(
            status_code=404,
            detail="Данный размер отсутствует у данной модели, либо же он активен",
        )
