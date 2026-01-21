from typing import Callable

from stock_notification_service.stock_notification.models import db_helper


async def create_record_service(
    table_name: Callable,
    schema_create,
):
    async with db_helper.session_context() as session:
        async with session.begin():
            new_record = table_name(**schema_create.dict())
            session.add(new_record)
