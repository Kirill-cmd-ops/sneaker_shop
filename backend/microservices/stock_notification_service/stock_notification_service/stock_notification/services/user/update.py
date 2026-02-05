from typing import Dict, Any

from microservices.stock_notification_service.stock_notification_service.stock_notification.models import User, \
    db_helper


async def update_user_service(
        user_id: int,
        user_data: Dict[str, Any],
):
    async with db_helper.session_context() as session:
        async with session.begin():
            user = await session.get(User, user_id)

            for field, value in user_data.items():
                setattr(user, field, value)

            session.add(user)
