from fastapi import HTTPException
from sqlalchemy import select
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
    await session.commit()
    await session.refresh(new_sneaker)
    return new_sneaker


async def delete_sneaker_to_favorite(
    session: AsyncSession,
    user_id: int,
    sneaker_id: int,
) -> None:
    stmt = (
        select(FavoriteSneakerAssociation)
        .join(Favorite)
        .where(
            Favorite.user_id == user_id,
            FavoriteSneakerAssociation.sneaker_id == sneaker_id,
        )
    )
    result = await session.execute(stmt)
    association = result.scalar_one_or_none()

    if not association:
        raise HTTPException(status_code=404, detail="Объект избранного не найден")

    await session.delete(association)
    await session.commit()
