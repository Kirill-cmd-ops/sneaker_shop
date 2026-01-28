from microservices.stock_notification_service.stock_notification_service.stock_notification.schemas import (
    UserCreate,
    UserUpdate,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.user.create import (
    create_user_service,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.user.delete import (
    delete_user_service,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.user.update import (
    update_user_service,
)


async def handle_user_event(key: str | None, value: dict):
    try:
        event_type = value.get("event_type")
        if event_type == "user_created":
            data = value.get("data")
            user_create = UserCreate(**data)
            await create_user_service(user_create=user_create)

        elif event_type == "user_updated":
            data = value.get("data")
            user_id = value.get("user_id")
            user_update = UserUpdate(**data)
            await update_user_service(
                user_id=user_id,
                user_update=user_update,
            )

        elif event_type == "user_deleted":
            user_id = value.get("user_id")
            await delete_user_service(
                user_id=user_id,
            )
    except Exception as e:
        print("Ошибка:", e)
