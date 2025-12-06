from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.models import (
    UserSneakerSubscription,
    User,
)


async def get_subscribed_users(
    session: AsyncSession,
    sneaker_id: int,
    size_id: int,
):
    stmt = (
        select(User.email)
        .join(User.sneaker_size_subscriptions)
        .where(UserSneakerSubscription.sneaker_id == sneaker_id)
        .where(UserSneakerSubscription.size_id == size_id)
    )

    result = await session.execute(stmt)
    return result.scalars().all()

