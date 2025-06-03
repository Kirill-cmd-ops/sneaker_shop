from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.config import settings
from cart_service.cart.models import db_helper
from cart_service.cart.dependencies.get_current_user import get_current_user
from cart_service.cart.services.cart import read_cart, create_cart

router = APIRouter(
    prefix=settings.api.v1.cart,
    tags=["Cart"],
)


@router.post("/cart")
async def call_create_cart(
    user: str = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await create_cart(session, user_id=user.id)


@router.get("/cart")
async def call_get_cart(
    user: str = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    items = await read_cart(session, user_id=user.id)
    return items
