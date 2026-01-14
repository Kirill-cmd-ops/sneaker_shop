from stock_notification_service.stock_notification.models import db_helper
from stock_notification_service.stock_notification.schemas import (
    UserCreate,
    UserUpdate,
)
from stock_notification_service.stock_notification.services.user.create import (
    create_user_service,
)
from stock_notification_service.stock_notification.services.user.delete import (
    delete_user_service,
)
from stock_notification_service.stock_notification.services.user.update import (
    update_user_service,
)


async def handle_user_event(key: str | None, value: dict):
    try:
        event_type = value.get("event_type")
        async with db_helper.session_context() as session:
            if event_type == "user_created":
                data = value.get("data")
                user_create = UserCreate.model_validate(obj=data, strict=False)
                await create_user_service(
                    session=session,
                    user_create=user_create,
                )

            elif event_type == "user_updated":
                data = value.get("data")
                user_id = value.get("user_id")
                user_update = UserUpdate.model_validate(obj=data, strict=False)
                await update_user_service(
                    session=session,
                    user_id=user_id,
                    user_update=user_update,
                )

            elif event_type == "user_deleted":
                user_id = value.get("user_id")
                await delete_user_service(
                    session=session,
                    user_id=user_id,
                )
    except Exception as e:
        print("Ошибка:", e)
