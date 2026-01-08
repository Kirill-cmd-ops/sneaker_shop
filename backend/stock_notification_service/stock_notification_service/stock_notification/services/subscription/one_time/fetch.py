from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from stock_notification_service.stock_notification.enums import SubscriptionStatus
from stock_notification_service.stock_notification.models import (
    UserSneakerOneTimeSubscription,
)


async def get_user_active_one_time_subscriptions(
    user_id: int,
    session: AsyncSession,
):
    result = await session.scalars(
        select(UserSneakerOneTimeSubscription).where(
            UserSneakerOneTimeSubscription.user_id == user_id,
            UserSneakerOneTimeSubscription.status == SubscriptionStatus.ACTIVE,
        )
    )
    return {"records": result.all()}


async def get_user_inactive_one_time_subscription(
    session: AsyncSession,
    user_id: int,
    subscription_id: int,
):
    return await session.scalar(
        select(UserSneakerOneTimeSubscription).where(
            UserSneakerOneTimeSubscription.user_id == user_id,
            UserSneakerOneTimeSubscription.id == subscription_id,
        )
    )


async def get_sneaker_active_one_time_subscriptions(
    session: AsyncSession,
    sneaker_id: int,
    size_id: int,
):
    result = await session.scalars(
        select(UserSneakerOneTimeSubscription)
        .where(
            UserSneakerOneTimeSubscription.sneaker_id == sneaker_id,
            UserSneakerOneTimeSubscription.size_id == size_id,
            UserSneakerOneTimeSubscription.status == SubscriptionStatus.ACTIVE,
        )
        .options(selectinload(UserSneakerOneTimeSubscription.user))
    )

    return result.all()
