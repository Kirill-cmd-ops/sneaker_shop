from typing import Type

from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.models import Base, SneakerColorAssociation
from sneaker_details_service.sneaker_details.schemas.sneaker_association import (
    SneakerAssocsCreate,
    SneakerAssocsDelete,
)


async def create_sneaker_association(
    session: AsyncSession,
    sneaker_associations_create: SneakerAssocsCreate,
    sneaker_association_model: Type[Base],
    field_name: str,
):
    """
    Функция для создания записи в ассоциативных таблицах
    """
    for assoc_id in sneaker_associations_create.assoc_ids:
        assoc_data = {
            "sneaker_id": sneaker_associations_create.sneaker_id,
            field_name: assoc_id,
        }

        sneaker_association = sneaker_association_model(**assoc_data)
        session.add(sneaker_association)
    await session.commit()


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
