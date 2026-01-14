from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.models import User


async def delete_user_service(session: AsyncSession, user_id: int):
    stmt = delete(User).where(User.id == user_id)
    await session.execute(stmt)

    await session.commit()
