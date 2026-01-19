from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from favorite_service.favorite.models import Favorite


async def get_favorite_service(session: AsyncSession, user_id: int):
    async with session.begin():
        favorite = await session.scalar(
            select(Favorite)
            .where(Favorite.user_id == user_id)
            .options(selectinload(Favorite.sneaker_associations))
        )

        if favorite is None:
            raise HTTPException(
                status_code=404, detail="У данного пользователя нету избранного"
            )

    return favorite.sneaker_associations


async def get_user_favorite_id_service(
    session: AsyncSession,
    user_id: int,
):
    favorite_id = await session.scalar(
        select(Favorite.id).filter(Favorite.user_id == user_id)
    )
    if not favorite_id:
        raise HTTPException(status_code=404, detail="Избранное пользователя не найдена")
    return favorite_id
