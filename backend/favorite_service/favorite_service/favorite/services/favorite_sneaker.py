from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.models import (
    Favorite,
    FavoriteSneakerAssociation,
    SneakerSizeAssociation,
)


async def create_sneaker_to_favorite(
    session: AsyncSession,
    favorite_id: int,
    sneaker_id: int,
    size_id: int,
):
    new_sneaker = FavoriteSneakerAssociation(
        favorite_id=favorite_id,
        sneaker_id=sneaker_id,
        size_id=size_id,
    )
    session.add(new_sneaker)
    return new_sneaker


async def update_sneaker_to_favorite(
    session: AsyncSession, favorite_sneaker_id: int, size_id: int
) -> FavoriteSneakerAssociation:
    request_get_sneaker = select(FavoriteSneakerAssociation).where(
        FavoriteSneakerAssociation.id == favorite_sneaker_id
    )
    result = await session.execute(request_get_sneaker)
    current_sneaker = result.scalar()
    if not current_sneaker.sneaker_id:
        raise HTTPException(status_code=404, detail="Элемент корзины не найден")

    request_get_sneaker_sizes = select(SneakerSizeAssociation.size_id).where(
        SneakerSizeAssociation.sneaker_id == current_sneaker.sneaker_id
    )
    result_sneaker_sizes = await session.execute(request_get_sneaker_sizes)
    allowed_sneaker_sizes = result_sneaker_sizes.scalars().all()

    if size_id in allowed_sneaker_sizes:
        current_sneaker.size_id = size_id
    else:
        raise HTTPException(
            status_code=404, detail="У данной модели кроссовок этот размер отсутствует"
        )

    return current_sneaker


async def delete_sneaker_to_favorite(
    session: AsyncSession,
    user_id: int,
    favorite_sneaker_id: int,
):
    stmt = delete(FavoriteSneakerAssociation).where(
        FavoriteSneakerAssociation.id == favorite_sneaker_id,
        FavoriteSneakerAssociation.favorite_id.in_(
            select(Favorite.id).where(Favorite.user_id == user_id)
        ),
    )
    result = await session.execute(stmt)

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Объект избранного не найден")
