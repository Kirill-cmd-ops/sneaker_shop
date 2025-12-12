from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.models import Favorite, FavoriteSneakerAssociation


async def create_sneaker_to_favorite(
    session: AsyncSession,
    favorite_id: int,
    sneaker_id: int,
):
    new_sneaker = FavoriteSneakerAssociation(
        favorite_id=favorite_id,
        sneaker_id=sneaker_id,
    )
    session.add(new_sneaker)

    return new_sneaker


async def delete_sneaker_to_favorite(
    session: AsyncSession,
    user_id: int,
    favorite_sneaker_id: int,
):
    stmt = (
        delete(FavoriteSneakerAssociation)
        .where(
            FavoriteSneakerAssociation.id == favorite_sneaker_id,
            FavoriteSneakerAssociation.favorite_id.in_(
                select(Favorite.id).where(Favorite.user_id == user_id)
            )
        )
    )
    result = await session.execute(stmt)

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Объект избранного не найден")
