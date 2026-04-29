from typing import Any, Dict

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.domain.exceptions import (
    SneakerSizeAlreadyExists,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import SneakerSizeAssociation


async def add_sizes_to_sneaker_service(
        session: AsyncSession,
        sneaker_id: int,
        size_list: list[Dict[str, Any]],
) -> list[Any]:
    """
    Вставляет связи размеров и возвращает созданные строки (после SELECT по sneaker_id и size_id).
    """
    if not size_list:
        return []

    try:
        sneaker_sizes = [
            {
                "sneaker_id": sneaker_id,
                "size_id": size_data["size_id"],
                "quantity": size_data["quantity"],
            }
            for size_data in size_list
        ]
        size_ids = [size_data["size_id"] for size_data in size_list]

        async with session.begin():
            await session.execute(insert(SneakerSizeAssociation).values(sneaker_sizes))
            stmt = select(SneakerSizeAssociation).where(
                SneakerSizeAssociation.sneaker_id == sneaker_id,
                SneakerSizeAssociation.size_id.in_(size_ids),
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())
    except IntegrityError:
        raise SneakerSizeAlreadyExists()
