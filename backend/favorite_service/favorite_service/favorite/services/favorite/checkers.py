from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.models import Favorite


async def check_favorite_exists(
    session: AsyncSession,
    user_id: int,
):
    favorite_id = await session.scalar(
        select(Favorite.id).filter(Favorite.user_id == user_id)
    )
    if not favorite_id:
        raise HTTPException(status_code=404, detail="Избранное пользователя не найдена")
    return favorite_id
