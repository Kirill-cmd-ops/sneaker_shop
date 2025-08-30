from typing import Type

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from catalog_service.catalog.models import Base
from catalog_service.catalog.schemas.sneaker_association import (
    SneakerAssocsDelete,
)

async def delete_sneaker_association(
    session: AsyncSession,
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
        .where(sneaker_association_model.sneaker_id == sneaker_assoc_delete.sneaker_id)
        .where(field.in_(sneaker_assoc_delete.assoc_ids))
    )
    result = await session.execute(stmt)

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404, detail="Ничего не найдено по вашим параметрам"
        )

    await session.commit()

async def read_sneaker_association(
    session: AsyncSession,
    sneaker_association_model: Type[Base],
    sneaker_id: int,
):
    """
    Функция для чтения записи в ассоциативных таблицах
    """
    stmt = select(sneaker_association_model).where(
        sneaker_association_model.sneaker_id == sneaker_id
    )
    result = await session.execute(stmt)
    sneaker_associations = result.scalars().all()
    return sneaker_associations