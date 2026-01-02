from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from stock_notification_service.stock_notification.enums import SubscriptionStatus
from stock_notification_service.stock_notification.models import UserSneakerSubscription


async def get_user_active_subscriptions(
    user_id: int,
    session: AsyncSession,
):
    request_view_all_subscription_user = select(UserSneakerSubscription).where(
        UserSneakerSubscription.user_id == user_id,
        UserSneakerSubscription.status == SubscriptionStatus.ACTIVE,
    )

    result = await session.execute(request_view_all_subscription_user)
    all_subscription_user = result.scalars().all()

    return {"records": all_subscription_user}