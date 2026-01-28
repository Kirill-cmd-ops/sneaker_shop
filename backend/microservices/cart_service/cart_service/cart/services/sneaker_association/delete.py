from typing import Type

from fastapi import HTTPException
from sqlalchemy import delete

from microservices.cart_service.cart_service.cart.models import Base, db_helper
from microservices.cart_service.cart_service.cart.schemas import SneakerAssocsDelete


async def delete_sneaker_associations_service(
        sneaker_id: int,
        sneaker_assoc_delete: SneakerAssocsDelete,
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
                .where(field.in_(sneaker_assoc_delete.assoc_ids))
            )
            result = await session.execute(stmt)

            if result.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Ничего не найдено по вашим параметрам"
                )
