from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.config import settings
from stock_notification_service.stock_notification.enums import SubscriptionStatus
from stock_notification_service.stock_notification.models import (
    Sneaker,
    SneakerSizeAssociation,
)
from stock_notification_service.stock_notification.schemas import SneakerSizeUpdate
from stock_notification_service.stock_notification.services.subscription.one_time.fetch import \
    get_sneaker_active_one_time_subscriptions
from stock_notification_service.stock_notification.services.subscription.permanent.fetch import \
    get_sneaker_active_subscriptions

from stock_notification_service.stock_notification.celery_tasks.update_tasks import (
    handle_update_quantity,
)


async def update_sneaker_sizes(
    session: AsyncSession, sneaker_id: int, sneaker_size_update: SneakerSizeUpdate
):
    stmt = (
        select(SneakerSizeAssociation)
        .where(SneakerSizeAssociation.sneaker_id == sneaker_id)
        .where(SneakerSizeAssociation.size_id == sneaker_size_update.size.size_id)
    )
    result = await session.execute(stmt)
    sneaker_size = result.scalar_one()

    sneaker_size_quantity_old = sneaker_size.quantity
    sneaker_size_quantity_new = sneaker_size_update.size.quantity

    sneaker_size.quantity = sneaker_size_update.size.quantity

    session.add(sneaker_size)
    await session.commit()

    if sneaker_size_quantity_old == 0 and sneaker_size_quantity_new > 0:
        subscribed_users = await get_subscribed_users(
            session,
            sneaker_id,
            sneaker_size_update.size.size_id,
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
