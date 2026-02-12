from typing import Type

from sqlalchemy import delete

from microservices.stock_notification_service.stock_notification_service.stock_notification.models import Base, \
    db_helper


async def delete_sizes_from_sneaker_service(
        sneaker_id: int,
        assoc_ids: list[int],
        sneaker_association_model: Type[Base],
        field_name: str,
):
    """
    Функция для одаления записи в ассоциативной таблице
    """
    async with db_helper.session_context() as session:
        async with session.begin():
            field = getattr(sneaker_association_model, field_name)
            stmt = (
                delete(sneaker_association_model)
                .where(sneaker_association_model.sneaker_id == sneaker_id)
                .where(field.in_(assoc_ids))
            )
            await session.execute(stmt)
