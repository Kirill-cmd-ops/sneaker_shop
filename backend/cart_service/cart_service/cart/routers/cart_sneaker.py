from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from cart_service.cart.models import db_helper, Cart, CartSneakerAssociation
from cart_service.cart.schemas import CartSneakerCreate, CartSneakerUpdate
from cart_service.cart.schemas.cart_sneaker import (
    CartSneakerDelete,
    CartSneakerQuantity,
)
from cart_service.cart.services.cart_sneaker import (
    create_sneaker_to_cart,
    delete_sneaker_to_cart,
    update_sneaker_to_cart,
)
from cart_service.cart.dependencies.get_current_user import get_user_by_header
from cart_service.cart.config import settings
from cart_service.cart.services.check_permissions import check_role_permissions


router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root, settings.api.v1.prefix, settings.api.v1.sneaker
    ),
    tags=["Cart Sneaker"],
)


@router.post(
    "/add/",
    response_model=dict,
    dependencies=(Depends(check_role_permissions("cart.sneaker.add")),),
)
async def call_create_sneaker_to_cart(
    item_create: CartSneakerCreate,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    stmt = select(Cart).filter(Cart.user_id == user_id)
    result = await session.execute(stmt)
    user_cart = result.scalar_one_or_none()
    if not user_cart:
        raise HTTPException(status_code=404, detail="Корзина пользователя не найдена")

    stmt = select(CartSneakerAssociation).where(
        CartSneakerAssociation.cart_id == user_cart.id,
        CartSneakerAssociation.sneaker_id == item_create.sneaker_id,
        CartSneakerAssociation.sneaker_size == item_create.sneaker_size,
    )
    result = await session.execute(stmt)
    sneaker_record = result.scalar_one_or_none()

    if sneaker_record is None:
        await create_sneaker_to_cart(
            session,
            cart_id=user_cart.id,
            sneaker_id=item_create.sneaker_id,
            sneaker_size=item_create.sneaker_size,
        )
    else:
        sneaker_record.quantity += 1
        await session.commit()

    return {"status": "Элемент добавлен либо quantity + 1"}


@router.put(
    "/update/{association_id}",
    response_model=dict,
    dependencies=(Depends(check_role_permissions("cart.sneaker.update")),),
)
async def call_update_sneaker_to_cart(
    association_id: int,
    item_data: CartSneakerUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    updated_item = await update_sneaker_to_cart(
        session, association_id=association_id, sneaker_size=item_data.sneaker_size
    )
    return {"status": "Элемент обновлён", "item_id": updated_item.id}


@router.delete(
    "/delete/{sneaker_id}",
    response_model=dict,
    dependencies=(Depends(check_role_permissions("cart.sneaker.delete")),),
)
async def call_delete_sneaker_to_cart(
    item_delete: CartSneakerDelete,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await delete_sneaker_to_cart(
        session,
        item_delete=item_delete,
        user_id=user_id,
    )
    return {"status": "Элемент удалён"}


@router.patch(
    "/patch/decrease/{sneaker_id}",
    response_model=dict,
    dependencies=(
        Depends(check_role_permissions("cart.sneaker.delete")),
    ),  # Update after
)
async def decrease_cart_sneaker_quantity(
    item_quantity: CartSneakerQuantity,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    stmt = select(Cart).filter(Cart.user_id == user_id)
    result = await session.execute(stmt)
    user_cart = result.scalar_one_or_none()
    if not user_cart:
        raise HTTPException(status_code=404, detail="Корзина пользователя не найдена")

    stmt = select(CartSneakerAssociation).where(
        CartSneakerAssociation.cart_id == user_cart.id,
        CartSneakerAssociation.sneaker_id == item_quantity.sneaker_id,
        CartSneakerAssociation.sneaker_size == item_quantity.sneaker_size,
        CartSneakerAssociation.quantity > 1,
    )

    result = await session.execute(stmt)
    sneaker_record = result.scalar_one_or_none()

    if sneaker_record:
        sneaker_record.quantity -= 1

        await session.commit()
        return {"status": "quantity -= 1"}
    return {"status": "quantity = 1"}


@router.patch(
    "/patch/increase/{sneaker_id}",
    response_model=dict,
    dependencies=(
        Depends(check_role_permissions("cart.sneaker.delete")),
    ),  # Update after
)
async def increase_cart_sneaker_quantity(
    item_quantity: CartSneakerQuantity,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    stmt = select(Cart).filter(Cart.user_id == user_id)
    result = await session.execute(stmt)
    user_cart = result.scalar_one_or_none()
    if not user_cart:
        raise HTTPException(status_code=404, detail="Корзина пользователя не найдена")

    stmt = select(CartSneakerAssociation).where(
        CartSneakerAssociation.cart_id == user_cart.id,
        CartSneakerAssociation.sneaker_id == item_quantity.sneaker_id,
        CartSneakerAssociation.sneaker_size == item_quantity.sneaker_size,
    )

    result = await session.execute(stmt)
    sneaker_record = result.scalar_one_or_none()

    if sneaker_record:
        sneaker_record.quantity += 1

        await session.commit()
        return {"status": "quantity += 1"}
    return {"status": "there is no such record"}
