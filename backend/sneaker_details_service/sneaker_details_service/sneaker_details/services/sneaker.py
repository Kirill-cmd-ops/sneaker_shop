from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from backend.catalog_service.catalog_service.catalog.models import Sneaker


async def get_sneaker_details(
    session: AsyncSession,
    sneakerId: int,
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
        .where(Sneaker.id == sneakerId)
    )
    result = await session.execute(stmt)
    sneaker = result.scalar_one_or_none()
    return sneaker
