from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.stock_notification_service.stock_notification_service.stock_notification.enums import \
    SubscriptionStatus
from microservices.stock_notification_service.stock_notification_service.stock_notification.models import (
    UserSneakerOneTimeSubscription,
)


async def reactivate_all_one_time_subscriptions_for_sneaker_service(
        session: AsyncSession,
        sneaker_id: int,
):
    await session.execute(
        update(UserSneakerOneTimeSubscription)
        .where(
            UserSneakerOneTimeSubscription.sneaker_id == sneaker_id,
            UserSneakerOneTimeSubscription.status
            == SubscriptionStatus.INACTIVE_BY_SYSTEM,
            UserSneakerOneTimeSubscription.is_sent == False,
        )
        .values(status=SubscriptionStatus.ACTIVE)
    )
    await session.commit()
