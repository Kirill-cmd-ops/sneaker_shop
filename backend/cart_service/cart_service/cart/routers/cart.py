from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.auth.authentication.fastapi_users import fastapi_users

from backend.auth_servicee import User
from backend.cart_service.cart_service.cart.services.cart import read_cart, create_cart
from backend.auth_servicee import db_helper
from backend.core.schemas.sneaker import SneakerOut

router = APIRouter()


@router.post("/cart")
async def call_create_cart(
    user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await create_cart(session, user_id=user.id)


@router.get("/cart", response_model=list[SneakerOut])
async def call_get_cart(
    user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    items = await read_cart(session, user_id=user.id)
    return items
