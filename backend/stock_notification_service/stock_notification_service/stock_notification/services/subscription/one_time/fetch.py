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
    request_view_all_subscription_user = select(UserSneakerOneTimeSubscription).where(
        UserSneakerOneTimeSubscription.user_id == user_id,
        UserSneakerOneTimeSubscription.status == SubscriptionStatus.ACTIVE,
    )

    result = await session.execute(request_view_all_subscription_user)
    all_subscription_user = result.scalars().all()

    return {"records": all_subscription_user}


async def get_sneaker_active_one_time_subscriptions(
    session: AsyncSession,
    sneaker_id: int,
    size_id: int,
):
    stmt = (
        select(UserSneakerOneTimeSubscription)
        .where(
            UserSneakerOneTimeSubscription.sneaker_id == sneaker_id,
            UserSneakerOneTimeSubscription.size_id == size_id,
            UserSneakerOneTimeSubscription.status == SubscriptionStatus.ACTIVE,
        )
        .options(selectinload(UserSneakerOneTimeSubscription.user))
    )
    result = await session.execute(stmt)
    return result.scalars().all()