from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.stock_notification_service.stock_notification_service.stock_notification.enums import \
    SubscriptionStatus
from microservices.stock_notification_service.stock_notification_service.stock_notification.models import \
    UserSneakerSubscription


async def deactivate_all_permanent_subscriptions_for_user_service(
        user_id: int,
        session: AsyncSession,
):
    async with session.begin():
        await session.execute(
            update(UserSneakerSubscription)
            .where(
                UserSneakerSubscription.user_id == user_id,
                UserSneakerSubscription.status == SubscriptionStatus.ACTIVE,
            )
            .values(status=SubscriptionStatus.INACTIVE_BY_USER)
        )

    return {"records was deactivate"}


async def deactivate_all_permanent_subscriptions_for_sneaker_service(
        session: AsyncSession,
        sneaker_id: int,
):
    await session.execute(
        update(UserSneakerSubscription)
        .where(
            UserSneakerSubscription.sneaker_id == sneaker_id,
            UserSneakerSubscription.status == SubscriptionStatus.ACTIVE,
        )
        .values(status=SubscriptionStatus.INACTIVE_BY_SYSTEM)
    )
    await session.commit()
