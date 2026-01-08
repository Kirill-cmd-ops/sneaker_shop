from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.enums import SubscriptionStatus
from stock_notification_service.stock_notification.models import UserSneakerSubscription


async def reactivate_user_subscription(
    subscription_id: int,
    user_id: int,
    session: AsyncSession,
):
    subscription = await session.scalar(
        select(UserSneakerSubscription).where(
            UserSneakerSubscription.user_id == user_id,
            UserSneakerSubscription.id == subscription_id,
            UserSneakerSubscription.status == SubscriptionStatus.INACTIVE_BY_USER,
        )
    )

    subscription.status = SubscriptionStatus.ACTIVE

    return {"record was reactivate"}
