from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.models import FavoriteSneakerAssociation
from favorite_service.favorite.schemas import FavoriteSneakerCreate


async def get_sneaker_in_favorite_service(
    session: AsyncSession,
    favorite_id: int,
    item_create: FavoriteSneakerCreate,
):
    return await session.scalar(
        select(FavoriteSneakerAssociation).where(
            FavoriteSneakerAssociation.favorite_id == favorite_id,
            FavoriteSneakerAssociation.sneaker_id == item_create.sneaker_id,
        )
    )
