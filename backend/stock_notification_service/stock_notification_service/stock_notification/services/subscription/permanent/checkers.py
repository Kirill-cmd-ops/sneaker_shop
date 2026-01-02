from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.enums import SubscriptionStatus
from stock_notification_service.stock_notification.models import UserSneakerSubscription


async def user_has_active_subscription(
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


async def user_has_inactive_subscription(
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
