from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.stock_notification_service.stock_notification_service.stock_notification.domain.exceptions import \
    OneTimeSubscriptionAlreadyExists
from microservices.stock_notification_service.stock_notification_service.stock_notification.models import \
    UserSneakerOneTimeSubscription


async def create_user_one_time_subscription_service(
        sneaker_id: int,
        size_id: int,
        user_id: int,
        session: AsyncSession,
):
    try:
        new_user_one_time_subscription = UserSneakerOneTimeSubscription(
            user_id=user_id,
            sneaker_id=sneaker_id,
            size_id=size_id,
        )
        session.add(new_user_one_time_subscription)
    except IntegrityError:
        raise OneTimeSubscriptionAlreadyExists()

    return {"status": new_user_one_time_subscription}
