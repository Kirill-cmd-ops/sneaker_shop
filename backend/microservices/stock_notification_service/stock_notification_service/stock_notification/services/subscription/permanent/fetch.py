from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from stock_notification_service.stock_notification.enums import SubscriptionStatus
from stock_notification_service.stock_notification.models import UserSneakerSubscription


async def get_active_permanent_subscriptions_for_user_service(
    user_id: int,
    session: AsyncSession,
):
    result = await session.scalars(
        select(UserSneakerSubscription).where(
            UserSneakerSubscription.user_id == user_id,
            UserSneakerSubscription.status == SubscriptionStatus.ACTIVE,
        )
    )

    all_subscription_user = result.all()

    return {"records": all_subscription_user}


async def get_active_permanent_subscriptions_for_sneaker_service(
    session: AsyncSession,
    sneaker_id: int,
    size_id: int,
):
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
):
    subscription = await session.scalar(
        select(UserSneakerSubscription).where(
            UserSneakerSubscription.user_id == user_id,
            UserSneakerSubscription.id == subscription_id,
            UserSneakerSubscription.status == SubscriptionStatus.INACTIVE_BY_USER,
        )
    )

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="Подписка требующая реактивации не найдена",
        )
    return subscription
