from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.stock_notification_service.stock_notification_service.stock_notification.enums import \
    SubscriptionStatus
from microservices.stock_notification_service.stock_notification_service.stock_notification.models import \
    UserSneakerSubscription


async def reactivate_permanent_subscription_by_id_service(
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


async def reactivate_permanent_subscription_by_sneaker_size_service(
        session: AsyncSession,
        user_id: int,
        sneaker_id: int,
        size_id: int,
):
    stmt = (
        update(UserSneakerSubscription)
        .where(
            UserSneakerSubscription.user_id == user_id,
            UserSneakerSubscription.sneaker_id == sneaker_id,
            UserSneakerSubscription.size_id == size_id,
            UserSneakerSubscription.status == SubscriptionStatus.INACTIVE_BY_USER,
        )
        .values(status=SubscriptionStatus.ACTIVE)
        .returning(UserSneakerSubscription)
    )

    update_subscription = await session.scalar(stmt)
    if update_subscription:
        return {"status": "Подписка была создана", "subscription": update_subscription}
    return None
