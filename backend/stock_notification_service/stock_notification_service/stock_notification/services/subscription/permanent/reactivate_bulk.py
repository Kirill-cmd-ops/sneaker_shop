from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.enums import SubscriptionStatus
from stock_notification_service.stock_notification.models import UserSneakerSubscription


async def reactivate_all_sneaker_subscriptions(
    session: AsyncSession,
    sneaker_id: int,
):
    await session.execute(
        update(UserSneakerSubscription)
        .where(
            UserSneakerSubscription.sneaker_id == sneaker_id,
            UserSneakerSubscription.status == SubscriptionStatus.INACTIVE_BY_SYSTEM,
        )
        .values(status=SubscriptionStatus.ACTIVE)
    )
    await session.commit()