from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.stock_notification_service.stock_notification_service.stock_notification.enums import \
    SubscriptionStatus
from microservices.stock_notification_service.stock_notification_service.stock_notification.models import (
    UserSneakerOneTimeSubscription,
)


async def check_active_one_time_subscription_service(
        session: AsyncSession,
        user_id: int,
        sneaker_id: int,
        size_id: int,
):
    user_active_subscription = await session.scalar(
        select(UserSneakerOneTimeSubscription).where(
            UserSneakerOneTimeSubscription.user_id == user_id,
            UserSneakerOneTimeSubscription.sneaker_id == sneaker_id,
            UserSneakerOneTimeSubscription.size_id == size_id,
            UserSneakerOneTimeSubscription.status == SubscriptionStatus.ACTIVE,
        )
    )
    if user_active_subscription:
        raise HTTPException(
            status_code=200,
            detail="Разовая подписка на данный товар присутствует у данного пользователя и она активна",
        )
