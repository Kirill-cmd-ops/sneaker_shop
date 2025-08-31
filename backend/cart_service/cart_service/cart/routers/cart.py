from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.config import settings
from cart_service.cart.models import db_helper
from cart_service.cart.dependencies.get_current_user import get_user_by_header
from cart_service.cart.services.cart import read_cart

router = APIRouter(
    prefix=settings.api.v1.cart,
    tags=["Cart"],
)


@router.get("/cart")
async def call_get_cart(
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    items = await read_cart(session, user_id=user_id)
    return items
