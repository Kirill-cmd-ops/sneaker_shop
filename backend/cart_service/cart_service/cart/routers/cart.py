from fastapi import APIRouter, Depends
from fastapi.params import Header
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.config import settings
from cart_service.cart.models import db_helper
from cart_service.cart.dependencies.get_current_user import get_user_by_header
from cart_service.cart.services.cart import read_cart
from cart_service.cart.services.check_permissions import check_role_permissions
from cart_service.cart.services.total_price import calculate_total_price
from celery_client.celery_handler.cart_view_handler import handle_cart_view


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


@router.get("/send_message/")
async def send_messages():
    handle_cart_view.delay(
        settings.smtp_config.smtp_hostname,
        settings.smtp_config.smtp_port,
        settings.smtp_config.smtp_start_tls,
        settings.smtp_config.smtp_username,
        settings.smtp_config.smtp_password,
    )

    return {"message was sent successfully!"}
