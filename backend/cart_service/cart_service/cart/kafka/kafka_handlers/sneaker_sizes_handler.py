from cart_service.cart.models import db_helper, SneakerSizeAssociation
from cart_service.cart.schemas import (
    SneakerSizesCreate,
    SneakerSizeUpdate,
    SneakerAssocsDelete,
)
from cart_service.cart.services.sneaker_association import (
    delete_sneaker_association,
)
from cart_service.cart.services.sneaker_sizes import (
    create_sneaker_sizes,
    update_sneaker_sizes,
)


async def handle_sneaker_sizes(key: str | None, value: dict):
    try:
        event_type = value.get("event_type")
        async with db_helper.session_context() as session:
            if event_type == "sneaker_sizes_created":
                data = value.get("data")
                sneaker_sizes_create = SneakerSizesCreate(**data)
                await create_sneaker_sizes(session, sneaker_sizes_create)
            elif event_type == "sneaker_sizes_updated":
                data = value.get("data")
                sneaker_sizes_update = SneakerSizeUpdate(**data)
                await update_sneaker_sizes(session, sneaker_sizes_update)
            else:
                data = value.get("data")
                sneaker_assoc_delete = SneakerAssocsDelete(**data)
                await delete_sneaker_association(
                    session, sneaker_assoc_delete, SneakerSizeAssociation, "size_id"
                )
    except Exception as e:
        print("Ошибка: ", e)
