from stock_notification_service.stock_notification.services.subscription.orchestrators import (
    deactivate_all_subscriptions_for_sneaker_orchestrator,
    reactivate_all_subscriptions_for_sneaker_orchestrator,
)


async def handle_sneaker_active_event(key: str | None, value: dict):
    try:
        event_type = value.get("event_type")
        if event_type == "sneaker_updated":
            sneaker_id = value.get("sneaker_id")
            data = value.get("data")
            if data["is_active"] is False:
                await deactivate_all_subscriptions_for_sneaker_orchestrator(
                    sneaker_id=sneaker_id,
                )
            elif data["is_active"] is True:
                await reactivate_all_subscriptions_for_sneaker_orchestrator(
                    sneaker_id=sneaker_id,
                )
    except Exception as e:
        print("Ошибка:", e)
