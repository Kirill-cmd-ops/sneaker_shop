from typing import Type

from sqlalchemy import delete

from microservices.cart_service.cart_service.cart.models import Base, db_helper


async def delete_sneaker_associations_service(
        sneaker_id: int,
        assoc_ids: list[int],
        sneaker_association_model: Type[Base],
        field_name: str,
) -> None:
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

