from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, contains_eager

from sneaker_details_service.sneaker_details.models.sneaker import Sneaker

from sneaker_details_service.sneaker_details.models.sneaker_size import SneakerSizeAssociation


async def get_sneaker_details(
    session: AsyncSession,
    sneaker_id: int,
):
    stmt = (
        select(Sneaker)
        .join(Sneaker.size_associations)
        .join(SneakerSizeAssociation.size)
        .where(Sneaker.id == sneaker_id)
        .where(SneakerSizeAssociation.quantity > 0)
        .options(
            contains_eager(Sneaker.sizes),
            joinedload(Sneaker.brand),
            joinedload(Sneaker.country),
            selectinload(Sneaker.colors),
            selectinload(Sneaker.materials),
        )
    )
    result = await session.execute(stmt)
    sneaker = result.unique().scalar_one_or_none()
    return sneaker
