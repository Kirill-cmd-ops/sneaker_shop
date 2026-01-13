from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from sneaker_details_service.sneaker_details.models import Sneaker


async def get_sneaker_service(
    session: AsyncSession,
    sneaker_id: int,
):
    stmt = (
        select(Sneaker)
        .where(Sneaker.id == sneaker_id)
        .where(Sneaker.is_active == True)
        .options(
            joinedload(Sneaker.brand),
            joinedload(Sneaker.country),
            selectinload(Sneaker.sizes),
            selectinload(Sneaker.colors),
            selectinload(Sneaker.materials),
        )
    )
    result = await session.execute(stmt)
    sneaker = result.unique().scalar_one_or_none()
    return sneaker
