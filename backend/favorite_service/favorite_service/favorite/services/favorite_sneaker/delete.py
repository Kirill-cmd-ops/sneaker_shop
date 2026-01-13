from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.models import FavoriteSneakerAssociation, Favorite


async def delete_sneaker_from_favorite_service(
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
