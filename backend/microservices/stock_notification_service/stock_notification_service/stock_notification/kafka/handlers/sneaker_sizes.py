from microservices.stock_notification_service.stock_notification_service.stock_notification.models import \
    SneakerSizeAssociation
from microservices.stock_notification_service.stock_notification_service.stock_notification.schemas import (
    SneakerSizesCreate,
    SneakerSizeUpdate,
    SneakerAssocsDelete,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.sneaker_size.create import (
    add_sizes_to_sneaker_service,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.sneaker_size.delete import (
    delete_sizes_from_sneaker_service,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.sneaker_size.orchestrators import (
    update_sneaker_size_quantity_with_notifications_orchestrator,
)


async def handle_sneaker_sizes_event(key: str | None, value: dict) -> None:
    event_type = value.get("event_type")
    if event_type == "sneaker_sizes_created":
        data = value.get("data")
        sneaker_sizes_create = SneakerSizesCreate(**data)
        size_list = [size.model_dump() for size in sneaker_sizes_create.sizes]

        await add_sizes_to_sneaker_service(
            sneaker_id=int(key),
            size_list=size_list,
        )
    elif event_type == "sneaker_sizes_updated":
        data = value.get("data")
        sneaker_size_update = SneakerSizeUpdate(**data)

        size_id = sneaker_size_update.size.size_id
        quantity = sneaker_size_update.size.quantity

        await update_sneaker_size_quantity_with_notifications_orchestrator(
            sneaker_id=int(key),
            size_id=size_id,
            quantity=quantity,

        )
    elif event_type == "sneaker_sizes_deleted":
        data = value.get("data")
        sneaker_assoc_delete = SneakerAssocsDelete(**data)
        size_ids = sneaker_assoc_delete.assoc_ids

        await delete_sizes_from_sneaker_service(
            sneaker_id=int(key),
            assoc_ids=size_ids,
            sneaker_association_model=SneakerSizeAssociation,
            field_name="size_id",
        )
