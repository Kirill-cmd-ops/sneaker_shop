from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.favorite_service.favorite_service.favorite.models import (
    FavoriteSneakerAssociation,
    Favorite,
    SneakerSizeAssociation,
)


async def update_sneaker_in_favorite_service(
        session: AsyncSession,
        favorite_sneaker_id: int,
        size_id: int,
        user_id: int,
) -> FavoriteSneakerAssociation:
    async with session.begin():
        current_sneaker = await session.scalar(
            select(FavoriteSneakerAssociation).where(
                FavoriteSneakerAssociation.id == favorite_sneaker_id,
                FavoriteSneakerAssociation.favorite_id.in_(
                    select(Favorite.id).where(Favorite.user_id == user_id),
                ),
            )
        )

        result_sneaker_sizes = await session.scalars(
            select(SneakerSizeAssociation.size_id).where(
                SneakerSizeAssociation.sneaker_id == current_sneaker.sneaker_id
            )
        )
        allowed_sneaker_sizes = result_sneaker_sizes.all()

        if size_id in allowed_sneaker_sizes:
            current_sneaker.size_id = size_id
        else:
            raise HTTPException(
                status_code=404, detail="У данной модели кроссовок этот размер отсутствует"
            )

    return current_sneaker
