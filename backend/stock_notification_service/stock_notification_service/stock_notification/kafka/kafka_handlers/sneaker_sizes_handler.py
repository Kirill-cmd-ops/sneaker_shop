from stock_notification_service.stock_notification.models import (
    db_helper,
    SneakerSizeAssociation,
)
from stock_notification_service.stock_notification.schemas import (
    SneakerSizesCreate,
    SneakerSizeUpdate,
    SneakerAssocsDelete,
)
from stock_notification_service.stock_notification.services.sneaker_sizes import (
    create_sneaker_sizes,
    update_sneaker_sizes,
    delete_sneaker_association,
)


async def handle_sneaker_sizes(key: str | None, value: dict):
    try:
        event_type = value.get("event_type")
        async with db_helper.session_context() as session:
            if event_type == "sneaker_sizes_created":
                data = value.get("data")
                sneaker_sizes_create = SneakerSizesCreate(**data)
                await create_sneaker_sizes(session, int(key), sneaker_sizes_create)
            elif event_type == "sneaker_sizes_updated":
                data = value.get("data")
                sneaker_sizes_update = SneakerSizeUpdate(**data)
                await update_sneaker_sizes(session, int(key), sneaker_sizes_update)
            elif event_type == "sneaker_sizes_deleted":
                data = value.get("data")
                sneaker_assoc_delete = SneakerAssocsDelete(**data)
                await delete_sneaker_association(
                    session,
                    int(key),
                    sneaker_assoc_delete,
                    SneakerSizeAssociation,
                    "size_id",
                )
    except Exception as e:
        print("Ошибка: ", e)
