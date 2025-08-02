from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.config import settings
from favorite_service.favorite.models.db_helper import db_helper
from favorite_service.favorite.dependencies.get_current_user import get_user_by_header
from favorite_service.favorite.services.favorite import read_favorite, create_favorite

router = APIRouter(
    prefix=settings.api.v1.favorite,
    tags=["Favorite"],
)


@router.get("/favorite")
async def call_get_favorite(
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    items = await read_favorite(session, user_id=user_id)
    return items
