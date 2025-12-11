from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.models import Favorite


async def check_favorite_exists(
    session: AsyncSession,
    user_id: int,
):
    stmt = select(Favorite.id).filter(Favorite.user_id == user_id)
    result = await session.execute(stmt)
    favorite_id = result.scalar_one_or_none()
    if not favorite_id:
        raise HTTPException(status_code=404, detail="Избранное пользователя не найдена")
    return favorite_id
