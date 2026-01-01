from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.enums import SubscriptionStatus
from stock_notification_service.stock_notification.models import (
    UserSneakerOneTimeSubscription,
)


async def deactivate_all_user_one_time_subscriptions(
    user_id: int,
    session: AsyncSession,
):
    await session.execute(
        update(UserSneakerOneTimeSubscription)
        .where(
            UserSneakerOneTimeSubscription.user_id == user_id,
            UserSneakerOneTimeSubscription.status == SubscriptionStatus.ACTIVE,
            UserSneakerOneTimeSubscription.is_sent == False,
        )
        .values(status=SubscriptionStatus.INACTIVE_BY_USER)
    )

    return {"records was deactivate"}


async def deactivate_all_sneaker_one_time_subscriptions(
    session: AsyncSession,
    sneaker_id: int,
):
    await session.execute(
        update(UserSneakerOneTimeSubscription)
        .where(
            UserSneakerOneTimeSubscription.sneaker_id == sneaker_id,
            UserSneakerOneTimeSubscription.status == SubscriptionStatus.ACTIVE,
            UserSneakerOneTimeSubscription.is_sent == False,
        )
        .values(status=SubscriptionStatus.INACTIVE_BY_SYSTEM)
    )
    await session.commit()
