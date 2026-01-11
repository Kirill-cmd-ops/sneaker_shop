from typing import Type

from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import Base
from cart_service.cart.schemas import SneakerAssocsDelete


async def delete_sneaker_associations_service(
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