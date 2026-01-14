from stock_notification_service.stock_notification.models import db_helper
from stock_notification_service.stock_notification.services.subscription.one_time.deactivate_bulk import (
    deactivate_all_one_time_subscriptions_for_sneaker_service,
)
from stock_notification_service.stock_notification.services.subscription.one_time.reactivate_bulk import (
    reactivate_all_one_time_subscriptions_for_sneaker_service,
)
from stock_notification_service.stock_notification.services.subscription.permanent.deactivate_bulk import (
    deactivate_all_permanent_subscriptions_for_sneaker_service,
)
from stock_notification_service.stock_notification.services.subscription.permanent.reactivate_bulk import (
    reactivate_all_permanent_subscriptions_for_sneaker_service,
)


async def handle_sneaker_active_event(key: str | None, value: dict):
    try:
        event_type = value.get("event_type")
        async with db_helper.session_context() as session:
            if event_type == "sneaker_updated":
                sneaker_id = value.get("sneaker_id")
                data = value.get("data")
                if data["is_active"] is False:
                    await deactivate_all_permanent_subscriptions_for_sneaker_service(
                        session=session,
                        sneaker_id=sneaker_id,
                    )
                    await deactivate_all_one_time_subscriptions_for_sneaker_service(
                        session=session,
                        sneaker_id=sneaker_id,
                    )
                elif data["is_active"] is True:
                    await reactivate_all_permanent_subscriptions_for_sneaker_service(
                        session=session,
                        sneaker_id=sneaker_id,
                    )
                    await reactivate_all_one_time_subscriptions_for_sneaker_service(
                        session=session,
                        sneaker_id=sneaker_id,
                    )
    except Exception as e:
        print("Ошибка:", e)
