from cart_service.cart.models import db_helper
from cart_service.cart.schemas import SneakerCreate, SneakerUpdate
from cart_service.cart.services.sneaker.create import create_sneaker_service
from cart_service.cart.services.sneaker.delete import delete_sneaker_service
from cart_service.cart.services.sneaker.update import update_sneaker_service


async def handle_sneaker_event(key: str | None, value: dict):
    try:
        event_type = value.get("event_type")
        if event_type == "sneaker_created":
            data = value.get("data")
            sneaker_create = SneakerCreate(**data)
            await create_sneaker_service(sneaker_create=sneaker_create)

        elif event_type == "sneaker_updated":
            data = value.get("data")
            sneaker_id = value.get("sneaker_id")
            sneaker_update = SneakerUpdate(**data)
            await update_sneaker_service(
                sneaker_id=sneaker_id,
                sneaker_update=sneaker_update,
            )

        elif event_type == "sneaker_deleted":
            sneaker_id = value.get("sneaker_id")
            await delete_sneaker_service(sneaker_id=sneaker_id)
    except Exception as e:
        print("Ошибка:", e)
