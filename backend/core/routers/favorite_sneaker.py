from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from auth_service.auth.authentication.fastapi_users import fastapi_users
from backend.auth_servicee import User
from backend.auth_servicee import db_helper
from backend.core.schemas.favorite_sneaker import FavoriteSneakerCreate
from backend.core.services.favorite_sneaker import (
    create_sneaker_to_favorite,
    delete_sneaker_to_favorite,
)
from backend.core.models import Favorite

router = APIRouter()


@router.post("/favorite_add/", response_model=dict)
async def call_create_sneaker_to_favorite(
    item: FavoriteSneakerCreate,
    user: User = Depends(fastapi_users.current_user()),
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
    user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await delete_sneaker_to_favorite(session, user_id=user.id, sneaker_id=sneaker_id)
    return {"status": "Элемент удалён"}
