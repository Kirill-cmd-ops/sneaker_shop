from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.models import Favorite


async def delete_favorite(session: AsyncSession, user_id: int):
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    await session.execute(stmt)
    return {"Избранное пользователя было удалено успешно"}