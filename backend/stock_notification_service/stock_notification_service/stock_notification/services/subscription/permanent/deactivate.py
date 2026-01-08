from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.enums import SubscriptionStatus
from stock_notification_service.stock_notification.models import UserSneakerSubscription


async def deactivate_user_subscription(
    subscription_id: int,
    user_id: int,
    session: AsyncSession,
):
    subscription = await session.scalar(
        select(UserSneakerSubscription).where(
            UserSneakerSubscription.user_id == user_id,
            UserSneakerSubscription.id == subscription_id,
            UserSneakerSubscription.status == SubscriptionStatus.ACTIVE,
        )
    )

    subscription.status = SubscriptionStatus.INACTIVE_BY_USER

    return {"record was deactivate"}
