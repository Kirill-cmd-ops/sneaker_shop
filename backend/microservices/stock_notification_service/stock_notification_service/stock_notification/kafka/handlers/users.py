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


async def handle_user_event(key: str | None, value: dict) -> None:
    event_type = value.get("event_type")
    if event_type == "user_created":
        data = value.get("data")
        user_create = UserCreate(**data)
        user_create_data = user_create.model_dump()
        await create_user_service(user_data=user_create_data)

    elif event_type == "user_updated":
        data = value.get("data")
        user_id = value.get("user_id")
        user_update = UserUpdate(**data)
        user_update_data = user_update.model_dump(exclude_unset=True)
        await update_user_service(
            user_id=user_id,
            user_data=user_update_data,
        )

    elif event_type == "user_deleted":
        user_id = value.get("user_id")
        await delete_user_service(
            user_id=user_id,
        )
