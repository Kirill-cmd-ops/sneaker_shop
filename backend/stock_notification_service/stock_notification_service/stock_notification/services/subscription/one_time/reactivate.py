from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.enums import SubscriptionStatus
from stock_notification_service.stock_notification.models import (
    UserSneakerOneTimeSubscription,
)


async def reactivate_user_one_time_subscription(
    subscription_id: int,
    user_id: int,
    session: AsyncSession,
):
    subscription = await session.scalar(
        select(UserSneakerOneTimeSubscription).where(
            UserSneakerOneTimeSubscription.user_id == user_id,
            UserSneakerOneTimeSubscription.id == subscription_id,
            UserSneakerOneTimeSubscription.status
            == SubscriptionStatus.INACTIVE_BY_USER,
        )
    )

    subscription.status = SubscriptionStatus.ACTIVE

    return {"record was reactivate"}
