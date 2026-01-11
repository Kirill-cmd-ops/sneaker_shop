from catalog_service.catalog.models import db_helper, SneakerSizeAssociation
from catalog_service.catalog.schemas import (
    SneakerSizesCreate,
    SneakerSizeUpdate,
    SneakerAssocsDelete,
)
from catalog_service.catalog.services.sneaker_association.delete import (
    delete_sneaker_associations_service,
)
from catalog_service.catalog.services.sneaker_size.create import (
    add_sizes_to_sneaker_service,
)
from catalog_service.catalog.services.sneaker_size.update import (
    update_sneaker_size_quantity_service,
)


async def handle_sneaker_sizes_event(key: str | None, value: dict):
    try:
        event_type = value.get("event_type")
        async with db_helper.session_context() as session:
            if event_type == "sneaker_sizes_created":
                data = value.get("data")
                sneaker_sizes_create = SneakerSizesCreate(**data)
                await add_sizes_to_sneaker_service(
                    session=session,
                    sneaker_id=int(key),
                    sneaker_sizes_create=sneaker_sizes_create,
                )
            elif event_type == "sneaker_sizes_updated":
                data = value.get("data")
                sneaker_sizes_update = SneakerSizeUpdate(**data)
                await update_sneaker_size_quantity_service(
                    session=session,
                    sneaker_id=int(key),
                    sneaker_size_update=sneaker_sizes_update,
                )
            elif event_type == "sneaker_sizes_deleted":
                data = value.get("data")
                sneaker_assoc_delete = SneakerAssocsDelete(**data)
                await delete_sneaker_associations_service(
                    session=session,
                    sneaker_id=int(key),
                    sneaker_assoc_delete=sneaker_assoc_delete,
                    sneaker_association_model=SneakerSizeAssociation,
                    field_name="size_id",
                )
    except Exception as e:
        print("Ошибка: ", e)
