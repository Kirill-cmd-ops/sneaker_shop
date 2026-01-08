from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.config import settings

from favorite_service.favorite.models import db_helper
from favorite_service.favorite.dependencies.get_current_user import get_user_by_header
from favorite_service.favorite.dependencies.check_permissions import (
    check_role_permissions,
)
from favorite_service.favorite.services.favorite.delete import delete_favorite
from favorite_service.favorite.services.favorite.fetch import read_favorite

router = APIRouter(
    prefix=settings.api.build_path(settings.api.root, settings.api.v1.prefix),
    tags=["Favorite"],
)


@router.get(
    "/",
    dependencies=(Depends(check_role_permissions("favorite.view")),),
)
async def call_get_favorite(
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        return await read_favorite(
            session=session,
            user_id=user_id,
        )


@router.delete(
    "/",
)
async def call_delete_favorite(
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        return await delete_favorite(
            session=session,
            user_id=user_id,
        )
