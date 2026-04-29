from typing import Any, Type

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.domain.exceptions import \
    SneakerAssociationAlreadyExists
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import Base


async def create_sneaker_associations_service(
        session: AsyncSession,
        sneaker_id: int,
        assoc_ids: list[int],
        sneaker_association_model: Type[Base],
        field_name: str,
) -> list[Any]:
    """
    Функция для создания записи в ассоциативных таблицах.
    Возвращает строки связей для этого sneaker и переданных id (после вставки).
    """
    if not assoc_ids:
        return []

    try:
        sneaker_associations = [
            {
                "sneaker_id": sneaker_id,
                field_name: assoc_id,
            }
            for assoc_id in assoc_ids
        ]
        async with session.begin():
            await session.execute(
                insert(sneaker_association_model).values(sneaker_associations)
            )
            fk_column = getattr(sneaker_association_model, field_name)
            stmt = select(sneaker_association_model).where(
                sneaker_association_model.sneaker_id == sneaker_id,
                fk_column.in_(assoc_ids),
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())
    except IntegrityError:
        raise SneakerAssociationAlreadyExists()
