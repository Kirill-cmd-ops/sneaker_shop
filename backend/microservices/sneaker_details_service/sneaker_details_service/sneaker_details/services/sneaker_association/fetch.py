from typing import Type, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import Base


async def get_sneaker_associations_service(
        session: AsyncSession,
        sneaker_association_model: Type[Base],
        sneaker_id: int,
) -> Sequence[DeclarativeBase]:
    """
    Функция для чтения записи в ассоциативных таблицах
    """
    async with session.begin():
        result = await session.scalars(
            select(sneaker_association_model).where(
                sneaker_association_model.sneaker_id == sneaker_id
            )
        )
    return result.all()
