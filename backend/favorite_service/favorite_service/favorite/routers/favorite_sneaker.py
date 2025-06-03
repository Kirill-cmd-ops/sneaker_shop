from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from favorite_service.favorite.models import db_helper
from favorite_service.favorite.schemas.favorite_sneaker import FavoriteSneakerCreate
from favorite_service.favorite.services.favorite_sneaker import (
    create_sneaker_to_favorite,
    delete_sneaker_to_favorite,
)
from favorite_service.favorite.models import Favorite
from favorite_service.favorite.dependencies.get_current_user import get_current_user
from favorite_service.favorite.config import settings

router = APIRouter(
    prefix=settings.api.v1.favorite_sneaker,
    tags=["Favorite Sneaker"],
)


@router.post("/favorite_add/", response_model=dict)
async def call_create_sneaker_to_favorite(
    item: FavoriteSneakerCreate,
    user: str = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    stmt = select(Favorite).filter(Favorite.user_id == user.id)
    result = await session.execute(stmt)
    user_favorite = result.scalar_one_or_none()
    if not user_favorite:
        raise HTTPException(status_code=404, detail="Избранное пользователя не найдена")

    new_item = await create_sneaker_to_favorite(
        session,
        favorite_id=user_favorite.id,
        sneaker_id=item.sneaker_id,
    )
    return {"status": "Элемент добавлен", "item_id": new_item.id}

@router.delete("/favorite_delete/{sneaker_id}", response_model=dict)
async def call_delete_sneaker_to_favorite(
    sneaker_id: int,
    user: str = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await delete_sneaker_to_favorite(session, user_id=user.id, sneaker_id=sneaker_id)
    return {"status": "Элемент удалён"}
