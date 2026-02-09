from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from microservices.favorite_service.favorite_service.favorite.domain.exceptions import FavoriteNotFound
from microservices.favorite_service.favorite_service.favorite.models import Favorite


async def get_favorite_service(session: AsyncSession, user_id: int):
    favorite = await session.scalar(
        select(Favorite)
        .where(Favorite.user_id == user_id)
        .options(selectinload(Favorite.sneaker_associations))
    )

    if favorite is None:
        raise FavoriteNotFound()

    return favorite.sneaker_associations


async def get_user_favorite_id_service(
        session: AsyncSession,
        user_id: int,
):
    favorite_id = await session.scalar(
        select(Favorite.id).filter(Favorite.user_id == user_id)
    )
    if not favorite_id:
        raise FavoriteNotFound()

    return favorite_id
