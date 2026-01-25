from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.models import Sneaker
from favorite_service.favorite.schemas import FavoriteSneakerCreate


async def check_sneaker_exists_service(
    session: AsyncSession,
    sneaker_id: int,
):
    sneaker = await session.get(Sneaker, sneaker_id)
    if not sneaker:
        raise HTTPException(status_code=404, detail="Товар не найден в каталоге")
