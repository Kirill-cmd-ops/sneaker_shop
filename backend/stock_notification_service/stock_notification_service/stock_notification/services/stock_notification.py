from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.models import UserSneakerSubscription
from stock_notification_service.stock_notification.schemas.subscription import SubscriptionCreate


async def add_user_subscriptions(
    subscription_create: SubscriptionCreate,
    user_id: int,
    session: AsyncSession,
):
    user_subscription = UserSneakerSubscription(
        user_id=user_id,
        sneaker_id=subscription_create.sneaker_id,
        size_id=subscription_create.size_id,
    )
    session.add(user_subscription)
    return {"record": user_subscription}


async def delete_user_subscriptions(
    subscription_id: int,
    user_id: int,
    session: AsyncSession,
):
    request_delete_subscription_user = (
        delete(UserSneakerSubscription)
        .where(UserSneakerSubscription.user_id == user_id)
        .where(UserSneakerSubscription.id == subscription_id)
    )

    await session.execute(request_delete_subscription_user)

    return {"record was remove"}


async def delete_all_user_subscriptions(
    user_id: int,
    session: AsyncSession,
):
    request_delete_all_subscription_user = delete(UserSneakerSubscription).where(
        UserSneakerSubscription.user_id == user_id
    )

    await session.execute(request_delete_all_subscription_user)

    return {"records was remove"}


async def get_user_subscriptions_for_notifications(
    user_id: int,
    session: AsyncSession,
):
    request_view_all_subscription_user = select(UserSneakerSubscription).where(
        UserSneakerSubscription.user_id == user_id
    )

    result = await session.execute(request_view_all_subscription_user)
    all_subscription_user = result.scalars().all()

    return {"records": all_subscription_user}
