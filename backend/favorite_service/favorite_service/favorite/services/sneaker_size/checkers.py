from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.models import Sneaker, SneakerSizeAssociation
from favorite_service.favorite.schemas import FavoriteSneakerCreate


async def check_sneaker_has_size_service(
    session: AsyncSession,
    item_create: FavoriteSneakerCreate,
):
    sneaker_size = await session.scalar(
        select(Sneaker)
        .join(SneakerSizeAssociation)
        .where(
            Sneaker.id == item_create.sneaker_id,
            SneakerSizeAssociation.size_id == item_create.size_id,
        )
    )

    if not sneaker_size:
        raise HTTPException(status_code=404, detail="Размер данной модели не найден")
