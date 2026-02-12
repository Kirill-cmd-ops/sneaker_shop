from typing import Callable, Dict, Any

from sqlalchemy.exc import IntegrityError

from microservices.stock_notification_service.stock_notification_service.stock_notification.models import db_helper


async def create_record_service(
        table_name: Callable,
        data: Dict[str, Any],
):
    try:
        async with db_helper.session_context() as session:
            async with session.begin():
                new_record = table_name(**data)
                session.add(new_record)
    except IntegrityError:
        return
