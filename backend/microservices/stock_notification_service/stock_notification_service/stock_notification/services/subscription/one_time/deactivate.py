from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.stock_notification_service.stock_notification_service.stock_notification.domain.exceptions import \
    OneTimeSubscriptionNotFound
from microservices.stock_notification_service.stock_notification_service.stock_notification.enums import \
    SubscriptionStatus
from microservices.stock_notification_service.stock_notification_service.stock_notification.models import (
    UserSneakerOneTimeSubscription,
)


async def deactivate_user_one_time_subscription_service(
        subscription_id: int,
        user_id: int,
        session: AsyncSession,
) -> str:
    async with session.begin():
        subscription = await session.scalar(
            select(UserSneakerOneTimeSubscription).where(
                UserSneakerOneTimeSubscription.user_id == user_id,
                UserSneakerOneTimeSubscription.id == subscription_id,
                UserSneakerOneTimeSubscription.status == SubscriptionStatus.ACTIVE,
                UserSneakerOneTimeSubscription.is_sent == False,
            )
        )

        if not subscription:
            raise OneTimeSubscriptionNotFound()

        subscription.status = SubscriptionStatus.INACTIVE_BY_USER

    return "record was deactivate"
