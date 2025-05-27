from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.models import FavoriteSneakerAssociation


async def create_sneaker_to_favorite(
    session: AsyncSession,
    favorite_id: int,
    sneaker_id: int,
    sneaker_size: float,
):
    new_sneaker = FavoriteSneakerAssociation(
        favorite_id=favorite_id,
        sneaker_id=sneaker_id,
        sneaker_size=sneaker_size,
    )
    session.add(new_sneaker)
    await session.commit()
    await session.refresh(new_sneaker)
    return new_sneaker

async def delete_sneaker_to_favorite(
    session: AsyncSession, association_id: int
) -> None:
    current_sneaker = await session.get(FavoriteSneakerAssociation, association_id)
    if not current_sneaker:
        raise HTTPException(status_code=404, detail="Элемент избранного не найден")
    await session.delete(current_sneaker)
    await session.commit()
