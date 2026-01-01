from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.models import User
from stock_notification_service.stock_notification.schemas import UserUpdate


async def update_user(
    session: AsyncSession, user_id: int, user_update: UserUpdate
):
    user = await session.get(User, user_id)
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    session.add(user)
    await session.commit()