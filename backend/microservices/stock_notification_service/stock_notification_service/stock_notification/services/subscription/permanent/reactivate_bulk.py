from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.stock_notification_service.stock_notification_service.stock_notification.enums import \
    SubscriptionStatus
from microservices.stock_notification_service.stock_notification_service.stock_notification.models import \
    UserSneakerSubscription


async def reactivate_all_permanent_subscriptions_for_sneaker_service(
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
