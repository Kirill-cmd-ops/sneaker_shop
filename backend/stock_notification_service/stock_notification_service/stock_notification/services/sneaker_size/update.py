from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.config import settings
from stock_notification_service.stock_notification.models import (
    SneakerSizeAssociation,
)
from stock_notification_service.stock_notification.schemas import SneakerSizeUpdate

from stock_notification_service.stock_notification.celery_tasks.update_tasks import (
    handle_update_quantity,
)
from stock_notification_service.stock_notification.services.subscription.one_time.fetch import \
    get_active_one_time_subscriptions_for_sneaker_service
from stock_notification_service.stock_notification.services.subscription.permanent.fetch import \
    get_active_permanent_subscriptions_for_sneaker_service


async def update_sneaker_size_quantity_service(
    session: AsyncSession,
    sneaker_id: int,
    sneaker_size_update: SneakerSizeUpdate,
):
    sneaker_size = await session.scalar(
        select(SneakerSizeAssociation)
        .where(SneakerSizeAssociation.sneaker_id == sneaker_id)
        .where(SneakerSizeAssociation.size_id == sneaker_size_update.size.size_id)
    )

    sneaker_size_quantity_old = sneaker_size.quantity
    sneaker_size_quantity_new = sneaker_size_update.size.quantity

    sneaker_size.quantity = sneaker_size_update.size.quantity

    session.add(sneaker_size)
    await session.commit()

    if sneaker_size_quantity_old == 0 and sneaker_size_quantity_new > 0:
        subscribed_users = await get_active_permanent_subscriptions_for_sneaker_service(
            session=session,
            sneaker_id=sneaker_id,
            size_id=sneaker_size_update.size.size_id,
        )

        subscribed_users_one_time = await get_active_one_time_subscriptions_for_sneaker_service(
            session=session,
            sneaker_id=sneaker_id,
            size_id=sneaker_size_update.size.size_id,
        )

        for user_email in subscribed_users:
            handle_update_quantity.delay(
                hostname=settings.smtp_config.smtp_hostname,
                port=settings.smtp_config.smtp_port,
                start_tls=settings.smtp_config.smtp_start_tls,
                username=settings.smtp_config.smtp_username,
                password=settings.smtp_config.smtp_password,
                sender_gmail="Sneaker Shop <bondarenkokirill150208@gmail.com>",
                recipient_gmail=user_email,
                email_title="Уведомление о поступлении товара",
                body_title="Данная модель кроссовок поступила в наличие",
            )

        for user_email_one_time in subscribed_users_one_time:
            handle_update_quantity.delay(
                hostname=settings.smtp_config.smtp_hostname,
                port=settings.smtp_config.smtp_port,
                start_tls=settings.smtp_config.smtp_start_tls,
                username=settings.smtp_config.smtp_username,
                password=settings.smtp_config.smtp_password,
                sender_gmail="Sneaker Shop <bondarenkokirill150208@gmail.com>",
                recipient_gmail=user_email_one_time,
                email_title="Уведомление о поступлении товара",
                body_title="Данная модель кроссовок поступила в наличие",
            )


# TODO: доработать логику
