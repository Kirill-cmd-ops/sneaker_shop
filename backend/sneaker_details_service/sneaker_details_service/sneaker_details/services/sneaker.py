from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from sneaker_details_service.sneaker_details.models.sneaker import Sneaker


async def get_sneaker_details(
    session: AsyncSession,
    sneaker_id: int,
):
    stmt = (
        select(Sneaker)
        .options(
            joinedload(Sneaker.brand),
            selectinload(Sneaker.sizes),
            joinedload(Sneaker.country),
            selectinload(Sneaker.colors),
            selectinload(Sneaker.materials),
        )
        .where(Sneaker.id == sneaker_id)
    )
    result = await session.execute(stmt)
    sneaker = result.scalar_one_or_none()
    return sneaker
