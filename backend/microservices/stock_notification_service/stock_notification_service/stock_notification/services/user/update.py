from microservices.stock_notification_service.stock_notification_service.stock_notification.models import User, \
    db_helper
from microservices.stock_notification_service.stock_notification_service.stock_notification.schemas import UserUpdate


async def update_user_service(
        user_id: int,
        user_update: UserUpdate,
):
    async with db_helper.session_context() as session:
        async with session.begin():
            user = await session.get(User, user_id)
            update_data = user_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)

            session.add(user)
