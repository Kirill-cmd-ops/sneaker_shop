from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import db_helper
from cart_service.cart.schemas import CartSneakerCreate, CartSneakerUpdate

from cart_service.cart.dependencies.user_id import get_current_user_id
from cart_service.cart.config import settings
from cart_service.cart.services.cart.fetch import get_user_cart_id_service
from cart_service.cart.services.cart_sneaker.create import add_sneaker_to_cart_service
from cart_service.cart.services.cart_sneaker.delete import (
    delete_sneaker_from_cart_service,
)
from cart_service.cart.services.cart_sneaker.fetch import get_sneaker_in_cart_service
from cart_service.cart.services.cart_sneaker.update import (
    update_sneaker_in_cart_service,
    increment_sneaker_quantity_in_cart_service,
    decrement_sneaker_quantity_in_cart_service,
)
from cart_service.cart.dependencies.permissions import check_role_permissions
from cart_service.cart.services.sneaker.checkers import check_sneaker_exists_service
from cart_service.cart.services.sneaker_size.checkers import (
    check_sneaker_has_size_service,
)

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
async def add_sneaker_to_cart(
    item_create: CartSneakerCreate,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        cart_id = await get_user_cart_id_service(
            session=session,
            user_id=user_id,
        )
        await check_sneaker_exists_service(session=session, item_create=item_create)
        await check_sneaker_has_size_service(
            session=session,
            item_create=item_create,
        )
        sneaker_record = await get_sneaker_in_cart_service(
            session=session,
            cart_id=cart_id,
            item_create=item_create,
        )

        if sneaker_record is None:
            await add_sneaker_to_cart_service(
                session=session,
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
async def update_sneaker_in_cart(
    cart_sneaker_id: int,
    item_data: CartSneakerUpdate,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        updated_item = await update_sneaker_in_cart_service(
            session=session,
            cart_sneaker_id=cart_sneaker_id,
            size_id=item_data.size_id,
            user_id=user_id,
        )
        return {"status": "Элемент обновлён", "item_id": updated_item.id}


@router.delete(
    "/{cart_sneaker_id}",
    response_model=dict,
    dependencies=(Depends(check_role_permissions("cart.sneaker.delete")),),
)
async def delete_sneaker_from_cart(
    cart_sneaker_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        await delete_sneaker_from_cart_service(
            session=session,
            cart_sneaker_id=cart_sneaker_id,
            user_id=user_id,
        )
        return {"status": "Элемент удалён"}


@router.patch(
    "/{cart_sneaker_id}",
    response_model=dict,
    dependencies=(Depends(check_role_permissions("cart.sneaker.delete")),),
)
async def update_sneaker_quantity_in_cart(
    cart_sneaker_id: int,
    action: int = Query(..., ge=0, le=1),
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        cart_id = await get_user_cart_id_service(
            session=session,
            user_id=user_id,
        )

        if action == 1:
            result = await increment_sneaker_quantity_in_cart_service(
                cart_sneaker_id=cart_sneaker_id,
                cart_id=cart_id,
                session=session,
            )
        else:
            result = await decrement_sneaker_quantity_in_cart_service(
                cart_sneaker_id=cart_sneaker_id,
                cart_id=cart_id,
                session=session,
            )
        return result
