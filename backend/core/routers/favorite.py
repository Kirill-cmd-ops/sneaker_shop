from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.auth.authentication.fastapi_users import fastapi_users

from backend.auth_servicee import User
from backend.core.services.favorite import read_favorite, create_favorite
from backend.auth_servicee import db_helper
from backend.core.schemas.sneaker import SneakerOut

router = APIRouter()


@router.post("/favorite")
async def call_create_favorite(
    user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await create_favorite(session, user_id=user.id)


@router.get("/favorite", response_model=list[SneakerOut])
async def call_get_cart(
    user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    items = await read_favorite(session, user_id=user.id)
    return items
