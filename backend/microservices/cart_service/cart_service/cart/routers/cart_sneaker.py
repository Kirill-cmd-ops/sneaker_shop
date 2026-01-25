from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import db_helper
from cart_service.cart.schemas import CartSneakerCreate

from cart_service.cart.dependencies.user_id import get_current_user_id
from cart_service.cart.config import settings
from cart_service.cart.services.cart.fetch import get_user_cart_id_service
from cart_service.cart.services.cart_sneaker.delete import (
    delete_sneaker_from_cart_service,
)
from cart_service.cart.services.cart_sneaker.orchestrators import (
    add_sneaker_to_cart_orchestrator,
    update_sneaker_quantity_in_cart_orchestrator,
)
from cart_service.cart.services.cart_sneaker.update import (
    update_sneaker_in_cart_service,
    increment_sneaker_quantity_in_cart_service,
    decrement_sneaker_quantity_in_cart_service,
)
from cart_service.cart.dependencies.permissions import check_role_permissions

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root, settings.api.v1.prefix, settings.api.v1.sneakers
    ),
    tags=["Cart Sneaker"],
)


@router.post(
    "/",
    response_model=dict,
)
async def add_sneaker_to_cart(
    item_create: CartSneakerCreate,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    sneaker_id = item_create.sneaker_id
    size_id = item_create.size_id

    return await add_sneaker_to_cart_orchestrator(
        session=session,
        user_id=user_id,
        sneaker_id=sneaker_id,
        size_id=size_id,
    )


@router.put(
    "/{cart_sneaker_id}",
    response_model=dict,
)
async def update_sneaker_in_cart(
    cart_sneaker_id: int,
    size_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    updated_item = await update_sneaker_in_cart_service(
        session=session,
        cart_sneaker_id=cart_sneaker_id,
        size_id=size_id,
        user_id=user_id,
    )
    return {"status": "Элемент обновлён", "item_id": updated_item.id}


@router.delete(
    "/{cart_sneaker_id}",
    response_model=dict,
)
async def delete_sneaker_from_cart(
    cart_sneaker_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await delete_sneaker_from_cart_service(
        session=session,
        cart_sneaker_id=cart_sneaker_id,
        user_id=user_id,
    )


@router.patch(
    "/{cart_sneaker_id}",
    response_model=dict,
)
async def update_sneaker_quantity_in_cart(
    cart_sneaker_id: int,
    action: int = Query(..., ge=0, le=1),
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await update_sneaker_quantity_in_cart_orchestrator(
        session=session,
        action=action,
        user_id=user_id,
        cart_sneaker_id=cart_sneaker_id,
    )
