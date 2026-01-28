from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.cart_service.cart_service.cart.models import Base


async def get_sneaker_associations_service(
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
