from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.models import User
from stock_notification_service.stock_notification.schemas import UserCreate


async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
):
    user = User(**user_create.dict())
    session.add(user)
    await session.flush()

    await session.commit()