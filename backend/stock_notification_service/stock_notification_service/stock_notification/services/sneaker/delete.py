from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.models import Sneaker


async def delete_sneaker_service(session: AsyncSession, sneaker_id: int):
    stmt = delete(Sneaker).where(Sneaker.id == sneaker_id)
    await session.execute(stmt)

    await session.commit()
