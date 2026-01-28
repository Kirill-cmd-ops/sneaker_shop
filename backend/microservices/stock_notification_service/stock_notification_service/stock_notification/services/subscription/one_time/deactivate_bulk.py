from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.stock_notification_service.stock_notification_service.stock_notification.enums import \
    SubscriptionStatus
from microservices.stock_notification_service.stock_notification_service.stock_notification.models import (
    UserSneakerOneTimeSubscription,
)


async def deactivate_all_one_time_subscriptions_for_user_service(
        user_id: int,
        session: AsyncSession,
):
    async with session.begin():
        await session.execute(
            update(UserSneakerOneTimeSubscription)
            .where(
                UserSneakerOneTimeSubscription.user_id == user_id,
                UserSneakerOneTimeSubscription.status == SubscriptionStatus.ACTIVE,
                UserSneakerOneTimeSubscription.is_sent == False,
            )
            .values(status=SubscriptionStatus.INACTIVE_BY_USER)
        )

    return {"records was deactivate"}


async def deactivate_all_one_time_subscriptions_for_sneaker_service(
        session: AsyncSession,
        sneaker_id: int,
):
    await session.execute(
        update(UserSneakerOneTimeSubscription)
        .where(
            UserSneakerOneTimeSubscription.sneaker_id == sneaker_id,
            UserSneakerOneTimeSubscription.status == SubscriptionStatus.ACTIVE,
            UserSneakerOneTimeSubscription.is_sent == False,
        )
        .values(status=SubscriptionStatus.INACTIVE_BY_SYSTEM)
    )
    await session.commit()
