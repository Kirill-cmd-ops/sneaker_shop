from typing import Dict, Any

from microservices.stock_notification_service.stock_notification_service.stock_notification.models import User, \
    db_helper


async def create_user_service(
        user_data: Dict[str, Any],
):
    async with db_helper.session_context() as session:
        async with session.begin():
            user = User(**user_data)
            session.add(user)
