from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from microservices.stock_notification_service.stock_notification_service.stock_notification.domain.exceptions import \
    PermanentSubscriptionNotFound
from microservices.stock_notification_service.stock_notification_service.stock_notification.enums import \
    SubscriptionStatus
from microservices.stock_notification_service.stock_notification_service.stock_notification.models import \
    UserSneakerSubscription


async def get_active_permanent_subscriptions_for_user_service(
        user_id: int,
        session: AsyncSession,
) -> Sequence[UserSneakerSubscription]:
    result = await session.scalars(
        select(UserSneakerSubscription).where(
            UserSneakerSubscription.user_id == user_id,
            UserSneakerSubscription.status == SubscriptionStatus.ACTIVE,
        )
    )

    return result.all()


async def get_active_permanent_subscriptions_for_sneaker_service(
        session: AsyncSession,
        sneaker_id: int,
        size_id: int,
) -> Sequence[UserSneakerSubscription]:
    result = await session.scalars(
        select(UserSneakerSubscription)
        .where(
            UserSneakerSubscription.sneaker_id == sneaker_id,
            UserSneakerSubscription.size_id == size_id,
            UserSneakerSubscription.status == SubscriptionStatus.ACTIVE,
        )
        .options(selectinload(UserSneakerSubscription.user))
    )

    return result.all()


async def get_inactive_permanent_subscription_for_user_service(
        session: AsyncSession,
        user_id: int,
        subscription_id: int,
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

    return subscription
