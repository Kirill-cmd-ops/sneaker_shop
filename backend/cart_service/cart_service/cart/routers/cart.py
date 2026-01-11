from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.config import settings
from cart_service.cart.models import db_helper
from cart_service.cart.dependencies.user_id import get_current_user_id
from cart_service.cart.services.cart.delete import delete_cart_service
from cart_service.cart.services.cart.fetch import get_cart_service
from cart_service.cart.services.cart.price import get_cart_total_service

router = APIRouter(
    prefix=settings.api.build_path(settings.api.root, settings.api.v1.prefix),
    tags=["Cart"],
)


@router.get(
    "/",
)
async def get_cart(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        items = await get_cart_service(
            session=session,
            user_id=user_id,
        )

        total_price = get_cart_total_service(items=items)

        return {"Цена корзины: ": total_price, "Кроссовки": items}


@router.delete(
    "/",
)
async def delete_cart(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        return await delete_cart_service(
            session=session,
            user_id=user_id,
        )
