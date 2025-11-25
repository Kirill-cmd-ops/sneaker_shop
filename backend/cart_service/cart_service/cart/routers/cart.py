from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.config import settings
from cart_service.cart.models import db_helper
from cart_service.cart.dependencies.get_current_user import get_user_by_header
from cart_service.cart.services.cart import read_cart
from cart_service.cart.services.check_permissions import check_role_permissions
from cart_service.cart.services.total_price import calculate_total_price


router = APIRouter(
    prefix=settings.api.build_path(settings.api.root, settings.api.v1.prefix),
    tags=["Cart"],
)


@router.get(
    "/view/",
    dependencies=(Depends(check_role_permissions("cart.view")),),
)
async def call_get_cart(
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    items = await read_cart(session, user_id=user_id)

    total_price = calculate_total_price(items)

    return {"Цена корзины: ": total_price, "Кроссовки": items}
