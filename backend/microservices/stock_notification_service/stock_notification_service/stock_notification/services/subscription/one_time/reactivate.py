from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.stock_notification_service.stock_notification_service.stock_notification.domain.exceptions import \
    OneTimeSubscriptionNotFound
from microservices.stock_notification_service.stock_notification_service.stock_notification.enums import \
    SubscriptionStatus
from microservices.stock_notification_service.stock_notification_service.stock_notification.models import (
    UserSneakerOneTimeSubscription,
)


async def reactivate_one_time_subscription_by_id_service(
        subscription_id: int,
        user_id: int,
        session: AsyncSession,
) -> UserSneakerOneTimeSubscription:
    subscription = await session.scalar(
        select(UserSneakerOneTimeSubscription).where(
            UserSneakerOneTimeSubscription.user_id == user_id,
            UserSneakerOneTimeSubscription.id == subscription_id,
            UserSneakerOneTimeSubscription.status
            == SubscriptionStatus.INACTIVE_BY_USER,
        )
    )

    if not subscription:
        raise OneTimeSubscriptionNotFound()

    subscription.status = SubscriptionStatus.ACTIVE

    return subscription


async def reactivate_one_time_subscription_by_sneaker_size_service(
        session: AsyncSession,
        user_id: int,
        sneaker_id: int,
        size_id: int,
) -> UserSneakerOneTimeSubscription | None:
    stmt = (
        update(UserSneakerOneTimeSubscription)
        .where(
            UserSneakerOneTimeSubscription.user_id == user_id,
            UserSneakerOneTimeSubscription.sneaker_id == sneaker_id,
            UserSneakerOneTimeSubscription.size_id == size_id,
            UserSneakerOneTimeSubscription.status
            == SubscriptionStatus.INACTIVE_BY_USER,
        )
        .values(status=SubscriptionStatus.ACTIVE)
        .returning(UserSneakerOneTimeSubscription)
    )

    update_subscription = await session.scalar(stmt)
    if update_subscription:
        return update_subscription
    return None
