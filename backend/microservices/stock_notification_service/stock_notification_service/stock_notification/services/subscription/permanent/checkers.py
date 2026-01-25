from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.enums import SubscriptionStatus
from stock_notification_service.stock_notification.models import UserSneakerSubscription


async def check_active_permanent_subscription_service(
    session: AsyncSession,
    user_id: int,
    sneaker_id: int,
    size_id: int,
):
    user_active_subscription = await session.scalar(
        select(UserSneakerSubscription).where(
            UserSneakerSubscription.user_id == user_id,
            UserSneakerSubscription.sneaker_id == sneaker_id,
            UserSneakerSubscription.size_id == size_id,
            UserSneakerSubscription.status == SubscriptionStatus.ACTIVE,
        )
    )
    if user_active_subscription:
        raise HTTPException(
            status_code=200,
            detail="Перманентная подписка на данный товар присутствует у данного пользователя и она активна",
        )
