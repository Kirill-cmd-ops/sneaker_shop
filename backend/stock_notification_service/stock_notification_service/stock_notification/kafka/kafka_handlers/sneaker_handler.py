from stock_notification_service.stock_notification.models import db_helper
from stock_notification_service.stock_notification.schemas import (
    SneakerCreate,
    SneakerUpdate,
)
from stock_notification_service.stock_notification.services.sneaker.create import create_sneaker
from stock_notification_service.stock_notification.services.sneaker.delete import delete_sneaker
from stock_notification_service.stock_notification.services.sneaker.update import update_sneaker


async def handle_sneaker(key: str | None, value: dict):
    try:
        event_type = value.get("event_type")
        async with db_helper.session_context() as session:
            if event_type == "sneaker_created":
                data = value.get("data")
                sneaker_create = SneakerCreate.model_validate(data, strict=False)
                await create_sneaker(session, sneaker_create)

            elif event_type == "sneaker_updated":
                data = value.get("data")
                sneaker_id = value.get("sneaker_id")
                sneaker_update = SneakerUpdate.model_validate(data, strict=False)
                await update_sneaker(session, sneaker_id, sneaker_update)

            elif event_type == "sneaker_deleted":
                sneaker_id = value.get("sneaker_id")
                await delete_sneaker(session, sneaker_id)
    except Exception as e:
        print("Ошибка:", e)
