from typing import Dict, Any

from microservices.stock_notification_service.stock_notification_service.stock_notification.models import Sneaker, \
    db_helper


async def create_sneaker_service(
        sneaker_data: Dict[str, Any],
):
    async with db_helper.session_context() as session:
        async with session.begin():
            sneaker = Sneaker(**sneaker_data)
            session.add(sneaker)
