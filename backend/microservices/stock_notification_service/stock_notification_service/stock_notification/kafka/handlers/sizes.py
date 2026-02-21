from microservices.stock_notification_service.stock_notification_service.stock_notification.models import Size
from microservices.stock_notification_service.stock_notification_service.stock_notification.schemas import SizeCreate
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.record.create import (
    create_record_service,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.record.delete import (
    delete_record_service,
)


async def handle_size_event(key: str | None, value: dict) -> None:
    event_type = value.get("event_type")
    if event_type == "size_created":
        data = value.get("data")
        size_create = SizeCreate(**data)
        size_create_data = size_create.model_dump()
        await create_record_service(
            table_name=Size,
            data=size_create_data,
        )

    elif event_type == "size_deleted":
        size_id = value.get("size_id")
        await delete_record_service(
            table_name=Size,
            record_id=size_id,
        )
