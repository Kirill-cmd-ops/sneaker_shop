from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.stock_notification_service.stock_notification_service.stock_notification.domain.exceptions import \
    PermanentSubscriptionAlreadyExists
from microservices.stock_notification_service.stock_notification_service.stock_notification.models import \
    UserSneakerSubscription


async def create_user_permanent_subscription_service(
        sneaker_id: int,
        size_id: int,
        user_id: int,
        session: AsyncSession,
):
    try:
        new_user_subscription = UserSneakerSubscription(
            user_id=user_id,
            sneaker_id=sneaker_id,
            size_id=size_id,
        )
        session.add(new_user_subscription)
    except IntegrityError:
        raise PermanentSubscriptionAlreadyExists()

    return {"status": new_user_subscription}
