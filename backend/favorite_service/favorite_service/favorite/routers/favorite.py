from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.config import settings

from favorite_service.favorite.models import db_helper
from favorite_service.favorite.dependencies.user_id import get_current_user_id
from favorite_service.favorite.dependencies.permissions import (
    check_role_permissions,
)
from favorite_service.favorite.services.favorite.delete import delete_favorite_service
from favorite_service.favorite.services.favorite.fetch import get_favorite_service

router = APIRouter(
    prefix=settings.api.build_path(settings.api.root, settings.api.v1.prefix),
    tags=["Favorite"],
)


@router.get(
    "/",
    dependencies=(Depends(check_role_permissions("favorite.view")),),
)
async def get_favorite(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        return await get_favorite_service(
            session=session,
            user_id=user_id,
        )


@router.delete(
    "/",
)
async def delete_favorite(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        return await delete_favorite_service(
            session=session,
            user_id=user_id,
        )
