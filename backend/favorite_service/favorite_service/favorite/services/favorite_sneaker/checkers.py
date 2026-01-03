from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.models import FavoriteSneakerAssociation
from favorite_service.favorite.schemas import FavoriteSneakerCreate


async def check_sneaker_in_favorite_exists(
    session: AsyncSession,
    favorite_id: int,
    item_create: FavoriteSneakerCreate,
):
    stmt = select(FavoriteSneakerAssociation).where(
        FavoriteSneakerAssociation.favorite_id == favorite_id,
        FavoriteSneakerAssociation.sneaker_id == item_create.sneaker_id,
    )
    result = await session.execute(stmt)
    sneaker_record = result.scalar_one_or_none()
    return sneaker_record