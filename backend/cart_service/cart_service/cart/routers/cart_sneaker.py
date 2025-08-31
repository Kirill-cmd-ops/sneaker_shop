from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from cart_service.cart.models import db_helper, Cart
from cart_service.cart.schemas.cart_sneaker import CartSneakerCreate, CartSneakerUpdate
from cart_service.cart.services.cart_sneaker import (
    create_sneaker_to_cart,
    delete_sneaker_to_cart,
    update_sneaker_to_cart,
)
from cart_service.cart.dependencies.get_current_user import get_user_by_header
from cart_service.cart.config import settings

router = APIRouter(
    prefix=settings.api.v1.cart_sneaker,
    tags=["Cart Sneaker"],
)


@router.post("/cart_add/", response_model=dict)
async def call_create_sneaker_to_cart(
    item: CartSneakerCreate,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    stmt = select(Cart).filter(Cart.user_id == user_id)
    result = await session.execute(stmt)
    user_cart = result.scalar_one_or_none()
    if not user_cart:
        raise HTTPException(status_code=404, detail="Корзина пользователя не найдена")

    new_item = await create_sneaker_to_cart(
        session,
        cart_id=user_cart.id,
        sneaker_id=item.sneaker_id,
        sneaker_size=item.sneaker_size,
    )
    return {"status": "Элемент добавлен", "item_id": new_item.id}


@router.put("/cart_update/{association_id}", response_model=dict)
async def call_update_sneaker_to_cart(
    association_id: int,
    item_data: CartSneakerUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    updated_item = await update_sneaker_to_cart(
        session, association_id=association_id, sneaker_size=item_data.sneaker_size
    )
    return {"status": "Элемент обновлён", "item_id": updated_item.id}


@router.delete("/cart_delete/{sneaker_id}", response_model=dict)
async def call_delete_sneaker_to_cart(
    sneaker_id: int,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await delete_sneaker_to_cart(session, user_id=user_id, sneaker_id=sneaker_id)
    return {"status": "Элемент удалён"}
