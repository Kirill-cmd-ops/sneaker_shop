from typing import Type

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.models import Base
from sneaker_details_service.sneaker_details.schemas import SneakerAssocsCreate


async def create_sneaker_associations_service(
    session: AsyncSession,
    sneaker_id: int,
    sneaker_associations_create: SneakerAssocsCreate,
    sneaker_association_model: Type[Base],
    field_name: str,
):
    """
    Функция для создания записи в ассоциативных таблицах
    """
    sneaker_associations = [
        {
            "sneaker_id": sneaker_id,
            field_name: assoc_id,
        }
        for assoc_id in sneaker_associations_create.assoc_ids
    ]
    await session.execute(
        insert(sneaker_association_model).values(sneaker_associations)
    )
