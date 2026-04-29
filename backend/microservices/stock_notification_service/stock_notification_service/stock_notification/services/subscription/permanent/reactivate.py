from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.stock_notification_service.stock_notification_service.stock_notification.domain.exceptions import \
    PermanentSubscriptionNotFound
from microservices.stock_notification_service.stock_notification_service.stock_notification.enums import \
    SubscriptionStatus
from microservices.stock_notification_service.stock_notification_service.stock_notification.models import \
    UserSneakerSubscription


async def reactivate_permanent_subscription_by_id_service(
        subscription_id: int,
        user_id: int,
        session: AsyncSession,
) -> UserSneakerSubscription:
    subscription = await session.scalar(
        select(UserSneakerSubscription).where(
            UserSneakerSubscription.user_id == user_id,
            UserSneakerSubscription.id == subscription_id,
            UserSneakerSubscription.status == SubscriptionStatus.INACTIVE_BY_USER,
        )
    )

    if not subscription:
        raise PermanentSubscriptionNotFound()

    subscription.status = SubscriptionStatus.ACTIVE

    return subscription


async def reactivate_permanent_subscription_by_sneaker_size_service(
        session: AsyncSession,
        user_id: int,
        sneaker_id: int,
        size_id: int,
) -> UserSneakerSubscription | None:
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
        return update_subscription
    return None
