from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.favorite_service.favorite_service.favorite.models import db_helper
from favorite_service.favorite.dependencies.get_current_user import get_current_user
from favorite_service.favorite.services.favorite import read_favorite, create_favorite

router = APIRouter()


@router.post("/favorite")
async def call_create_favorite(
    user: str = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await create_favorite(session, user_id=user.id)


@router.get("/favorite")
async def call_get_favorite(
    user: str = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    items = await read_favorite(session, user_id=user.id)
    return items
