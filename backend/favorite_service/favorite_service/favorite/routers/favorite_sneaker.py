from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from favorite_service.favorite.models import db_helper, Favorite
from favorite_service.favorite.schemas import FavoriteSneakerCreate
from favorite_service.favorite.services.check_permissions import check_role_permissions
from favorite_service.favorite.services.favorite_sneaker import (
    create_sneaker_to_favorite,
    delete_sneaker_to_favorite,
)
from favorite_service.favorite.dependencies.get_current_user import get_user_by_header
from favorite_service.favorite.config import settings

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root, settings.api.v1.prefix, settings.api.v1.sneaker
    ),
    tags=["Favorite Sneaker"],
)


@router.post(
    "/add/",
    response_model=dict,
    dependencies=(Depends(check_role_permissions("favorite.sneaker.add")),),
)
async def call_create_sneaker_to_favorite(
    item: FavoriteSneakerCreate,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    stmt = select(Favorite).filter(Favorite.user_id == user_id)
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


@router.delete(
    "/delete/{sneaker_id}",
    response_model=dict,
    dependencies=(Depends(check_role_permissions("favorite.sneaker.delete")),),
)
async def call_delete_sneaker_to_favorite(
    sneaker_id: int,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await delete_sneaker_to_favorite(session, user_id=user_id, sneaker_id=sneaker_id)
    return {"status": "Элемент удалён"}
