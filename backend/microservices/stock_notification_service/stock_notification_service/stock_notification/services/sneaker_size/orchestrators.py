from microservices.stock_notification_service.stock_notification_service.stock_notification.models import db_helper
from microservices.stock_notification_service.stock_notification_service.stock_notification.schemas import \
    SneakerSizeUpdate
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.sneaker_size.update import (
    update_sneaker_size_quantity_service,
    get_subscribed_emails,
    send_notification_for_subscribed_emails,
)


async def update_sneaker_size_quantity_with_notifications_orchestrator(
        sneaker_id: int,
        sneaker_size_update: SneakerSizeUpdate,
):
    async with db_helper.session_context() as session:
        async with session.begin():
            should_notify = await update_sneaker_size_quantity_service(
                session=session,
                sneaker_id=sneaker_id,
                sneaker_size_update=sneaker_size_update,
            )

            if should_notify:
                emails = await get_subscribed_emails(
                    session=session,
                    sneaker_id=sneaker_id,
                    sneaker_size_update=sneaker_size_update,
                )

    if emails:
        await send_notification_for_subscribed_emails(emails=emails)
