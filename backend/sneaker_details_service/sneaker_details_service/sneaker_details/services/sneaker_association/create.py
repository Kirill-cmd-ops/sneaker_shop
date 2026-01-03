from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.models import Base
from sneaker_details_service.sneaker_details.schemas import SneakerAssocsCreate


async def create_sneaker_association(
    session: AsyncSession,
    sneaker_id: int,
    sneaker_associations_create: SneakerAssocsCreate,
    sneaker_association_model: Type[Base],
    field_name: str,
):
    """
    Функция для создания записи в ассоциативных таблицах
    """
    for assoc_id in sneaker_associations_create.assoc_ids:
        assoc_data = {
            "sneaker_id": sneaker_id,
            field_name: assoc_id,
        }

        sneaker_association = sneaker_association_model(**assoc_data)
        session.add(sneaker_association)