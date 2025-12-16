from typing import Type

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.config import settings
from stock_notification_service.stock_notification.models import (
    Base,
    SneakerSizeAssociation,
)
from stock_notification_service.stock_notification.schemas import (
    SneakerSizeUpdate,
    SneakerSizesCreate,
    SneakerAssocsDelete,
)
from stock_notification_service.stock_notification.services.subscribed_users import (
    get_subscribed_users,
)
from stock_notification_service.stock_notification.celery_tasks.update_tasks import (
    handle_update_quantity,
)


async def create_sneaker_sizes(
    session: AsyncSession, sneaker_id: int, sneaker_sizes_create: SneakerSizesCreate
):
    for size_data in sneaker_sizes_create.sizes:
        sneaker_size = SneakerSizeAssociation(
            sneaker_id=sneaker_id,
            size_id=size_data.size_id,
            quantity=size_data.quantity,
        )
        session.add(sneaker_size)
    await session.commit()


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


async def delete_sneaker_association(
    session: AsyncSession,
    sneaker_id: int,
    sneaker_assoc_delete: SneakerAssocsDelete,
    sneaker_association_model: Type[Base],
    field_name: str,
):
    """
    Функция для одаления записи в ассоциативной таблице
    """
    field = getattr(sneaker_association_model, field_name)
    stmt = (
        delete(sneaker_association_model)
        .where(sneaker_association_model.sneaker_id == sneaker_id)
        .where(field.in_(sneaker_assoc_delete.assoc_ids))
    )
    result = await session.execute(stmt)

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404, detail="Ничего не найдено по вашим параметрам"
        )

    await session.commit()
