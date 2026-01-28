from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.stock_notification_service.stock_notification_service.stock_notification.enums import \
    SubscriptionStatus
from microservices.stock_notification_service.stock_notification_service.stock_notification.models import (
    UserSneakerOneTimeSubscription,
)


async def reactivate_one_time_subscription_by_id_service(
        subscription_id: int,
        user_id: int,
        session: AsyncSession,
):
    subscription = await session.scalar(
        select(UserSneakerOneTimeSubscription).where(
            UserSneakerOneTimeSubscription.user_id == user_id,
            UserSneakerOneTimeSubscription.id == subscription_id,
            UserSneakerOneTimeSubscription.status
            == SubscriptionStatus.INACTIVE_BY_USER,
        )
    )

    subscription.status = SubscriptionStatus.ACTIVE

    return {"record was reactivate"}


async def reactivate_one_time_subscription_by_sneaker_size_service(
        session: AsyncSession,
        user_id: int,
        sneaker_id: int,
        size_id: int,
):
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
        return {
            "status": "Подписка была реактивирована",
            "subscription": update_subscription,
        }
    return None
