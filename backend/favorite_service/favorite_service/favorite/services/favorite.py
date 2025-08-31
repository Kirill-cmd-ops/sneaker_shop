from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from favorite_service.favorite.models import Favorite


async def create_favorite(session: AsyncSession, user_id: int):
    new_favorite = Favorite(user_id=user_id)
    session.add(new_favorite)
    await session.commit()
    await session.refresh(new_favorite)

async def read_favorite(session: AsyncSession, user_id: int):
    stmt = select(Favorite).where(Favorite.user_id == user_id).options(selectinload(Favorite.sneaker_associations))
    result = await session.execute(stmt)
    favorite = result.scalar_one_or_none()
    if favorite is None:
        raise HTTPException(
            status_code=404, detail="У данного пользователя нету избранного"
        )

    return favorite.sneaker_associations
