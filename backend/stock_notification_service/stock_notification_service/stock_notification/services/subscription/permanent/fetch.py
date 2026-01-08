from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from stock_notification_service.stock_notification.enums import SubscriptionStatus
from stock_notification_service.stock_notification.models import UserSneakerSubscription


async def get_user_active_subscriptions(
    user_id: int,
    session: AsyncSession,
):
    result = await session.scalars(
        select(UserSneakerSubscription).where(
            UserSneakerSubscription.user_id == user_id,
            UserSneakerSubscription.status == SubscriptionStatus.ACTIVE,
        )
    )

    all_subscription_user = result.all()

    return {"records": all_subscription_user}


async def get_sneaker_active_subscriptions(
    session: AsyncSession,
    sneaker_id: int,
    size_id: int,
):
    result = await session.scalars(
        select(UserSneakerSubscription)
        .where(
            UserSneakerSubscription.sneaker_id == sneaker_id,
            UserSneakerSubscription.size_id == size_id,
            UserSneakerSubscription.status == SubscriptionStatus.ACTIVE,
        )
        .options(selectinload(UserSneakerSubscription.user))
    )

    return result.all()
