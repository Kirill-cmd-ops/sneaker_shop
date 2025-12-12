from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import db_helper
from cart_service.cart.schemas import CartSneakerCreate, CartSneakerUpdate
from cart_service.cart.services.cart_sneaker import (
    create_sneaker_to_cart,
    delete_sneaker_to_cart,
    update_sneaker_to_cart,
)
from cart_service.cart.dependencies.get_current_user import get_user_by_header
from cart_service.cart.config import settings
from cart_service.cart.services.check_cart import check_cart_exists
from cart_service.cart.services.check_permissions import check_role_permissions
from cart_service.cart.services.check_sneaker import check_sneaker_exists
from cart_service.cart.services.check_sneaker_in_cart import (
    check_sneaker_in_cart_exists,
)
from cart_service.cart.services.check_sneaker_size import check_sneaker_size_exists
from cart_service.cart.services.decrease_quantity import decrease_sneaker_quantity
from cart_service.cart.services.increase_quantity import increase_sneaker_quantity

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root, settings.api.v1.prefix, settings.api.v1.sneakers
    ),
    tags=["Cart Sneaker"],
)


@router.post(
    "/",
    response_model=dict,
    dependencies=(Depends(check_role_permissions("cart.sneaker.add")),),
)
async def call_create_sneaker_to_cart(
    item_create: CartSneakerCreate,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        cart_id = await check_cart_exists(session, user_id)
        await check_sneaker_exists(session, item_create)
        await check_sneaker_size_exists(session, item_create)
        sneaker_record = await check_sneaker_in_cart_exists(
            session, cart_id, item_create
        )

        if sneaker_record is None:
            await create_sneaker_to_cart(
                session,
                cart_id=cart_id,
                sneaker_id=item_create.sneaker_id,
                size_id=item_create.size_id,
            )
            return {"status": "Элемент добавлен"}

    return {"status": "Товар уже есть в корзине"}


@router.put(
    "/{cart_sneaker_id}",
    response_model=dict,
    dependencies=(Depends(check_role_permissions("cart.sneaker.update")),),
)
async def call_update_sneaker_to_cart(
    cart_sneaker_id: int,
    item_data: CartSneakerUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        updated_item = await update_sneaker_to_cart(
            session, cart_sneaker_id=cart_sneaker_id, size_id=item_data.size_id
        )
        return {"status": "Элемент обновлён", "item_id": updated_item.id}


@router.delete(
    "/{cart_sneaker_id}",
    response_model=dict,
    dependencies=(Depends(check_role_permissions("cart.sneaker.delete")),),
)
async def call_delete_sneaker_to_cart(
    cart_sneaker_id: int,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        await delete_sneaker_to_cart(
            session,
            cart_sneaker_id=cart_sneaker_id,
            user_id=user_id,
        )
        return {"status": "Элемент удалён"}


@router.patch(
    "/{cart_sneaker_id}",
    response_model=dict,
    dependencies=(Depends(check_role_permissions("cart.sneaker.delete")),),
)
async def cart_sneaker_quantity(
    cart_sneaker_id: int,
    action: int = Query(..., ge=0, le=1),
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        cart_id = await check_cart_exists(session, user_id)

        if action == 1:
            result = await increase_sneaker_quantity(cart_sneaker_id, cart_id, session)
        else:
            result = await decrease_sneaker_quantity(cart_sneaker_id, cart_id, session)
        return result
