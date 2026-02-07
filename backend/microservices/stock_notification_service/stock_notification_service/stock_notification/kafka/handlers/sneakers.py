from microservices.stock_notification_service.stock_notification_service.stock_notification.schemas import (
    SneakerCreate,
    SneakerUpdate,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.sneaker.create import (
    create_sneaker_service,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.sneaker.delete import (
    delete_sneaker_service,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.sneaker.update import (
    update_sneaker_service,
)


async def handle_sneaker_event(key: str | None, value: dict):
    event_type = value.get("event_type")
    if event_type == "sneaker_created":
        data = value.get("data")
        sneaker_create = SneakerCreate(**data)
        sneaker_create_data = sneaker_create.model_dump()
        await create_sneaker_service(sneaker_data=sneaker_create_data)

    elif event_type == "sneaker_updated":
        data = value.get("data")
        sneaker_id = value.get("sneaker_id")
        sneaker_update = SneakerUpdate(**data)
        sneaker_update_data = sneaker_update.model_dump(exclude_unset=True)
        await update_sneaker_service(
            sneaker_id=sneaker_id,
            sneaker_data=sneaker_update_data,
        )

    elif event_type == "sneaker_deleted":
        sneaker_id = value.get("sneaker_id")
        await delete_sneaker_service(sneaker_id=sneaker_id)
