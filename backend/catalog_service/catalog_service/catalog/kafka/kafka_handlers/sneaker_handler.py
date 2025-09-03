from catalog_service.catalog.models import db_helper
from catalog_service.catalog.schemas import SneakerCreate, SneakerUpdate
from catalog_service.catalog.services.sneakers import (
    create_sneaker,
    update_sneaker,
    delete_sneaker,
)


async def handle_sneaker(key: str | None, value: dict):
    try:
        event_type = value.get("event_type")
        async with db_helper.session_context() as session:
            if event_type == "sneaker_created":
                data = value.get("data")
                sneaker_create = SneakerCreate(**data)
                await create_sneaker(session, sneaker_create)

            elif event_type == "sneaker_updated":
                data = value.get("data")
                sneaker_id = value.get("sneaker_id")
                sneaker_update = SneakerUpdate(**data)
                await update_sneaker(session, sneaker_id, sneaker_update)

            else:
                sneaker_id = value.get("sneaker_id")
                await delete_sneaker(session, sneaker_id)
    except Exception as e:
        print("Ошибка:", e)
