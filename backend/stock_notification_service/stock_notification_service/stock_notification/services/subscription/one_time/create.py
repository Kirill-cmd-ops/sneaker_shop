from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.models import UserSneakerOneTimeSubscription


async def add_user_one_time_subscription(
    sneaker_id: int,
    size_id: int,
    user_id: int,
    session: AsyncSession,
):
    new_user_one_time_subscription = UserSneakerOneTimeSubscription(
        user_id=user_id,
        sneaker_id=sneaker_id,
        size_id=size_id,
    )
    session.add(new_user_one_time_subscription)
    return {"status": new_user_one_time_subscription}