from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.favorite_service.favorite_service.favorite.models import FavoriteSneakerAssociation


async def get_sneaker_in_favorite_service(
        session: AsyncSession,
        favorite_id: int,
        sneaker_id: int,
):
    return await session.scalar(
        select(FavoriteSneakerAssociation).where(
            FavoriteSneakerAssociation.favorite_id == favorite_id,
            FavoriteSneakerAssociation.sneaker_id == sneaker_id,
        )
    )
