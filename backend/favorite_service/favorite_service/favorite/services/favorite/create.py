from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.models import Favorite


async def create_favorite_service(session: AsyncSession, user_id: int):
    new_favorite = Favorite(user_id=user_id)
    session.add(new_favorite)
    await session.commit()
    await session.refresh(new_favorite)