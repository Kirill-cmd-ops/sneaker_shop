from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.models import Base


async def read_sneaker_association(
    session: AsyncSession,
    sneaker_association_model: Type[Base],
    sneaker_id: int,
):
    """
    Функция для чтения записи в ассоциативных таблицах
    """
    result = await session.scalars(
        select(sneaker_association_model).where(
            sneaker_association_model.sneaker_id == sneaker_id
        )
    )
    return result.all()
